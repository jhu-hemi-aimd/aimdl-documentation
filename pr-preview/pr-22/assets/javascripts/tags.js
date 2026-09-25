/* Hashtag queries use exact page tags; ordinary searches stay with Material. */
(() => {
  const base = new URL('../../', document.currentScript.src);
  let index;
  let request = 0;
  let renderedQuery;

  function queryParts(value) {
    const tags = [];
    const text = value.replace(/(^|\s)#([a-z0-9]+(?:[-_][a-z0-9]+)*)/gi,
      (_, space, tag) => { tags.push(tag.toLowerCase()); return space; })
      .replace(/(^|\s)#(?=\s|$)/g, '$1');
    return { tags, words: text.toLowerCase().trim().split(/\s+/).filter(Boolean) };
  }

  async function update() {
    const input = document.querySelector('[data-md-component="search-query"]');
    const output = document.querySelector('[data-tag-results]');
    const native = document.querySelector('[data-md-component="search-result"]');
    if (!input || !output || !native) return;
    // Refocusing the search must not remove the link being clicked.
    if (renderedQuery === input.value) return;
    renderedQuery = input.value;
    const version = ++request;
    const { tags, words } = queryParts(input.value);
    const partial = input.value.match(/(?:^|\s)#([a-z0-9_-]*)$/i);
    const tagMode = tags.length > 0 || partial !== null;
    native.hidden = tagMode;
    output.hidden = !tagMode;
    if (!tagMode) return;
    const status = document.createElement('div');
    status.className = 'md-search-result__meta';
    status.setAttribute('role', 'status');
    status.textContent = 'Searching tags…';
    if (!index) output.replaceChildren(status);
    try {
      index ||= fetch(new URL('tags.json', base)).then(response => {
        if (!response.ok) throw new Error('Tag index unavailable');
        return response.json();
      }).catch(error => { index = undefined; throw error; });
      const pages = await index;
      if (version !== request) return;
      const knownTags = [...new Set(pages.flatMap(page => page.tags))].sort();
      const prefix = partial?.[1].toLowerCase();
      const suggestions = prefix !== undefined && !knownTags.includes(prefix)
        ? knownTags.filter(tag => tag.startsWith(prefix)) : [];
      if (suggestions.length) {
        status.textContent = 'Choose a tag';
        const choices = document.createElement('nav');
        choices.className = 'tag-search-suggestions';
        choices.setAttribute('aria-label', 'Suggested tags');
        for (const tag of suggestions) {
          const link = document.createElement('a');
          link.href = `?q=${encodeURIComponent('#' + tag)}`;
          link.dataset.tagQuery = tag;
          link.textContent = `#${tag}`;
          choices.append(link);
        }
        output.replaceChildren(status, choices);
        return;
      }
      const matches = pages.filter(page => {
        const searchable = `${page.title} ${page.text}`.toLowerCase();
        return tags.every(tag => page.tags.includes(tag)) &&
          words.every(word => searchable.includes(word));
      });
      status.textContent = `${matches.length} matching ${matches.length === 1 ? 'page' : 'pages'}`;
      const list = document.createElement('ul');
      list.className = 'md-search-result__list';
      for (const page of matches) {
        const item = document.createElement('li');
        item.className = 'md-search-result__item';
        const link = document.createElement('a');
        link.className = 'md-search-result__link';
        link.href = new URL(page.url, base).href;
        const article = document.createElement('article');
        article.className = 'md-search-result__article md-typeset';
        const title = document.createElement('h1');
        title.className = 'md-search-result__title';
        title.textContent = page.title;
        const labels = document.createElement('p');
        labels.className = 'tag-search-labels';
        labels.textContent = page.tags.map(tag => `#${tag}`).join(' ');
        article.append(title, labels);
        link.append(article);
        item.append(link);
        list.append(item);
      }
      output.replaceChildren(status, list);
    } catch (_) {
      if (version === request) {
        renderedQuery = undefined;
        status.textContent = 'Tag search could not load. Please try again.';
        output.replaceChildren(status);
      }
    }
  }

  function mount() {
    const native = document.querySelector('[data-md-component="search-result"]');
    const input = document.querySelector('[data-md-component="search-query"]');
    if (!native || !input) return;
    if (!document.querySelector('[data-tag-results]')) {
      const output = document.createElement('div');
      output.className = 'md-search-result';
      output.dataset.tagResults = '';
      output.hidden = true;
      native.after(output);
      renderedQuery = undefined;
    }
    input.placeholder = 'Search';
    input.setAttribute('aria-label', 'Search');
    update();
  }

  document.addEventListener('input', event => {
    if (event.target.matches('[data-md-component="search-query"]')) update();
  });
  document.addEventListener('focusin', event => {
    if (event.target.matches('[data-md-component="search-query"]')) update();
  });
  document.addEventListener('reset', event => {
    if (event.target.querySelector('[data-md-component="search-query"]')) setTimeout(update, 0);
  });
  document.addEventListener('click', event => {
    const tag = event.target.closest('[data-tag-query]');
    if (!tag || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button !== 0) return;
    const input = document.querySelector('[data-md-component="search-query"]');
    if (!input) return;
    event.preventDefault();
    // Material closes search on any link click inside the search panel.
    // Handle tag choices before that listener (and instant navigation).
    event.stopPropagation();
    input.value = `#${tag.dataset.tagQuery}`;
    const toggle = document.getElementById('__search');
    if (toggle && !toggle.checked) {
      toggle.checked = true;
      toggle.dispatchEvent(new Event('change', { bubbles: true }));
    }
    input.focus();
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
  }, true);
  document.addEventListener('keydown', event => {
    const output = document.querySelector('[data-tag-results]');
    const input = document.querySelector('[data-md-component="search-query"]');
    if (!output || output.hidden || !input ||
        (event.target !== input && !output.contains(event.target))) return;
    const links = [...output.querySelectorAll('a')];
    if (!['ArrowDown', 'ArrowUp', 'Enter'].includes(event.key)) return;
    // Material's keyboard handler only knows about its native (hidden) results.
    event.preventDefault();
    event.stopPropagation();
    if (event.key === 'Enter') {
      (event.target === input ? links[0] : event.target.closest('a'))?.click();
    } else {
      const choices = [input, ...links];
      const step = event.key === 'ArrowDown' ? 1 : -1;
      const position = choices.indexOf(document.activeElement);
      choices[(position + step + choices.length) % choices.length].focus();
    }
  }, true);
  if (typeof document$ !== 'undefined') document$.subscribe(mount);
  else mount();
})();

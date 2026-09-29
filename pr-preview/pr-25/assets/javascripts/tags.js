/* Hashtag queries use exact page tags; ordinary searches stay with Material. */
(() => {
  const base = new URL('../../', document.currentScript.src);
  let index;
  let request = 0;

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
    const version = ++request;
    const { tags, words } = queryParts(input.value);
    const partial = input.value.match(/(?:^|\s)#([a-z0-9_-]*)$/i);
    const tagMode = tags.length > 0 || partial !== null;
    native.hidden = tagMode;
    output.hidden = !tagMode;
    if (!tagMode) return;
    output.replaceChildren();
    const status = document.createElement('div');
    status.className = 'md-search-result__meta';
    status.setAttribute('role', 'status');
    status.textContent = 'Searching tags…';
    output.append(status);
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
        output.append(choices);
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
      output.append(list);
    } catch (_) {
      if (version === request) status.textContent = 'Tag search could not load. Please try again.';
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
    input.value = `#${tag.dataset.tagQuery}`;
    input.focus();
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
  });
  if (typeof document$ !== 'undefined') document$.subscribe(mount);
  else mount();
})();

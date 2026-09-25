"""Render small tag links and export page-level data for hashtag searches."""

import html
import json
import re
from pathlib import Path
from urllib.parse import quote

from mkdocs.exceptions import PluginError
from mkdocs.plugins import event_priority

_pages = []


def on_pre_build(config):
    _pages.clear()


@event_priority(100)
def on_page_markdown(markdown, page, **kwargs):
    tags = page.meta.get("tags", [])
    if not isinstance(tags, list) or any(
        not isinstance(tag, str) or not re.fullmatch(r"[a-z0-9]+(?:[-_][a-z0-9]+)*", tag)
        for tag in tags
    ):
        raise PluginError(f"{page.file.src_uri}: tags must be a list of lowercase names, e.g. tags: [safety, sample-handling]")
    page.meta["tags"] = list(dict.fromkeys(tags))
    return markdown


@event_priority(-100)
def on_page_content(content, page, **kwargs):
    tags = page.meta.get("tags", [])
    if not tags or "tags" in page.meta.get("hide", []):
        return content
    links = " ".join(
        f'<a href="?q={quote("#" + tag, safe="")}" data-tag-query="{html.escape(tag)}">#{html.escape(tag)}</a>'
        for tag in tags
    )
    navigation = f'<nav class="page-tags" aria-label="Page tags" data-search-exclude>{links}</nav>'
    heading = re.search(r"</h1\s*>", content, re.IGNORECASE)
    if heading:
        return content[:heading.end()] + navigation + content[heading.end():]
    return f'<h1>{html.escape(page.title)}</h1>{navigation}{content}'


def on_page_context(context, page, **kwargs):
    if page.meta.get("search", {}).get("exclude", False):
        return context
    _pages.append({
        "url": page.url,
        "title": page.title,
        "tags": page.meta.get("tags", []),
        "text": html.unescape(re.sub(r"<[^>]+>", " ", page.content)),
    })
    return context


def on_post_build(config):
    Path(config["site_dir"], "tags.json").write_text(
        json.dumps(_pages, ensure_ascii=False), encoding="utf-8"
    )

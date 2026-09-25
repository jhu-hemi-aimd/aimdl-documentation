import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from mkdocs.exceptions import PluginError
from scripts import tags


class TagTests(unittest.TestCase):
    def page(self, **meta):
        return SimpleNamespace(meta=meta, title='Example <page>', url='nested/page/',
                               content='<h1>Example</h1><p>Content</p>',
                               file=SimpleNamespace(src_uri='nested/page.md'))

    def test_validation_and_deduplication(self):
        page = self.page(tags=['safety', 'sample-handling', 'safety'])
        tags.on_page_markdown('text', page)
        self.assertEqual(page.meta['tags'], ['safety', 'sample-handling'])
        for value in ('safety', [12], ['Two Words'], ['<script>'], ['#safety']):
            with self.subTest(value=value), self.assertRaises(PluginError):
                tags.on_page_markdown('text', self.page(tags=value))

    def test_links_follow_title_and_encode_hash(self):
        page = self.page(tags=['safety'])
        content = tags.on_page_content(page.content, page)
        self.assertIn('</h1><nav', content)
        self.assertIn('href="?q=%23safety"', content)
        self.assertIn('aria-label="Page tags"', content)
        self.assertEqual(content.count('class="page-tags"'), 1)

    def test_untagged_hidden_and_implicit_title(self):
        page = self.page()
        self.assertEqual(tags.on_page_content(page.content, page), page.content)
        page.meta = {'tags': ['safety'], 'hide': ['tags']}
        self.assertEqual(tags.on_page_content(page.content, page), page.content)
        page.meta = {'tags': ['safety']}
        self.assertTrue(tags.on_page_content('<p>Body</p>', page).startswith('<h1>Example &lt;page&gt;</h1>'))

    def test_index_exclusion_and_rebuild(self):
        tags.on_pre_build({})
        tags.on_page_context({}, self.page(tags=['safety']))
        tags.on_page_context({}, self.page(tags=['private'], search={'exclude': True}))
        with tempfile.TemporaryDirectory() as directory:
            config = {'site_dir': directory}
            tags.on_post_build(config)
            rows = json.loads(Path(directory, 'tags.json').read_text())
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['url'], 'nested/page/')
            self.assertEqual(rows[0]['tags'], ['safety'])
            tags.on_pre_build(config)
            tags.on_post_build(config)
            self.assertEqual(json.loads(Path(directory, 'tags.json').read_text()), [])

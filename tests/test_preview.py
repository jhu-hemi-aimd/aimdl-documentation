"""Prevent preview URL regressions, especially the /aimdl/ deployment prefix."""

import os
import unittest
from unittest.mock import patch

from scripts.preview import on_config


class PreviewConfigTests(unittest.TestCase):
    def config(self, url="https://docs.htmdec.org/aimdl/"):
        return {"site_url": url, "extra": {"existing": "preserved"}}

    def test_production_is_unchanged(self):
        with patch.dict(os.environ, {}, clear=True):
            config = self.config()
            self.assertEqual(on_config(config), self.config())

    def test_preview_preserves_production_prefix_and_metadata(self):
        with patch.dict(os.environ, {
            "DOCS_PREVIEW_PR": "123", "DOCS_PREVIEW_SHA": "abcdef0123456789"
        }, clear=True):
            config = on_config(self.config())
        self.assertEqual(config["site_url"],
                         "https://docs.htmdec.org/aimdl/pr-preview/pr-123/")
        self.assertEqual(config["extra"]["existing"], "preserved")
        self.assertEqual(config["extra"]["preview"], {
            "number": "123", "sha": "abcdef0",
            "production_url": "https://docs.htmdec.org/aimdl/",
        })

    def test_normalizes_missing_trailing_slash(self):
        with patch.dict(os.environ, {"DOCS_PREVIEW_PR": "7"}, clear=True):
            config = on_config(self.config("https://example.org/docs"))
        self.assertEqual(config["site_url"], "https://example.org/docs/pr-preview/pr-7/")

    def test_rejects_invalid_pr_paths(self):
        for number in ("../main", "0", "-1", "1/2", "１２", "1\n"):
            with self.subTest(number=number):
                with patch.dict(os.environ, {"DOCS_PREVIEW_PR": number}, clear=True):
                    with self.assertRaises(ValueError):
                        on_config(self.config())


if __name__ == "__main__":
    unittest.main()

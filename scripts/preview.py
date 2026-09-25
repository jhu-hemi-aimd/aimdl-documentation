"""Keep PR preview navigation under the production site's preview subfolder."""

import os
import re


def on_config(config):
    number = os.environ.get("DOCS_PREVIEW_PR", "")
    if not number:
        return config
    if not re.fullmatch(r"[1-9][0-9]*", number):
        raise ValueError("DOCS_PREVIEW_PR must be a positive PR number")
    production_url = config["site_url"].rstrip("/") + "/"
    config["extra"]["preview"] = {
        "number": number,
        "sha": os.environ.get("DOCS_PREVIEW_SHA", "")[:7],
        "production_url": production_url,
    }
    config["site_url"] = f"{production_url}pr-preview/pr-{number}/"
    return config

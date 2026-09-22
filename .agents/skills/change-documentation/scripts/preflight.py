#!/usr/bin/env python3
"""Preflight verification script for aimdl-documentation.

Validates YAML front matter against schema and executes strict MkDocs build checks.
"""

import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    sys.exit("Error: PyYAML is required. Install with: pip install pyyaml")

try:
    import jsonschema
except ImportError:
    sys.exit("Error: jsonschema is required. Install with: pip install jsonschema")


FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def extract_frontmatter(file_path: Path) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Extract and parse YAML front matter from a Markdown file."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as err:
        return None, f"Read error: {err}"

    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return None, "Missing opening or closing front matter delimiter ('---')"

    try:
        data = yaml.safe_load(match.group(1))
        if not isinstance(data, dict):
            return None, "Front matter must be a YAML mapping"
        return data, None
    except yaml.YAMLError as err:
        return None, f"YAML syntax error: {err}"


def normalize_metadata(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert YAML-parsed objects (like datetime.date) to JSON-compatible primitives."""
    normalized = {}
    for key, value in data.items():
        if isinstance(value, (datetime.date, datetime.datetime)):
            normalized[key] = value.isoformat()
        else:
            normalized[key] = value
    return normalized


def validate_frontmatter_files(docs_dir: Path, schema_path: Path) -> List[str]:
    """Validate all Markdown files in docs_dir against the JSON schema."""
    if not schema_path.is_file():
        return [f"Schema file not found at: {schema_path}"]

    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as err:
        return [f"Failed to parse schema {schema_path}: {err}"]

    errors: List[str] = []
    validator = jsonschema.Draft202012Validator(schema)

    for md_file in sorted(docs_dir.rglob("*.md")):
        rel_path = md_file.as_posix()
        raw_meta, parse_err = extract_frontmatter(md_file)

        if parse_err:
            errors.append(f"{rel_path}: {parse_err}")
            continue

        normalized = normalize_metadata(raw_meta or {})
        val_errors = sorted(validator.iter_errors(normalized), key=lambda e: e.path)

        for err in val_errors:
            field = ".".join(str(p) for p in err.path) if err.path else "root"
            errors.append(f"{rel_path} [{field}]: {err.message}")

    return errors


def run_mkdocs_build() -> bool:
    """Execute mkdocs build --strict."""
    print("Running 'mkdocs build --strict'...")
    try:
        result = subprocess.run(["mkdocs", "build", "--strict"], check=False)
        return result.returncode == 0
    except FileNotFoundError:
        print("'mkdocs' executable not found on PATH. Ensure virtual environment is activated.")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run documentation preflight validation.")
    parser.add_argument(
        "--docs-dir",
        default=Path("docs"),
        type=Path,
        help="Path to documentation source files (default: docs)",
    )
    parser.add_argument(
        "--schema",
        default=Path(".agents/schemas/frontmatter.schema.json"),
        type=Path,
        help="Path to front matter JSON schema",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Run only front matter validation and skip mkdocs build",
    )
    args = parser.parse_args()

    print("=== AIMD-L Documentation Preflight ===")

    # Step 1: Front Matter Schema Validation
    print(f"Validating front matter across '{args.docs_dir}'...")
    schema_errors = validate_frontmatter_files(args.docs_dir, args.schema)

    if schema_errors:
        print(f"\nFront matter schema validation failed ({len(schema_errors)} errors):")
        for err in schema_errors:
            print(f"  • {err}")
        sys.exit(1)

    print("Front matter validation passed.")

    # Step 2: Strict MkDocs Build
    if args.skip_build:
        print("⏩ Skipping MkDocs build (--skip-build requested).")
        sys.exit(0)

    build_success = run_mkdocs_build()
    if not build_success:
        print("\n'mkdocs build --strict' failed. Check logs above for broken links or nav errors.")
        sys.exit(1)

    print("Strict build succeeded. Safe to commit and push.")


if __name__ == "__main__":
    main()
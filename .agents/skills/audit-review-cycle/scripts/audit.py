#!/usr/bin/env python3
"""Audit documentation front matter for review cycles and ownership compliance."""

import argparse
import datetime
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    sys.exit("Error: PyYAML is required. Install with: pip install pyyaml")


FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_review_cycle(cycle_str: Optional[str]) -> Optional[datetime.timedelta]:
    """Convert strings like '6 months', '12 months', '90 days' into a timedelta."""
    if not cycle_str:
        return None
    cycle_str = str(cycle_str).strip().lower()
    match = re.match(r"^(\d+)\s*(day|month|year)s?$", cycle_str)
    if not match:
        return None

    count, unit = int(match.group(1)), match.group(2)
    if unit == "day":
        return datetime.timedelta(days=count)
    elif unit == "month":
        return datetime.timedelta(days=int(count * 30.4375))
    elif unit == "year":
        return datetime.timedelta(days=int(count * 365.25))
    return None


def parse_codeowners(codeowners_path: Path) -> List[Tuple[str, List[str]]]:
    """Parse .github/CODEOWNERS into a list of (pattern, [owners])."""
    if not codeowners_path.is_file():
        return []

    rules = []
    for line in codeowners_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        pattern = parts[0]
        owners = parts[1:]
        rules.append((pattern, owners))
    return rules


def match_codeowners(file_rel_path: str, rules: List[Tuple[str, List[str]]]) -> List[str]:
    """Find owners for a relative file path based on CODEOWNERS precedence (last match wins)."""
    matched_owners: List[str] = []
    norm_path = "/" + file_rel_path.lstrip("/")

    for pattern, owners in rules:
        # Standardize pattern prefix
        pat = pattern if pattern.startswith("/") else f"/{pattern}"
        if pat.endswith("/"):
            if norm_path.startswith(pat):
                matched_owners = owners
        elif pat.endswith("*"):
            prefix = pat.rstrip("*")
            if norm_path.startswith(prefix):
                matched_owners = owners
        elif norm_path == pat or norm_path.startswith(f"{pat}/"):
            matched_owners = owners

    return matched_owners


def extract_frontmatter(file_path: Path) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Extract and parse YAML front matter block from a Markdown file."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as err:
        return None, f"Read error: {err}"

    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return None, "Missing YAML front matter delimiter"

    try:
        data = yaml.safe_load(match.group(1))
        if not isinstance(data, dict):
            return None, "Front matter must be a YAML mapping"
        return data, None
    except yaml.YAMLError as err:
        return None, f"YAML syntax error: {err}"


def run_audit(docs_dir: Path, codeowners_path: Path, include_archived: bool = False) -> Dict[str, Any]:
    today = datetime.date.today()
    codeowner_rules = parse_codeowners(codeowners_path)

    report = {
        "audit_date": today.isoformat(),
        "overdue": [],
        "unreviewed": [],
        "upcoming": [],
        "missing_metadata": [],
        "ownership_mismatches": [],
    }

    for md_file in sorted(docs_dir.rglob("*.md")):
        rel_path = str(md_file.as_posix())
        meta, error = extract_frontmatter(md_file)

        if error or meta is None:
            report["missing_metadata"].append({"file": rel_path, "error": error})
            continue

        status = str(meta.get("status", "")).lower()
        if not include_archived and status in {"deprecated", "archived"}:
            continue

        title = meta.get("title", "Untitled")
        owner_team = meta.get("owner_team")
        primary_contact = meta.get("primary_contact")
        raw_cycle = meta.get("review_cycle")
        raw_last = meta.get("last_reviewed")

        owners = match_codeowners(rel_path, codeowner_rules)

        # Check for CODEOWNERS coverage
        team_token = f"@{owner_team}" if owner_team and not owner_team.startswith("@") else owner_team
        if not owners or (team_token and not any(team_token in o for o in owners)):
            report["ownership_mismatches"].append({
                "file": rel_path,
                "frontmatter_team": owner_team,
                "codeowners": owners,
            })

        # Check review status
        if not raw_last:
            report["unreviewed"].append({
                "file": rel_path,
                "title": title,
                "owner_team": owner_team,
                "primary_contact": primary_contact,
                "codeowners": owners,
            })
            continue

        # Parse last_reviewed date
        if isinstance(raw_last, (datetime.date, datetime.datetime)):
            last_date = raw_last if isinstance(raw_last, datetime.date) else raw_last.date()
        else:
            try:
                last_date = datetime.date.fromisoformat(str(raw_last).strip())
            except ValueError:
                report["missing_metadata"].append({
                    "file": rel_path,
                    "error": f"Invalid date format: '{raw_last}'",
                })
                continue

        cycle_delta = parse_review_cycle(raw_cycle)
        if not cycle_delta:
            report["missing_metadata"].append({
                "file": rel_path,
                "error": f"Invalid or missing review_cycle: '{raw_cycle}'",
            })
            continue

        due_date = last_date + cycle_delta
        days_until_due = (due_date - today).days

        item = {
            "file": rel_path,
            "title": title,
            "owner_team": owner_team,
            "primary_contact": primary_contact,
            "last_reviewed": last_date.isoformat(),
            "due_date": due_date.isoformat(),
            "review_cycle": str(raw_cycle),
            "codeowners": owners,
            "days_overdue": -days_until_due if days_until_due < 0 else 0,
        }

        if days_until_due < 0:
            report["overdue"].append(item)
        elif days_until_due <= 30:
            item["days_remaining"] = days_until_due
            report["upcoming"].append(item)

    return report


def main():
    parser = argparse.ArgumentParser(description="Audit documentation review cycles.")
    parser.add_argument("--path", default="docs", type=Path, help="Path to docs directory")
    parser.add_argument("--codeowners", default=".github/CODEOWNERS", type=Path, help="Path to CODEOWNERS")
    parser.add_argument("--include-archived", action="store_true", help="Include archived and deprecated files")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON only")
    args = parser.parse_args()

    results = run_audit(args.path, args.codeowners, args.include_archived)

    if args.json or not sys.stdout.isatty():
        print(json.dumps(results, indent=2))
        return

    # Console summary formatting
    print(f"=== Doc Review Cycle Audit ({results['audit_date']}) ===\n")

    if results["overdue"]:
        print(f"Overdue Pages ({len(results['overdue'])}):")
        for item in results["overdue"]:
            print(f"  • {item['file']} ('{item['title']}') - {item['days_overdue']} days overdue")
            print(f"    Owner: {item['owner_team']} | Contact: {item['primary_contact']} | CODEOWNERS: {', '.join(item['codeowners']) or 'None'}")
        print()

    if results["unreviewed"]:
        print(f"Unreviewed Pages ({len(results['unreviewed'])}):")
        for item in results["unreviewed"]:
            print(f"  • {item['file']} (last_reviewed: null)")
        print()

    if results["ownership_mismatches"]:
        print(f"Ownership Discrepancies ({len(results['ownership_mismatches'])}):")
        for item in results["ownership_mismatches"]:
            print(f"  • {item['file']}: front matter '{item['frontmatter_team']}' does not match CODEOWNERS {item['codeowners']}")
        print()

    if results["upcoming"]:
        print(f"Due within 30 Days ({len(results['upcoming'])}):")
        for item in results["upcoming"]:
            print(f"  • {item['file']} - {item.get('days_remaining', 0)} days remaining (due {item['due_date']})")
        print()

    if not any([results["overdue"], results["unreviewed"], results["missing_metadata"], results["ownership_mismatches"]]):
        print("All active documentation is up to date and correctly mapped!")


if __name__ == "__main__":
    main()
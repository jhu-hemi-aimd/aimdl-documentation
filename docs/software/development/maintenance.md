---
title: "Maintaining the control documentation"
status: needs-review
owner_team: software-team
primary_contact: null
last_reviewed: null
review_cycle: 12 months
safety_level: informational
tags: [software, controls]
---

# Maintaining the control documentation

Follow the repository's [contribution workflow](../../tutorials/contributing.md): issue, branch, edits, validation, pull request, review. Do not push directly to `main` or mark content reviewed merely because it was generated.

## Update source-derived pages

When behavior changes, update the repository overview, affected controller/API/state reference, examples and source-review notes together. Record the new source revisions or archive hashes in the snapshot page. Keep run scripts as downloadable JSON and link them from the controller pages. Do not silently update a historical script that is intended to preserve a supplied experiment.

Every new Markdown page needs the full front matter and one matching H1. Add it to `mkdocs.yml` navigation and use relative links. Operational examples remain subject to instrument-owner review.

## Generate error documentation from AIMDDS

Install `generate_error_doc.py` beside the existing `generate_error_pdf.py` in `aimdds/src/api/scripts/`. The supplied additions archive also contains its standard-library unit tests. Run from any working directory:

```bash
python /path/to/aimdds/src/api/scripts/generate_error_doc.py \
  /path/to/aimdl-documentation/docs/software/reference/error-codes.md
```

The script resolves the AIMDDS API root relative to itself. A separately downloaded copy can use an explicit source root:

```bash
python generate_error_doc.py \
  /path/to/aimdl-documentation/docs/software/reference/error-codes.md \
  --api-root /path/to/aimdds/src/api
```

The generator imports the same error package/central registry as the application, discovers subsystem titles/ranges, verifies exact central-registry coverage, sorts deterministically and emits all definition fields with stable `error-<code>` anchors. It also validates duplicate codes and range/key consistency. It uses only the Python standard library and does not initialize Django, connect to PostgreSQL or import instrument SDKs.

Use Python 3.11 or later for the current registry's `StrEnum` dependency. Run drift detection without changing the file:

```bash
python /path/to/aimdds/src/api/scripts/generate_error_doc.py \
  /path/to/aimdl-documentation/docs/software/reference/error-codes.md --check
```

Exit codes: 0 success/current, 1 missing or stale output in check mode, 2 generation/import/I/O failure. The generated page intentionally keeps `last_reviewed: null`; generation does not perform a human review. Modify error definitions in AIMDDS, then regenerate both PDF and Markdown rather than editing the catalog by hand.

Run tests in the AIMDDS checkout:

```bash
python -m unittest discover -s src/api/scripts -p test_generate_error_doc.py -v
```

The documentation build consumes checked-in Markdown, so readers/builders do not need AIMDDS or access to hardware. The symbol audit is a separate reference and should also be updated when controller enums or robotics mappings change.

## Validate the documentation

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python .agents/skills/change-documentation/scripts/preflight.py
python -m unittest discover -s tests
mkdocs build --strict
```

Preflight validates front matter and runs the strict build. `jsonschema` is included in requirements so this documented gate is installable. For an extracted archive without Git history, disable only the revision-date plugin:

```bash
ENABLE_GIT_REVISION_DATE=false mkdocs build --strict
```

Use the normal build in a Git checkout. Preview with `mkdocs serve`, inspect navigation/tables/diagrams on narrow and wide screens, then request documentation-steward review. The build's strict link/nav validation does not validate experiment safety or vendor settings.

## Ownership and review

Software pages use `software-team` metadata as the existing software section does. Current CODEOWNERS still routes repository review to documentation stewards until the per-instrument teams exist. Keep safety review attached to the original instrument/safety pages; this software reference does not introduce new safety procedures.

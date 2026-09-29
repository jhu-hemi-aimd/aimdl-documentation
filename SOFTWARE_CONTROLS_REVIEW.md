# Software and controls documentation delivery

Prepared 2026-09-29 from the supplied repository archives, error PDF, full SMHM example and uploaded documentation baseline. Source fingerprints are recorded in `docs/software/reference/source-snapshot.md`.

## Contents

- 27 software pages covering AIMDAS, AIMDDS, AIMDRM, AIMDRC, MAXIMA, HELIX, SPHINX and COORD.
- Front-end actions, implemented API endpoints, scheduling decisions, shared-client state transitions, OPC UA structure, coordinate transforms, setup, data handling and recovery.
- Seven downloadable schema-version-2 examples; the full supplied SMHM script is unchanged.
- Six Mermaid diagrams using the repository's existing Material/SuperFences configuration.
- A generated catalog of all 170 AIMDDS definitions, plus a controller-symbol crosswalk that identifies two unregistered HELIX heating-laser codes.
- A companion AIMDDS additions archive containing `src/api/scripts/generate_error_doc.py` and six unit tests. The generator uses the standard library and the canonical AIMDDS registry, with deterministic output and a read-only `--check` mode.

## Verification results

| Check | Result |
| --- | --- |
| AIMDDS generator unit tests | 6 passed |
| Existing documentation preview-configuration tests | 4 passed |
| Python compilation of generator and tests | Passed |
| Generated catalog drift check | Passed |
| PDF/registry numeric code-set comparison | Same 170 codes; this was not a field-by-field PDF text comparison |
| JSON examples through actual AIMDDS `validate_run_script` and `parse_run_script` | All 7 passed |
| Inline JSON | All 8 blocks parsed; complete scripts passed the source validator |
| Full SMHM preservation | Byte-for-byte match |
| Static documentation inspection | 68 pages in navigation, metadata schema-keyword checks, 320 relative links/anchors; no detected errors |
| Mermaid | Six source blocks inspected; browser rendering not verified |
| Official preflight | Blocked: `jsonschema` is unavailable |
| Strict MkDocs build / remaining MkDocs-dependent tests | Blocked: `mkdocs` is unavailable; dependency installation was denied by environment package-network restrictions |

The static inspection used PyYAML and repository-specific checks. It does not substitute for the repository's official JSON Schema validator, MkDocs build or browser inspection. This delivery must not be represented as having passed the strict build. No device connections, physical runs, production writes or hardware-readiness tests were performed.

## Complete the required build gate

From an authorized documentation Git checkout with these changes applied:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python .agents/skills/change-documentation/scripts/preflight.py
python -m unittest discover -s tests
mkdocs build --strict
```

For the extracted archive without Git history, set `ENABLE_GIT_REVISION_DATE=false` for preflight and build:

```bash
ENABLE_GIT_REVISION_DATE=false python .agents/skills/change-documentation/scripts/preflight.py
ENABLE_GIT_REVISION_DATE=false mkdocs build --strict
```

Inspect the generated site, especially navigation, wide API tables, error anchors and Mermaid diagrams. Keep the new pages `needs-review` until instrument/software owners have reviewed the implementation descriptions and examples.

## Integration and contribution workflow

The GitHub connector was blocked by organization SAML authorization. No issue, remote branch, commit or pull request was created. The uploaded ZIP was used as the baseline; current remote HEAD could not be compared. Apply this archive's changed/new files on an authorized contribution branch, link an issue, complete the build gate, and open a review PR according to the repository's contributing instructions. Do not replace a newer remote checkout wholesale without reviewing its changes.

Install the two companion Python files beside AIMDDS's existing `generate_error_pdf.py`. Run from the AIMDDS checkout:

```bash
python -m unittest discover -s src/api/scripts -p test_generate_error_doc.py -v
python src/api/scripts/generate_error_doc.py   /path/to/aimdl-documentation/docs/software/reference/error-codes.md --check
```

Remove `--check` to regenerate the checked-in error reference. Python 3.11+ is required by the current error package. The standalone generator download requires `--api-root /path/to/aimdds/src/api` unless installed in its intended location.

## Supporting repository fixes

- Added the Software navigation tree and cross-links from instrument, home, data and troubleshooting pages.
- Kept existing instrument procedures and safety content intact; labeled the MAXIMA legacy script reference and linked the current schema.
- Added missing required metadata on existing pages so they can pass the published schema.
- Allowed the existing `reviewers` and `hide` metadata fields in the schema instead of dropping them from their pages.
- Added `jsonschema` to requirements because the official preflight imports it.
- Added an environment switch for the Git revision-date plugin so source ZIPs can build without a Git history. Git-checkout behavior remains enabled by default.

## Findings for maintainer review

The source-review page records implementation limitations rather than silently presenting README intent as working behavior. These include unimplemented pause/resume, bypassed MAXIMA calibration and adaptive count time, cancellation cleanup limits, absent scheduler readiness gates, a defective nested error-list action, optional/nonpersistent result behavior and missing heating-laser error definitions. Control-software fixes are outside this documentation patch.

## Change inventory

This inventory is relative to the uploaded documentation ZIP. This delivery report is also new.

### New files

- `docs/software/architecture.md`
- `docs/software/controllers/coord.md`
- `docs/software/controllers/helix.md`
- `docs/software/controllers/maxima.md`
- `docs/software/controllers/sphinx.md`
- `docs/software/development/controller-interface.md`
- `docs/software/development/maintenance.md`
- `docs/software/examples/coord-maxima.json`
- `docs/software/examples/coord-photo-only.json`
- `docs/software/examples/coord.json`
- `docs/software/examples/helix.json`
- `docs/software/examples/index.md`
- `docs/software/examples/maxima.json`
- `docs/software/examples/smhm.json`
- `docs/software/examples/sphinx.json`
- `docs/software/operations/data-and-recovery.md`
- `docs/software/operations/troubleshooting.md`
- `docs/software/operator-guide.md`
- `docs/software/reference/api.md`
- `docs/software/reference/coordinates.md`
- `docs/software/reference/error-codes.md`
- `docs/software/reference/error-symbols.md`
- `docs/software/reference/opcua.md`
- `docs/software/reference/run-scripts.md`
- `docs/software/reference/source-review.md`
- `docs/software/reference/source-snapshot.md`
- `docs/software/repositories/aimdas.md`
- `docs/software/repositories/aimdds.md`
- `docs/software/repositories/aimdrc.md`
- `docs/software/repositories/aimdrm.md`
- `docs/software/setup/index.md`
- `docs/software/setup/services.md`
- `docs/software/setup/stations.md`

### Modified files

- `.agents/schemas/frontmatter.schema.json`
- `README.md`
- `docs/data-management/index.md`
- `docs/index.md`
- `docs/instruments/helix/index.md`
- `docs/instruments/index.md`
- `docs/instruments/maxima/index.md`
- `docs/instruments/maxima/reference/run-scripts.md`
- `docs/instruments/robotics/index.md`
- `docs/instruments/run_manager/index.md`
- `docs/instruments/sphinx/index.md`
- `docs/onboarding/index.md`
- `docs/policies/documentation-review.md`
- `docs/policies/index.md`
- `docs/software/index.md`
- `docs/troubleshooting/index.md`
- `docs/tutorials/contributing.md`
- `docs/tutorials/index.md`
- `mkdocs.yml`
- `requirements.txt`

### Removed files

None.

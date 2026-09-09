# aimdl-documentation

Documentation portal for the AIMD-L laboratory: SOPs, instrument manuals,
safety policies, onboarding, software setup, data management, and tutorials.
Deployed at [https://docs.htmdec.org/aimdl/](https://docs.htmdec.org/aimdl/). Created by the AIMD-L Documentation Stewards, an intrepid band disseminating information for users, developers, and AIMD-L bon vivants. You will someday be able to reach the Documentation Stewards by emailing info@htmdec.org but for now you will have to make do by asking someone from the Elbert Data Rabble, Matt, or Joseph.

## Creating/Maintaining Documentation

Basic instructions for adding to the documentation are in [contributing.md](docs/tutorials/contributing.md).  The instructions include info on how to use a coding agent to edit or contribute to this repo and documentation site.

A fundamental rule is that the main branch is protected — nobody edits it directly. Every change follows the same path: issue → branch → edits → commit/push → pull request → review → merge. This is standard GitHub usage but make sure you understand that you have to make an issue and a related branch where you work. Your work doesn't get to the main branch until you make a pull request (PR) and have it reviewed by someone on the Documentation Steward Team. When your PR is approved and merges, the site rebuilds and deploys automatically within a couple of minutes.

Continuous Integration (CI) runs `mkdocs build --strict` on every PR: a broken link, or a page added without a nav entry (or removed without cleaning up its links), fails the build.

## Local preview

```bash
pip install -r requirements.txt
mkdocs serve        # http://127.0.0.1:8000
```

`mkdocs build --strict` must pass before merging — CI enforces it, and it
fails on any broken internal link, so only link pages that exist.

## Version 1 scope

This is the **MkDocs-only** version of the architecture described in
[`planning/architecture-plan.md`](planning/architecture-plan.md):

- one repository, folder-level ownership (Model A), one build, one search index;
- operational documentation and *static* tutorials only;
- page-level YAML front matter for ownership/review metadata
  (see [Documentation review](docs/policies/documentation-review.md)).

Deliberately deferred to later versions:

- **Executable tutorials** (Jupyter Book / MyST, or `mkdocs-jupyter`) — the
  `docs/tutorials/` section is the seam where they attach.
- **Multi-repository assembly** (monorepo plugin, submodules, Model B).
- **Machine-readable instrument metadata** (`metadata/*.yml`) — add only when
  a script or page actually consumes it.

## Deployment

Pushes to `main` build strictly and publish to the `gh-pages` branch via
GitHub Actions. Enable GitHub Pages (source: `gh-pages` branch) in the
repository settings after the first successful workflow run.

# aimdl-documentation

Documentation portal for the AIMD-L laboratory: SOPs, instrument manuals,
safety policies, onboarding, software setup, data management, and tutorials.
Built with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
and deployed to GitHub Pages.

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
- Custom domain (`docs.aimdl.jhu.edu`) — configure after Pages deployment works.

## Deployment

Pushes to `main` build strictly and publish to the `gh-pages` branch via
GitHub Actions. Enable GitHub Pages (source: `gh-pages` branch) in the
repository settings after the first successful workflow run.

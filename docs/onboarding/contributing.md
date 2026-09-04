---
title: Updating the docs
status: active
owner_team: docs-stewards
last_reviewed: 2026-09-04
review_cycle: 12 months
safety_level: informational
---

# Updating the docs

This page is for members of the documentation teams: how to get access and
how to get a change published on this site.

## 1. Get access (one time)

1. Create a [GitHub account](https://github.com) if you don't have one.
2. Ask a documentation steward to add you to your team on
   `jhu-hemi-aimd/aimdl-documentation` with **write** access, and accept the
   invitation that arrives by email.
3. Clone the repository:

   ```bash
   git clone https://github.com/jhu-hemi-aimd/aimdl-documentation.git
   ```

## 2. How a change reaches the site

`main` is protected — nobody edits it directly. Every change follows the same
path: **issue → branch → edits → pull request → review → merge**. When your PR
merges, the site rebuilds and deploys automatically within a couple of minutes.

CI runs `mkdocs build --strict` on every PR: a broken link, or a page added
without a nav entry (or removed without cleaning up its links), fails the build.

## 3. Step by step

1. **Open an issue** describing the change: which page, what's wrong or
   missing, why. This gives the change a number, say `#12`.
2. **Create a branch** from up-to-date `main`:

   ```bash
   git switch main && git pull
   git switch -c docs/12-maxima-startup
   ```

3. **Write.** Pages are Markdown files under `docs/`, one folder per
   instrument or topic. Start every page with the front matter block below.
   If you *add* a page, add it to `nav:` in `mkdocs.yml`; if you *rename or
   remove* one, update the nav and any links to it in the same commit.
   Preview live while you write:

   ```bash
   pip install -r requirements.txt   # first time only
   mkdocs serve                      # http://127.0.0.1:8000
   ```

4. **Check** before pushing — this is exactly what CI will run:

   ```bash
   mkdocs build --strict
   ```

5. **Commit and push:**

   ```bash
   git add -A
   git commit -m "Add MAXIMA startup procedure (#12)"
   git push -u origin docs/12-maxima-startup
   ```

6. **Open a pull request** on GitHub with `Fixes #12` in the description, and
   request a review from your team's reviewers (safety-critical pages also
   need the lab safety team). When the review is approved and CI is green,
   the PR can be merged — and you're published.

### Front matter template

```yaml
---
title: Page title
status: draft            # draft | active | needs-review | deprecated | archived
owner_team: your-team
primary_contact: TBD
last_reviewed: null
review_cycle: 6 months
safety_level: operational  # informational | operational | safety-critical | restricted
---
```

## 4. The easy way: let a coding agent do the bookkeeping

If you use Claude Code (or another coding agent with GitHub access) inside
your clone, the issue, branch, checks, and PR can all be handled for you.
Run `gh auth login` once, then paste this prompt and fill in the first blank:

```text
You are in my local clone of jhu-hemi-aimd/aimdl-documentation, the AIMD-L
documentation site (Material for MkDocs; CI runs `mkdocs build --strict`).

I want to make this documentation change:
<DESCRIBE IT: which page(s) or new page, which instrument/topic, what content>

Do the following:
1. Create a GitHub issue for the change with `gh issue create`; call its number N.
2. Update main (`git switch main && git pull`) and create a branch named
   docs/N-<short-slug>.
3. Make the edits under docs/: every page starts with the same YAML front
   matter used by existing pages; a new page also gets a nav entry in
   mkdocs.yml; a renamed or removed page gets its nav entry and inbound
   links fixed in the same commit.
4. Write the content with me: ask me for any facts you are missing instead of
   guessing — never invent procedures, safety steps, or parameter values.
5. Run `mkdocs build --strict` and fix problems until it passes.
6. Commit with a message that references #N and push the branch.
7. Open a pull request with `gh pr create`, body "Fixes #N", and request
   review from the owner_team in the page's front matter (for safety-critical
   pages, also the lab safety team).
8. Do NOT push to main and do NOT merge. When done, give me the issue and
   PR links so I can follow the review.
```

You stay responsible for the content — read what the agent wrote before the
PR goes to review, exactly as you would your own draft.

Questions? Ask the documentation stewards.

# AIMD-L documentation architecture and starter configuration

**Purpose:** This document gives AIMD-L a practical starting architecture for a documentation system that supports both operational laboratory documentation and reproducible computational tutorials.

**Recommended pattern:**

- Use **Material for MkDocs** as the central AIMD-L documentation portal.
- Use **Jupyter Book / MyST** for executable tutorials, computational notebooks, and reproducible analysis workflows.
- Give each collaboration team explicit responsibility for its own content using either folder-level ownership in one repository or repository-level ownership with a central documentation assembly workflow.

This document is intended to become either:

1. the initial `README.md` for the central `aimdl-docs` repository; or
2. a planning document in an AIMD-L documentation governance repository.

--

## 1. Design goals

AIMD-L needs documentation for two related but different use cases.

### 1.1 Operational documentation

Operational documentation answers questions such as:

- How do I safely enter, use, and leave the lab?
- How do I start up, shut down, calibrate, or troubleshoot an instrument?
- What software stack do I need for a particular instrument or workflow?
- Who owns a procedure, when was it reviewed, and who can approve changes?
- What should a new student, postdoc, staff scientist, or collaborator read first?

This content should be easy to edit, fast to search, and governed with clear ownership. It should not require authors to understand executable notebooks.

**Recommended renderer:** Material for MkDocs.

### 1.2 Reproducible computational documentation

Computational documentation answers questions such as:

- How do I reproduce this figure, analysis, or dataset transformation?
- How do I query AIMD-L data services from Python?
- How do I process XRD, ptychography, laser shock, or microscopy data?
- How do I execute a Dagster workflow or validate a data pipeline?
- What software environment and input data are required to reproduce a result?

This content benefits from notebooks, executable MyST Markdown, cached outputs, environment files, and explicit data provenance.

**Recommended renderer:** Jupyter Book / MyST.

--

## 2. Recommended top-level architecture

Use a central documentation portal as the authoritative entry point:

```text
https://docs.aimdl.jhu.edu/
```

Recommended URL structure:

```text
/
  about/
  onboarding/
  safety/
  instruments/
    maxima/
    amdee-xrd/
    laser-shock/
    robotics/
  software/
  data-management/
  troubleshooting/
  policies/
  tutorials/
    xrd-analysis/
    girder-query/
    dagster-workflow/
    materials-data-model/
```

Recommended rendering strategy:

```text
Material for MkDocs
  Main portal
  Safety
  Onboarding
  Instrument manuals
  SOPs
  Software setup
  Data management
  Troubleshooting
  Policy and reference pages

Jupyter Book / MyST
  Executable tutorials
  Reproducible computational examples
  Dataset-to-figure workflows
  Workshop material
  Analysis narratives
  Publication-like technical reports
```

--

## 3. Repository models

There are two practical repository models. AIMD-L can start with Model A and later evolve to Model B.

### Model A: single central repository with folder ownership

This is the simplest model and should be the default starting point unless teams require separate repositories.

```text
aimdl-docs/
  README.md
  mkdocs.yml
  requirements.txt
  .github/
    workflows/
      ci.yml
      deploy.yml
    CODEOWNERS
  docs/
    index.md
    about/
    onboarding/
    safety/
    instruments/
      index.md
      maxima/
      amdee-xrd/
      laser-shock/
      robotics/
    software/
    data-management/
    troubleshooting/
    policies/
    tutorials/
      index.md
  metadata/
    instruments/
      maxima.yml
      amdee-xrd.yml
      laser-shock.yml
      robotics.yml
    teams.yml
    review-policy.yml
```

Advantages:

- One build.
- One navigation system.
- One search index.
- One issue tracker.
- Straightforward GitHub Pages deployment.
- Clear folder-level ownership using `CODEOWNERS`.

Disadvantages:

- Teams do not have fully independent repositories.
- A central review process is needed to prevent conflicts.

### Model B: central assembly repository plus team-owned repositories

Use this when teams need independent repositories but AIMD-L still wants one unified documentation portal.

```text
aimdl-docs-site/                    # Central assembly repository
  mkdocs.yml
  requirements.txt
  .github/
    workflows/
      ci.yml
      deploy.yml
  docs/
    index.md
    about/
    onboarding/
    safety/
    tutorials/
      index.md
  external/                         # Populated by GitHub Actions or git submodules
    maxima-sop/
    amdee-xrd-docs/
    laser-shock-docs/
    robotics-docs/

aimdl-maxima-docs/                  # Team-owned repository
  mkdocs.yml
  docs/
    index.md
    safety.md
    startup.md
    shutdown.md
    troubleshooting.md
    reference.md

aimdl-amdee-xrd-docs/               # Team-owned repository
  mkdocs.yml
  docs/
    index.md
    access.md
    measurement.md
    calibration.md
    data.md
    troubleshooting.md

aimdl-tutorials/                    # Jupyter Book / MyST repository
  myst.yml
  requirements.txt
  environment.yml
  README.md
  tutorials/
    xrd-analysis.md
    girder-query.ipynb
    dagster-workflow.md
```

Advantages:

- Each collaboration team can own its own repository.
- The central site can still present one consistent documentation portal.
- Team-specific CI can validate each repository before integration.

Disadvantages:

- More CI/CD complexity.
- One team can break the central build if validation is weak.
- Cross-repository navigation must be intentionally maintained.

--

## 4. Central Material for MkDocs portal

### 4.1 Recommended central repository name

Use one of the following:

```text
aimdl-docs
```

or, if the repository is only for assembly from many repositories:

```text
aimdl-docs-site
```

Recommended public site:

```text
https://docs.aimdl.jhu.edu/
```

Recommended GitHub Pages fallback:

```text
https://aimd-l.github.io/aimdl-docs/
```

Replace `aimd-l` with the actual GitHub organization name.

---

## 5. Central repository: `requirements.txt`

Use pinned versions once the first deployment is stable. Start unpinned during prototyping if necessary.

```text
mkdocs
mkdocs-material
mkdocs-git-revision-date-localized-plugin
mkdocs-minify-plugin
mkdocs-redirects
mkdocs-monorepo-plugin
pymdown-extensions
```

If the initial site does not aggregate external MkDocs projects, omit `mkdocs-monorepo-plugin` until needed.

---

## 6. Central repository: base `mkdocs.yml`

This version assumes Model A: one central repository with all operational docs under `docs/`.

```yaml
site_name: AIMD-L Documentation
site_description: Documentation portal for the AI for Materials Design Laboratory
site_author: AIMD-L
site_url: https://docs.aimdl.jhu.edu/

repo_name: AIMD-L/aimdl-docs
repo_url: https://github.com/AIMD-L/aimdl-docs
edit_uri: edit/main/docs/

docs_dir: docs
site_dir: site

copyright: Copyright &copy; Johns Hopkins University and AIMD-L contributors

theme:
  name: material
  language: en
  logo: assets/images/aimdl-logo.svg
  favicon: assets/images/favicon.ico
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.indexes
    - navigation.top
    - search.highlight
    - search.share
    - content.action.edit
    - content.action.view
    - content.code.copy
    - content.code.annotate
    - toc.follow
  palette:
    - scheme: default
      primary: blue
      accent: blue
      toggle:
        icon: material/weather-night
        name: Switch to dark mode
    - scheme: slate
      primary: blue
      accent: blue
      toggle:
        icon: material/weather-sunny
        name: Switch to light mode

plugins:
  - search
  - git-revision-date-localized:
      enable_creation_date: true
      type: date
  - minify:
      minify_html: true
  - redirects:
      redirect_maps: {}

markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - tables
  - toc:
      permalink: true
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg

nav:
  - Home: index.md
  - About:
      - Overview: about/index.md
      - People and roles: about/people.md
      - Documentation governance: about/governance.md
  - Onboarding:
      - Start here: onboarding/index.md
      - Accounts and access: onboarding/accounts.md
      - Required training: onboarding/training.md
      - First-week checklist: onboarding/first-week.md
  - Safety:
      - Safety overview: safety/index.md
      - Lab access: safety/access.md
      - X-ray safety: safety/xray.md
      - Laser safety: safety/laser.md
      - Robotics safety: safety/robotics.md
      - Emergency procedures: safety/emergency.md
  - Instruments:
      - Overview: instruments/index.md
      - MAXIMA: instruments/maxima/index.md
      - AMDEE XRD: instruments/amdee-xrd/index.md
      - Laser Shock: instruments/laser-shock/index.md
      - Robotics: instruments/robotics/index.md
  - Software:
      - Overview: software/index.md
      - Workstations: software/workstations.md
      - Python environments: software/python.md
      - Data access clients: software/data-access.md
      - Container workflows: software/containers.md
  - Data management:
      - Overview: data-management/index.md
      - Data lifecycle: data-management/lifecycle.md
      - Metadata and identifiers: data-management/metadata-identifiers.md
      - Girder / DMS: data-management/girder.md
      - File formats: data-management/file-formats.md
      - Archival and publication: data-management/archive-publication.md
  - Tutorials:
      - Overview: tutorials/index.md
      - Reproducible XRD analysis: tutorials/xrd-analysis.md
      - Querying AIMD-L data: tutorials/girder-query.md
      - Dagster workflows: tutorials/dagster-workflows.md
      - Materials data models: tutorials/materials-data-models.md
  - Troubleshooting:
      - Overview: troubleshooting/index.md
      - Instrument issues: troubleshooting/instruments.md
      - Software issues: troubleshooting/software.md
      - Data issues: troubleshooting/data.md
      - Escalation: troubleshooting/escalation.md
  - Policies:
      - Overview: policies/index.md
      - Documentation review: policies/documentation-review.md
      - Access policy: policies/access.md
      - Data policy: policies/data.md
```

--

## 7. Central repository: landing page template

Create `docs/index.md`:

```markdown
# AIMD-L Documentation

Welcome to the AIMD-L documentation portal.

This site contains authoritative documentation for laboratory operations, safety, instruments, software, data management, and reproducible computational workflows.

## Start here

- New users: begin with [Onboarding](onboarding/index.md).
- Instrument users: begin with [Instruments](instruments/index.md).
- Computational users: begin with [Tutorials](tutorials/index.md).
- Safety-critical operations: begin with [Safety](safety/index.md).

## Documentation types

| Type | Purpose | Primary renderer |
| --- | --- | --- |
| SOPs | Step-by-step operating procedures | Material for MkDocs |
| Instrument manuals | Access, operation, calibration, troubleshooting | Material for MkDocs |
| Data-management guides | Metadata, identifiers, storage, publication | Material for MkDocs |
| Reproducible tutorials | Executable analysis workflows | Jupyter Book / MyST |
| Technical reports | Computed figures, notebooks, equations, citations | Jupyter Book / MyST |

## Ownership

Every maintained page should have an owner, reviewer, and review cadence. See [Documentation governance](about/governance.md).
```

--

## 8. Page metadata convention

Every maintained operational page should begin with YAML front matter.

Example:

```yaml
---
title: MAXIMA startup procedure
status: active
owner_team: maxima-team
primary_contact: TBD
reviewers:
  - maxima-team
  - lab-safety-team
last_reviewed: 2026-06-01
review_cycle: 6 months
applies_to:
  - MAXIMA
  - X-ray operations
safety_level: safety-critical
---
```

Recommended `status` values:

```text
active
needs-review
draft
deprecated
archived
```

Recommended `safety_level` values:

```text
informational
operational
safety-critical
restricted
```

--

## 9. Instrument metadata YAML schema

Create one YAML file per instrument under:

```text
metadata/instruments/
```

Example schema:

```yaml
id: instrument-id
name: Human-readable instrument name
short_name: Short label
status: active
summary: One-paragraph instrument description.
location: Building / room / bay
owner_team: github-team-or-local-team-name
technical_leads:
  - name: TBD
    email: TBD
safety_contacts:
  - name: TBD
    email: TBD
repositories:
  docs: https://github.com/AIMD-L/example-docs
  control_software: null
  analysis_software: null
docs:
  mkdocs_path: docs/instruments/example/
  public_url: https://docs.aimdl.jhu.edu/instruments/example/
  edit_url: https://github.com/AIMD-L/aimdl-docs/edit/main/docs/instruments/example/index.md
review:
  cadence: 6 months
  last_reviewed: null
  next_review_due: null
access:
  requires_training: true
  requires_safety_approval: true
  access_request_url: null
safety:
  hazards:
    - TBD
  ppe:
    - TBD
  emergency_shutdown: TBD
related_tutorials:
  - title: Example computational tutorial
    url: https://docs.aimdl.jhu.edu/tutorials/example/
```

--

## 10. Example instrument YAML: MAXIMA

Create `metadata/instruments/maxima.yml`:

```yaml
id: maxima
name: MAXIMA
short_name: MAXIMA
status: active
summary: >
  MAXIMA is an AIMD-L instrument platform for automated materials experiments
  involving X-ray operations, robotic/sample handling workflows, and associated
  data acquisition and analysis pipelines.
location: TBD
owner_team: maxima-team
technical_leads:
  - name: TBD
    email: TBD
safety_contacts:
  - name: TBD
    email: TBD
repositories:
  docs: https://github.com/AIMD-L/maxima-sop
  control_software: null
  analysis_software: null
docs:
  mkdocs_path: docs/instruments/maxima/
  public_url: https://docs.aimdl.jhu.edu/instruments/maxima/
  edit_url: https://github.com/AIMD-L/aimdl-docs/edit/main/docs/instruments/maxima/index.md
review:
  cadence: 6 months
  last_reviewed: null
  next_review_due: null
access:
  requires_training: true
  requires_safety_approval: true
  access_request_url: null
safety:
  hazards:
    - X-ray radiation
    - Robotic motion
    - Electrical equipment
    - Moving stages and pinch points
  ppe:
    - Safety glasses as required by lab policy
    - Instrument-specific PPE as specified in the SOP
  emergency_shutdown: docs/instruments/maxima/emergency-shutdown.md
related_tutorials:
  - title: Querying MAXIMA experiment data
    url: https://docs.aimdl.jhu.edu/tutorials/maxima-data-query/
  - title: Reproducing MAXIMA analysis outputs
    url: https://docs.aimdl.jhu.edu/tutorials/maxima-analysis/
```

--

## 11. Example instrument YAML: AMDEE XRD

Create `metadata/instruments/amdee-xrd.yml`:

```yaml
id: amdee-xrd
name: AMDEE XRD
short_name: AMDEE XRD
status: active
summary: >
  AMDEE XRD documentation covers access, sample preparation, diffraction
  measurement procedures, calibration, data management, and downstream analysis
  workflows for X-ray diffraction data.
location: TBD
owner_team: xrd-team
technical_leads:
  - name: TBD
    email: TBD
safety_contacts:
  - name: TBD
    email: TBD
repositories:
  docs: https://github.com/AIMD-L/amdee-xrd-docs
  control_software: null
  analysis_software: null
docs:
  mkdocs_path: docs/instruments/amdee-xrd/
  public_url: https://docs.aimdl.jhu.edu/instruments/amdee-xrd/
  edit_url: https://github.com/AIMD-L/aimdl-docs/edit/main/docs/instruments/amdee-xrd/index.md
review:
  cadence: 6 months
  last_reviewed: null
  next_review_due: null
access:
  requires_training: true
  requires_safety_approval: true
  access_request_url: null
safety:
  hazards:
    - X-ray radiation
    - High voltage equipment
    - Moving goniometer or sample stages
  ppe:
    - Safety glasses as required by lab policy
    - Instrument-specific PPE as specified in the SOP
  emergency_shutdown: docs/instruments/amdee-xrd/emergency-shutdown.md
related_tutorials:
  - title: Reproducible XRD reduction with pyFAI
    url: https://docs.aimdl.jhu.edu/tutorials/xrd-pyfai/
  - title: XRD metadata and file-format handling
    url: https://docs.aimdl.jhu.edu/tutorials/xrd-metadata/
```

--

## 12. Example instrument YAML: Laser Shock

Create `metadata/instruments/laser-shock.yml`:

```yaml
id: laser-shock
name: Laser Shock Laboratory
short_name: Laser Shock
status: active
summary: >
  Laser Shock documentation covers safe operation, experiment setup, sample
  preparation, diagnostics, data capture, and computational workflows associated
  with laser shock experiments.
location: TBD
owner_team: laser-shock-team
technical_leads:
  - name: TBD
    email: TBD
safety_contacts:
  - name: TBD
    email: TBD
repositories:
  docs: https://github.com/AIMD-L/laser-shock-docs
  control_software: null
  analysis_software: null
docs:
  mkdocs_path: docs/instruments/laser-shock/
  public_url: https://docs.aimdl.jhu.edu/instruments/laser-shock/
  edit_url: https://github.com/AIMD-L/aimdl-docs/edit/main/docs/instruments/laser-shock/index.md
review:
  cadence: 6 months
  last_reviewed: null
  next_review_due: null
access:
  requires_training: true
  requires_safety_approval: true
  access_request_url: null
safety:
  hazards:
    - Laser exposure
    - High-energy optical systems
    - Projectile or fragment hazards
    - Electrical equipment
    - Acoustic or pressure hazards
  ppe:
    - Laser safety eyewear appropriate to the system wavelength and OD
    - Additional PPE as specified in the approved SOP
  emergency_shutdown: docs/instruments/laser-shock/emergency-shutdown.md
related_tutorials:
  - title: Laser shock data reduction
    url: https://docs.aimdl.jhu.edu/tutorials/laser-shock-data-reduction/
  - title: Laser shock metadata model
    url: https://docs.aimdl.jhu.edu/tutorials/laser-shock-metadata/
```

--

## 13. Example instrument YAML: Robotics

Create `metadata/instruments/robotics.yml`:

```yaml
id: robotics
name: AIMD-L Robotics and Automation Systems
short_name: Robotics
status: active
summary: >
  Robotics documentation covers safe operation, task programming, sample
  handling, robot workcell access, interlocks, emergency stops, and data capture
  from automated laboratory workflows.
location: TBD
owner_team: robotics-team
technical_leads:
  - name: TBD
    email: TBD
safety_contacts:
  - name: TBD
    email: TBD
repositories:
  docs: https://github.com/AIMD-L/robotics-docs
  control_software: null
  analysis_software: null
docs:
  mkdocs_path: docs/instruments/robotics/
  public_url: https://docs.aimdl.jhu.edu/instruments/robotics/
  edit_url: https://github.com/AIMD-L/aimdl-docs/edit/main/docs/instruments/robotics/index.md
review:
  cadence: 6 months
  last_reviewed: null
  next_review_due: null
access:
  requires_training: true
  requires_safety_approval: true
  access_request_url: null
safety:
  hazards:
    - Robotic motion
    - Pinch points
    - Unexpected startup
    - Moving samples or tooling
    - Electrical equipment
  ppe:
    - Safety glasses as required by lab policy
    - Closed-toe shoes
    - Additional PPE as specified in the workcell SOP
  emergency_shutdown: docs/instruments/robotics/emergency-shutdown.md
related_tutorials:
  - title: Robot-run metadata capture
    url: https://docs.aimdl.jhu.edu/tutorials/robot-metadata-capture/
  - title: Automation workflow logging
    url: https://docs.aimdl.jhu.edu/tutorials/automation-logs/
```

--

## 14. Instrument documentation folder template

For each instrument, use the same folder pattern.

Example for MAXIMA:

```text
docs/instruments/maxima/
  index.md
  access.md
  safety.md
  startup.md
  shutdown.md
  calibration.md
  measurement.md
  data-capture.md
  troubleshooting.md
  emergency-shutdown.md
  maintenance.md
  reference.md
```

Recommended `docs/instruments/maxima/index.md`:

```markdown
--
title: MAXIMA
status: active
owner_team: maxima-team
primary_contact: TBD
reviewers:
  - maxima-team
  - lab-safety-team
last_reviewed: null
review_cycle: 6 months
safety_level: operational
--

# MAXIMA

MAXIMA is an AIMD-L instrument platform for automated materials experiments.

## Required reading

1. [Access](access.md)
2. [Safety](safety.md)
3. [Startup](startup.md)
4. [Shutdown](shutdown.md)
5. [Emergency shutdown](emergency-shutdown.md)

## Common tasks

| Task | Page |
| --- | --- |
| Request access | [Access](access.md) |
| Start the system | [Startup](startup.md) |
| Shut down the system | [Shutdown](shutdown.md) |
| Troubleshoot an error | [Troubleshooting](troubleshooting.md) |
| Find data outputs | [Data capture](data-capture.md) |

## Related computational tutorials

- [Querying MAXIMA experiment data](../../tutorials/maxima-data-query.md)
- [Reproducing MAXIMA analysis outputs](../../tutorials/maxima-analysis.md)

## Ownership

- Owner team: `maxima-team`
- Primary contact: TBD
- Review cadence: 6 months
```

--

## 15. CODEOWNERS example

Create `.github/CODEOWNERS`:

```text
# Default documentation stewards
* @AIMD-L/docs-stewards

# Safety-critical content
/docs/safety/ @AIMD-L/lab-safety-team @AIMD-L/docs-stewards
/docs/instruments/*/safety.md @AIMD-L/lab-safety-team
/docs/instruments/*/emergency-shutdown.md @AIMD-L/lab-safety-team

# Instrument teams
/docs/instruments/maxima/ @AIMD-L/maxima-team
/docs/instruments/amdee-xrd/ @AIMD-L/xrd-team
/docs/instruments/laser-shock/ @AIMD-L/laser-shock-team
/docs/instruments/robotics/ @AIMD-L/robotics-team

# Software and data infrastructure
/docs/software/ @AIMD-L/software-team
/docs/data-management/ @AIMD-L/data-team

# Computational tutorials
/docs/tutorials/ @AIMD-L/tutorials-team @AIMD-L/data-team

# Repository metadata and CI
/mkdocs.yml @AIMD-L/docs-stewards
/requirements.txt @AIMD-L/docs-stewards
/.github/workflows/ @AIMD-L/docs-stewards
/metadata/ @AIMD-L/docs-stewards
```

Branch protection should require pull request review from code owners before merging into `main`.

--

## 16. GitHub Actions: MkDocs CI

Create `.github/workflows/ci.yml`:

```yaml
name: Validate documentation

on:
  pull_request:
  push:
    branches:
      - main

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install documentation dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Build MkDocs site strictly
        run: mkdocs build --strict
```

--

## 17. GitHub Actions: MkDocs deployment to GitHub Pages

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy documentation

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install documentation dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Deploy to GitHub Pages
        run: mkdocs gh-deploy --force
```

For a custom domain such as `docs.aimdl.jhu.edu`, configure the GitHub Pages custom domain in repository settings and coordinate DNS with the appropriate JHU IT process.

--

## 18. Multi-repository assembly model

If AIMD-L wants multiple team-owned repositories feeding a single central site, use a central assembly repository with one of the following approaches.

### 18.1 Approach 1: GitHub Actions checkout of external repositories

Example central build workflow:

```yaml
name: Build assembled documentation

on:
  pull_request:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Check out central documentation site
        uses: actions/checkout@v4
        with:
          path: site

      - name: Check out MAXIMA documentation
        uses: actions/checkout@v4
        with:
          repository: AIMD-L/maxima-sop
          path: site/external/maxima-sop

      - name: Check out AMDEE XRD documentation
        uses: actions/checkout@v4
        with:
          repository: AIMD-L/amdee-xrd-docs
          path: site/external/amdee-xrd-docs

      - name: Check out laser shock documentation
        uses: actions/checkout@v4
        with:
          repository: AIMD-L/laser-shock-docs
          path: site/external/laser-shock-docs

      - name: Check out robotics documentation
        uses: actions/checkout@v4
        with:
          repository: AIMD-L/robotics-docs
          path: site/external/robotics-docs

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        working-directory: site
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Build assembled site
        working-directory: site
        run: mkdocs build --strict
```

If external repositories are private, configure an access token or GitHub App with read access to those repositories.

### 18.2 Approach 2: Git submodules

A central repository may include team documentation repositories as submodules:

```text
aimdl-docs-site/
  external/
    maxima-sop/             # git submodule
    amdee-xrd-docs/         # git submodule
    laser-shock-docs/       # git submodule
```

This gives reproducible pinned versions of each team repo, but submodules add workflow complexity for contributors.

--

## 19. MkDocs monorepo plugin example

If using `mkdocs-monorepo-plugin`, the central `mkdocs.yml` can include navigation from team repositories.

Central `mkdocs.yml`:

```yaml
site_name: AIMD-L Documentation
site_url: https://docs.aimdl.jhu.edu/

theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.indexes
    - search.highlight
    - content.action.edit
    - content.code.copy

plugins:
  - search
  - monorepo

nav:
  - Home: index.md
  - Safety:
      - Overview: safety/index.md
      - X-ray safety: safety/xray.md
      - Laser safety: safety/laser.md
      - Robotics safety: safety/robotics.md
  - Instruments:
      - Overview: instruments/index.md
      - MAXIMA: '!include ./external/maxima-sop/mkdocs.yml'
      - AMDEE XRD: '!include ./external/amdee-xrd-docs/mkdocs.yml'
      - Laser Shock: '!include ./external/laser-shock-docs/mkdocs.yml'
      - Robotics: '!include ./external/robotics-docs/mkdocs.yml'
  - Software: software/index.md
  - Data management: data-management/index.md
  - Tutorials: tutorials/index.md
```

Team repository `mkdocs.yml` example for MAXIMA:

```yaml
site_name: MAXIMA Documentation

docs_dir: docs

nav:
  - Overview: index.md
  - Access: access.md
  - Safety: safety.md
  - Startup: startup.md
  - Shutdown: shutdown.md
  - Calibration: calibration.md
  - Measurement: measurement.md
  - Data capture: data-capture.md
  - Troubleshooting: troubleshooting.md
  - Emergency shutdown: emergency-shutdown.md
  - Reference: reference.md
```

Important rule: team `mkdocs.yml` files used for inclusion should focus on local navigation. The central site should own global theme, plugins, site URL, analytics, and top-level navigation.

--

## 20. Jupyter Book / MyST tutorial repository

Recommended repository name:

```text
aimdl-tutorials
```

Recommended structure:

```text
aimdl-tutorials/
  README.md
  myst.yml
  requirements.txt
  environment.yml
  .github/
    workflows/
      ci.yml
      deploy.yml
  tutorials/
    index.md
    xrd-analysis/
      index.md
      pyfai-reduction.ipynb
      metadata-validation.md
    girder-query/
      index.md
      query-examples.ipynb
    dagster-workflows/
      index.md
      run-workflow.md
      inspect-results.ipynb
    materials-data-models/
      index.md
      gemd-example.ipynb
  data/
    README.md
```

Recommended policy: tutorials should use small public or synthetic example data by default. Large or restricted datasets should be referenced through stable identifiers, access instructions, or data services rather than committed directly to the repository.

---

## 21. Jupyter Book / MyST `myst.yml` example

Create `myst.yml`:

```yaml
version: 1

project:
  title: AIMD-L Reproducible Tutorials
  description: Executable computational tutorials for AIMD-L data, analysis, and workflow examples.
  keywords:
    - AIMD-L
    - materials data
    - reproducible workflows
    - Jupyter Book
    - MyST
  authors:
    - name: AIMD-L contributors
  github: AIMD-L/aimdl-tutorials
  license: CC-BY-4.0

site:
  template: book-theme
  options:
    logo: assets/images/aimdl-logo.svg
    favicon: assets/images/favicon.ico
```

If using an older Sphinx-based Jupyter Book stack instead of the current MyST-oriented stack, use `_config.yml` and `_toc.yml` rather than `myst.yml`. For new work, prefer the current MyST-oriented configuration unless there is a compatibility reason not to.

--

## 22. Jupyter Book / MyST tutorial index page

Create `tutorials/index.md` in the Jupyter Book repository:

```markdown
# AIMD-L Reproducible Tutorials

This site contains executable tutorials and computational examples for AIMD-L workflows.

Each tutorial should include:

- scientific or operational purpose;
- required software environment;
- required input data;
- expected outputs;
- approximate runtime;
- provenance and citation information;
- responsible team and review cadence.

## Tutorial categories

- XRD and diffraction analysis
- Girder / DMS data access
- Dagster workflow execution
- Materials data models
- Metadata validation
- Figure reproduction
```

--

## 23. Tutorial metadata template

Every computational tutorial should include front matter similar to this:

```yaml
---
title: Reproducible XRD reduction with pyFAI
status: draft
owner_team: xrd-team
primary_contact: TBD
reviewers:
  - xrd-team
  - data-team
last_reviewed: null
review_cycle: 6 months
execution:
  tested: false
  expected_runtime: TBD
  kernel: python3
  requires_gpu: false
  requires_network: false
data:
  data_access: example-data
  data_url: null
  data_doi: null
  restricted: false
environment:
  file: environment.yml
  python: '3.11'
--
```

--

## 24. Jupyter tutorial environment example

Create `environment.yml`:

```yaml
name: aimdl-tutorials
channels:
  - conda-forge
dependencies:
  - python=3.11
  - pip
  - numpy
  - scipy
  - pandas
  - matplotlib
  - jupyterlab
  - ipykernel
  - pip:
      - jupyter-book
      - mystmd
      - girder-client
      - pyFAI
```

Adjust packages per tutorial. Avoid a single heavyweight environment if tutorials diverge significantly; use per-tutorial environment files when necessary.

--

## 25. Jupyter Book / MyST CI example

Create `.github/workflows/ci.yml` in `aimdl-tutorials`:

```yaml
name: Validate tutorials

on:
  pull_request:
  push:
    branches:
      - main

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Start Jupyter Book without execution
        run: jupyter book start --ci
```

For tutorials that should be executed in CI, add a separate scheduled workflow or protected branch workflow that runs with execution enabled. Do not execute expensive or data-sensitive notebooks on every pull request unless the runtime and data-access model are controlled.

Example execution check:

```yaml
name: Execute tutorial notebooks

on:
  workflow_dispatch:
  schedule:
    - cron: '0 7 * * 1'

permissions:
  contents: read

jobs:
  execute:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Execute tutorials
        run: jupyter book start --execute --ci
```

Review the exact build/deploy command against the Jupyter Book/MyST version AIMD-L standardizes on. The important policy decision is that notebooks should have explicit execution rules rather than ad hoc execution by individual authors.

--

## 26. Connecting MkDocs portal to Jupyter Book tutorials

There are three practical ways to connect the central portal and tutorial books.

### Option 1: link to the tutorial site

Main site:

```text
https://docs.aimdl.jhu.edu/tutorials/
```

Tutorial book:

```text
https://tutorials.aimdl.jhu.edu/
```

The MkDocs tutorials page links to each Jupyter Book tutorial.

This is the lowest-friction approach.

### Option 2: publish Jupyter Book under a subpath

Main site:

```text
https://docs.aimdl.jhu.edu/
```

Tutorial book:

```text
https://docs.aimdl.jhu.edu/tutorials/
```

This requires deployment coordination so that MkDocs output and Jupyter Book output are copied into one final static artifact.

### Option 3: central landing page plus separate books by topic

```text
https://docs.aimdl.jhu.edu/tutorials/
https://docs.aimdl.jhu.edu/tutorials/xrd/
https://docs.aimdl.jhu.edu/tutorials/girder/
https://docs.aimdl.jhu.edu/tutorials/dagster/
```

This works well if tutorial collections become large enough to deserve separate ownership.

Recommended initial choice: **Option 1**. Move to Option 2 only after the team has a stable deployment process.

--

## 27. Documentation governance

### 27.1 Required roles

Each content area should have:

```text
owner_team
primary_contact
reviewers
review_cycle
last_reviewed
status
```

### 27.2 Review classes

Recommended review classes:

```text
Safety-critical: review at least every 6 months or after equipment/procedure change
Operational: review every 6-12 months
Reference: review annually
Tutorial: review when software/data dependencies change, at least annually
Archived: no routine review, clearly marked as archived
```

### 27.3 Pull request policy

Recommended branch protection for `main`:

- Require pull request before merge.
- Require status checks to pass.
- Require code owner review.
- Require conversation resolution.
- Disallow direct pushes except for repository administrators.

### 27.4 Staleness policy

Pages should be marked `needs-review` when:

- the instrument changed;
- the software interface changed;
- safety procedures changed;
- a tutorial no longer executes;
- a linked data source moved;
- the review date has expired.

---

## 28. Initial implementation plan

### Phase 1: central portal prototype

1. Create `AIMD-L/aimdl-docs`.
2. Add `mkdocs.yml`, `requirements.txt`, and initial `docs/` tree.
3. Add `CODEOWNERS` and GitHub Actions CI.
4. Create placeholder instrument sections.
5. Add metadata YAML files for each initial instrument.
6. Deploy to GitHub Pages.
7. Configure custom domain after the prototype works.

### Phase 2: instrument content ownership

1. Assign owner teams.
2. Populate each instrument `index.md`.
3. Add access, safety, startup, shutdown, troubleshooting, and emergency shutdown pages.
4. Require code owner review for safety-critical sections.
5. Add review dates and status metadata.

### Phase 3: computational tutorials

1. Create `AIMD-L/aimdl-tutorials`.
2. Add `myst.yml`, `environment.yml`, and starter tutorial pages.
3. Add at least one small, executable tutorial using synthetic or public example data.
4. Decide whether tutorials are built without execution on every PR and executed on a schedule.
5. Link tutorial outputs from the central MkDocs portal.

### Phase 4: multi-repository assembly, if needed

1. Decide whether instrument teams need independent repositories.
2. If yes, move instrument sections to team-owned repositories.
3. Add central checkout or submodule strategy.
4. Add `mkdocs-monorepo-plugin` if central navigation merging is required.
5. Validate all external repositories before deployment.

--

## 29. Minimum viable repository checklist

For `aimdl-docs`:

```text
[ ] Repository created
[ ] `mkdocs.yml` added
[ ] `requirements.txt` added
[ ] `docs/index.md` added
[ ] `docs/safety/index.md` added
[ ] `docs/instruments/index.md` added
[ ] Instrument placeholder pages added
[ ] Metadata YAML files added
[ ] CODEOWNERS added
[ ] CI workflow added
[ ] Deployment workflow added
[ ] GitHub Pages enabled
[ ] Custom domain decision made
```

For `aimdl-tutorials`:

```text
[ ] Repository created
[ ] `myst.yml` added
[ ] `requirements.txt` or `environment.yml` added
[ ] Tutorial index added
[ ] First executable tutorial added
[ ] CI workflow added
[ ] Execution policy documented
[ ] Linked from central MkDocs portal
```

--

## 30. References

- Material for MkDocs documentation: https://squidfunk.github.io/mkdocs-material/
- MkDocs deployment documentation: https://www.mkdocs.org/user-guide/deploying-your-docs/
- Jupyter Book documentation: https://jupyterbook.org/
- Jupyter Book executable content documentation: https://jupyter-book.readthedocs.io/docs/execution/execution/
- Jupyter Book project initialization and `myst.yml`: https://jupyter-book.readthedocs.io/docs/get-started/init/
- GitHub CODEOWNERS documentation: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- GitHub Actions checkout: https://github.com/actions/checkout
- MkDocs monorepo plugin: https://backstage.github.io/mkdocs-monorepo-plugin/

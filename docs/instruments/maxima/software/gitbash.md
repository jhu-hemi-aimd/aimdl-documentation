---
title: Git Bash
status: needs-review
owner_team: maxima-team
primary_contact: Harrison Park
reviewers:
  - maxima-team
last_reviewed: null
review_cycle: 12 months
safety_level: informational
---

# Git Bash

**Relevant to:** All operators on the MAXIMA Windows control PC  

---

## Overview

Git Bash is a Windows package that installs **Bash** (the Bourne Again Shell), common Unix
command-line utilities, and Git onto Windows. For MAXIMA purposes, Git Bash is used primarily
as a terminal for interfacing with Docker containers and running instrument control commands.

Git Bash can be downloaded from:

```
https://git-scm.com/downloads/win
```

---

## Basic Navigation Reference

| Command | Meaning | Example |
|---------|---------|---------|
| `cd <path>` | Change directory | `cd aimdrc/src/api/apps/controller` |
| `cd ~` | Go to home directory | — |
| `pwd` | Print current working directory | — |
| `ls` | List files in the current directory | — |
| `echo <text>` | Print text or variable to terminal | `echo ~` |
| `~` | Shorthand for the home directory | `cd ~/Documents` |

---

## Startup Sequence

The following commands are run in sequence each time you start a MAXIMA session.
See [Startup Procedure](../procedures/startup.md) for context and a pre-start checklist.

```bash
# 1. Go to home directory
cd ~

# 2. Navigate to the controller directory
cd aimdrc/src/api/apps/controller

# 3. Open an interactive session in the aimdrc Docker container
winpty docker exec -it --user aimdrc aimdrc bash

# 4. (Inside container) Activate the Python virtual environment
. venv/bin/activate

# 5. (Inside container) Launch the Django management shell
./src/api/manage.py shell
```

---

## Common Issues

**`winpty` command not found:**  
Git Bash should include `winpty` by default. If it is missing, reinstall Git Bash and confirm
the full package (including Unix tools) is selected during installation.

**`cd aimdrc/src/api/apps/controller` fails with "no such file or directory":**  
Confirm you are starting from the home directory (`cd ~` first). The `aimdrc` directory should
be present in your home directory on the MAXIMA control PC.

**`docker exec` returns "No such container: aimdrc":**  
Docker Desktop is either not running or the `aimdrc` container has not been started. See
[Docker](docker.md) for diagnosis steps.

**`venv/bin/activate` not found inside the container:**  
The virtual environment path may differ. Run `ls` inside the container to confirm the directory
structure, or contact Eric Walker or Harrison Park.

---

## Changelog

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0 | March 2025 | Harrison Park | Initial draft |

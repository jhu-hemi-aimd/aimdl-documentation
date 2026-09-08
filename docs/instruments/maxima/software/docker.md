---
title: Docker
status: needs-review
owner_team: maxima-team
primary_contact: Harrison Park
reviewers:
  - maxima-team
last_reviewed: null
review_cycle: 12 months
safety_level: informational
---

# Docker

**Relevant to:** All operators setting up the MAXIMA control software stack  

---

## Overview

Docker is a containerization platform that runs isolated, reproducible software environments
called **containers**. Each container behaves like a self-contained mini-computer — it has its
own filesystem, dependencies, and processes, and cannot interfere with the host system or other
containers.

MAXIMA's instrument control software runs inside a container called `aimdrc`. This approach
ensures that the control environment is consistent across machines and easy to recreate from
the `Dockerfile`. All data processing tools (Dagster, PyFAI, PyMCA) also run in containerized
environments, enabling reproducible execution and isolation, as described in the MAXIMA
publication (Park et al., 2025, arXiv:2511.14905).

---

## Installation

Docker Desktop for Windows can be downloaded from:

```
https://www.docker.com/products/docker-desktop/
```

Install it and ensure it starts automatically at login, or remember to launch it manually before
each session.

---

## Starting Docker Desktop

1. Open **Docker Desktop** from the Windows start menu.
2. Wait for Docker to reach a **running** state — the whale icon in the system tray should turn
   green and the dashboard should show containers.
3. Do not proceed with Git Bash steps until Docker is fully running.

---

## The `aimdrc` Container

The `aimdrc` container is the primary environment for controlling MAXIMA. It contains:

- The AIMDRC instrument control API (Django-based)
- The Python virtual environment with all required dependencies
- The correct user permissions (`aimdrc` user) to interface with the instrument

### Starting the Container Session

The following command, run from Git Bash, opens an interactive terminal session inside the
container:

```bash
winpty docker exec -it --user aimdrc aimdrc bash
```

#### Command Breakdown

| Token | Meaning |
|-------|---------|
| `winpty` | Windows Pseudoterminal wrapper. Required because Windows lacks native support for interactive terminal processes. Systems after 2019 have `conpty` as a native alternative, but `winpty` is used here for reliability. |
| `docker exec` | Execute a command inside a running Docker container |
| `-i` | Interactive — keeps STDIN open so you can type into the session |
| `-t` | TTY — allocates a pseudo-terminal, making the session behave like a normal terminal |
| `-it` | Combination of `-i` and `-t` |
| `--user aimdrc` | Run the session as the `aimdrc` user. This user has the correct filesystem permissions to operate MAXIMA. |
| `aimdrc` | The name of the Docker container to exec into |
| `bash` | Launch a Bash shell inside the container |

**In summary:** Opens an interactive Bash terminal inside the `aimdrc` container, authenticated
as the `aimdrc` user, with a proper TTY so the session behaves like a normal terminal.

---

## Useful Docker Commands

These are run from Git Bash (outside the container), for diagnostics and management:

| Command | Purpose |
|---------|---------|
| `docker ps` | List all currently running containers |
| `docker ps -a` | List all containers, including stopped ones |
| `docker logs aimdrc` | View the output log of the `aimdrc` container |
| `docker restart aimdrc` | Restart the container |
| `docker inspect aimdrc` | Show full container configuration details |

---

## Troubleshooting

**Container is not running (`docker exec` fails):**  
Run `docker ps` to check status. If `aimdrc` is not in the list, the container may need to be
started. Run `docker start aimdrc` and try again.

**"Error response from daemon: Cannot connect to the Docker daemon":**  
Docker Desktop is not running. Launch it and wait for it to fully initialize before retrying.

**Permission denied inside the container:**  
Ensure you are running `--user aimdrc` in your exec command. The default Docker user may not
have the required permissions.

---

## Changelog

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0 | March 2025 | Harrison Park | Initial draft |

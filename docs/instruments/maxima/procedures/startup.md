---
title: MAXIMA manual startup
status: needs-review
owner_team: maxima-team
primary_contact: Harrison Park
reviewers:
  - maxima-team
last_reviewed: null
review_cycle: 6 months
safety_level: operational
---

# Startup Procedure

**Relevant to:** All operators running experiments on MAXIMA  
**Prerequisites:** Read [Safety Procedures](../safety.md) before proceeding.

---

## Overview

While MAXIMA is meant to be an automated device run through AIMD-L's run manager, there are instances in which this is infeasible. The run manager can go down, or there are simply checks that are easier to run manually. Accessing the MAXIMA controller manually through GitBash enables us to run MAXIMA this way. 

Starting MAXIMA requires launching the instrument control software stack in the correct order.
The control system runs inside a Docker container (`aimdrc`) on the MAXIMA control PC. Git Bash
is used to interface with that container from Windows.

For detailed explanations of each tool (Docker, Git Bash, the container commands), see
[Docker](../software/docker.md).

---

## Pre-Start Checklist

Before launching any software, confirm the following physical conditions:

- [ ] Second person present (buddy system — see [Safety](../safety.md))
- [ ] Auto-door is **closed**
- [ ] Warning light state is as expected (all off for now, X-ray ready) 
- [ ] Machine calibration is scheduled if this is first startup of the day (see [Calibration](calibration.md))

---

## Step 1: Launch Docker Desktop

Open **Docker Desktop** from the Windows start menu and wait for it to fully initialize.
The Docker icon in the system tray should show a green "running" state before proceeding.

> If Docker fails to start, restart the application. If the issue persists, restart the control PC
> and try again before contacting support.

---

## Step 2: Open Git Bash

Open **Git Bash** from the Windows start menu or desktop shortcut.

Confirm you are in the home directory:

```bash
echo ~
```

This should print something like `/c/Users/aimdrc` or similar. If not, navigate there:

```bash
cd ~
```

---

## Step 3: Navigate to the Controller Directory

```bash
cd aimdrc/src/api/apps/controller
```

---

## Step 4: Start the AIMDRC Container

```bash
winpty docker exec -it --user aimdrc aimdrc bash
```

This opens an interactive Bash session inside the `aimdrc` Docker container with the correct user
permissions. See [Docker](../software/docker.md) for a full breakdown of what each token in this
command means.

---

## Step 5: Activate the Python Virtual Environment

Inside the container:

```bash
. venv/bin/activate
```

The prompt should change to indicate the virtual environment is active (typically a `(venv)` prefix).

---

## Step 6: Launch the Django Shell

```bash
./src/api/manage.py shell
```

This opens an interactive Python shell within the Django application context, from which you can
import the `Controller` class and run experiments.

---

## Step 7: Verify Readiness

You should now have an active Python shell. You can verify the controller is importable:

```python
from apps.controller.controller import Controller
controller = Controller()
```

If this completes without errors, the system is ready.

> If you see import errors or connection failures, the most common cause is that Docker Desktop
> was not fully initialized before starting the container. Exit, restart Docker Desktop, and repeat
> from Step 4.

---

## Next Steps

- If this is the first startup of the day, proceed to **[Machine Calibration](calibration.md#machine-calibration)** before running any experiments.
- To run an experiment, see **[Running an Experiment](experiment.md)**.


Run scripts in MAXIMA are slightly different in running it manually vs. running it through the run manager. Refer to documentation on run scripts to ensure you are using the correct version. 

---

## Changelog

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0 | March 2025 | Harrison Park | Initial draft |

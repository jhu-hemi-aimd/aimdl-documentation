---
title: "Software setup"
status: needs-review
owner_team: software-team
primary_contact: null
last_reviewed: null
review_cycle: 6 months
safety_level: operational
tags: [software, controls]
---

# Software setup

Deploy the central services and then install AIMDRC with the appropriate controller on each station host. These instructions consolidate the supplied READMEs and build files. Hostnames, network routes, credentials, vendor installations and physical commissioning remain deployment-specific.

## Prerequisites and sequence

1. Provision the database service (`aimddb`) and required network/DNS/TLS infrastructure. Its repository is not supplied, so database-host installation is outside this source set.
2. Prepare [central services](services.md): AIMDAS, then AIMDDS, then AIMDRM, matching the order assumed by their READMEs.
3. Install [station clients and controllers](stations.md), including vendor dependencies and device/data mounts.
4. Confirm authentication, service reachability, station namespace/certificates, live status and persistent data paths before submitting an approved experiment.

The original local examples assume the Docker bridge assigns `.2` to the database, `.3` to AIMDAS, `.4` to AIMDDS and `.5` to AIMDRM on `172.17.0.0/16`. Docker does not guarantee those assignments on an arbitrary host. Inspect actual networking and update name mappings consistently.

## Configuration boundaries

| Configuration | Where it belongs |
| --- | --- |
| Local versus production service settings | `src/api/config/settings/main.py` symlink to `local.py` or `prod.py` |
| API addresses, service secrets, database credentials | Service settings and protected environment file |
| Station name, OPC UA certificates/private key | AIMDRC selected settings module |
| Controller selection | AIMDRC `CONTROLLER_CLASS_PATH` and installed `apps/controller/` |
| Device addresses, camera serials, calibration and limits | Controller subsystem constants/configuration |
| Experiment choices | Versioned JSON run script |
| Stored artifacts | Explicit persistent bind mounts/volumes and vendor data directories |

Do not copy credentials from a README into documentation or version control. The supplied MAXIMA README includes a share password; use deployment-managed credentials instead. No credentials are reproduced here.

## Smoke checks

* AIMDAS serves the application and can authenticate to AIMDDS.
* AIMDDS can reach PostgreSQL, its data portal and AIMDRM; its migrations and initial service users exist.
* AIMDRM has a healthy OPC UA server and robotics session; the browser receives system state.
* Each intended AIMDRC reports the correct logical station, certificate identity and heartbeat.
* Controller dependencies import inside the built image; hardware connections are commissioned under the instrument procedure.
* Data written from the station remains accessible in the intended persistent location.

These checks verify software wiring. They do not authorize sample motion, radiation or laser operations.

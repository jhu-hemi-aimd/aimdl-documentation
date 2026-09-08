---
title: MAXIMA
status: needs-review
owner_team: maxima-team
primary_contact: Harrison Park
reviewers:
  - maxima-team
  - lab-safety-team
last_reviewed: null
review_cycle: 6 months
safety_level: operational
---

# MAXIMA

MAXIMA (Multi-modal Automated X-ray Investigation of Materials) is the AIMD-L
high-throughput X-ray instrument: transmission-mode XRD with simultaneous XRF in
reflection geometry, robotic sample handling, and the associated acquisition and
analysis pipelines.

!!! warning "Read safety first"
    MAXIMA is a high-energy X-ray instrument. Read [MAXIMA safety](safety.md)
    before any operation, and never operate the instrument alone.

!!! note "Migrated SOP — under review"
    These pages were migrated from the standalone `MAXIMA-SOP` repository
    authored by Harrison Park. They are marked `needs-review`: the content has
    not yet been reviewed under this site's
    [documentation review policy](../../policies/documentation-review.md), and
    several planned pages are still empty. See the
    [changelog](changelog.md) for the SOP's own history and caveats.

## Safety

- [MAXIMA safety](safety.md) — X-ray and robotics safety, indication system, points of contact

## Procedures

- [Manual startup](procedures/startup.md) — launching the control stack via Docker and Git Bash
- [Calibration](procedures/calibration.md) — X-ray and sample-to-detector calibration
- [Sample handling](procedures/sample-handling.md) — coordinate system, mounting, scan points
- [Shutdown](procedures/shutdown.md) — *planned*
- [Running an experiment](procedures/experiment.md) — *planned*

### Design of experiments

- [DOE: HTMAX Ti-V (Rayna)](procedures/doe/rayna-htmax.md)

## Software

- [Docker](software/docker.md) — the `aimdrc` control container
- [Git Bash](software/gitbash.md) — terminal on the Windows control PC
- [Dagster](software/dagster.md) — sensor-driven XRD/XRF processing pipeline
- [PyFAI](software/pyfai.md) — azimuthal integration of XRD data
- [PyMCA](software/pymca.md) — XRF spectral fitting
- [Dectris Albula](software/albula.md) — *planned*
- [OpenMSIStream](software/openmsistream.md) — *planned*

## Reference

- [Run scripts](reference/run-scripts.md) — run-script format, coordinates, detector distance
- [Coordinate system](reference/coordinates.md) — *planned*
- [Detector specifications](reference/detector.md) — *planned*
- [X-ray source](reference/source.md) — *planned*

## Troubleshooting

- [MAXIMA troubleshooting](troubleshooting.md) — known issues, error codes, escalation

## Ownership

- Owner team: `maxima-team`
- Primary contact: Harrison Park
- Review cadence: 6 months

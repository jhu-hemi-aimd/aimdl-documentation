---
title: MAXIMA calibration
status: needs-review
owner_team: maxima-team
primary_contact: Harrison Park
reviewers:
  - maxima-team
last_reviewed: null
review_cycle: 6 months
safety_level: operational
---

# Calibration

**Relevant to:** All operators running experiments on MAXIMA  
**Prerequisites:** [Startup Procedure](startup.md) must be completed before calibration.

---

## Overview

MAXIMA requires two distinct types of calibration before data collection:

1. **X-ray calibration** — aligns and stabilizes the X-ray source (MetalJet). Happens every 24 hours or if X-ray source settings (current, voltage) are changed.
2. **Sample calibration** — establishes the sample-to-detector geometry using known calibrant
   materials placed on the sample holder. At this point in time is done through PyFAI GUI. Gannon Murray's current (March 25, 2026) work is on establishing MAXIMA-ViT, an automated sample-to-detector distance calibration.

Both are required when starting fresh for the day. X-ray calibration is forced at the start of each day, while sample calibration is currently (March 25, 2026) manually controlled. There is no system stopping you from running experiments without calibration. However, sample calibration is, from this date forward (March 25, 2026) required whenever it has been 24 hours since the last calibration, and also when the sample holder or detector are repositioned.
 
---

## Machine Calibration

### When to Perform

Machine calibration of the **Excillum MetalJet E1+** source is required:

- **At the start of every day**, before any X-ray operation
- **After any extended idle period** where X-rays have been off for several hours or more

### Procedure

Machine calibration is performed through the **Excillum software**, not through the AIMDRC
controller. The source self-calibrates once triggered.

1. Open the **X-Collect** software on the control PC.
2. Initiate calibration by turning on the X-ray. X-ray status should switch to "CALIBRATE."
3. Calibration typically completes in **5 minutes**.
4. Do not operate the X-ray shutter or begin experiments until calibration is confirmed complete.

---

## Sample (Detector Geometry) Calibration

### Purpose

Sample calibration uses alumina powder calibrants to determine the beam center position on the
detector and the accurate sample-to-detector distance. This information is used by PyFAI during
azimuthal integration to convert 2D diffraction patterns into 1D intensity profiles. Without
accurate calibration, all downstream `q` or `2θ` values will be incorrect, not to mention peaks might be wider or altogether non-existent.

The calibration workflow in the automated data pipeline performs:
- Correction for detector tilt
- Beam center location
- Sample-to-detector distance calibration

### Calibrant Materials and Positions

**Old system**
The following is a description of the older system used for calibration. 

Alumina (Al₂O₃) calibrant pucks are placed at four cardinal positions on the sample holder.
Their coordinates in the instrument coordinate system are:

| Position | Coordinates `[x, y]` |
|----------|----------------------|
| North    | `[6, 31]`            |
| West     | `[-23, 0]`           |
| South    | `[6, -32]`           |
| East     | `[35, 0]`            |

> **Coordinate convention:** Negative Y values are toward the lab bench (opposite side from
> Joseph's office). See [Sample Handling](sample-handling.md) for the full coordinate system
> description.

This system was dropped due to the difficulty of producing sample holders and calibrants that would reliably show alumina rings. The North-South-West-East system was originally developed to interpolate sample-to-detector distance at any point in the sample. This ended up being difficult due to the lack of sample flatness in most samples, as well as the difficulty in linearly interpolating poni1 and poni2 values, which describe detector tilt away from perpendicular to the X-ray beam. Any results from this era are calibrated using just the North calibrant ([6,31]). 

**Current System**
Currently, we use a single scan of Alumina per dataset. This is due to limitations in our automation, both robotic and computational. However, we are currently (March 25, 2026) in the process of developing new procedures. This is a work in progress. 

### Procedure

PYFAI Explanation: 
See: Software page. 
T
> **TODO:** Add expected output parameter ranges, citation of Gannon's MAXIMA-ViT work.

### Manual Calibration with PyFAI

If the automated pipeline is unavailable, calibration can be performed manually using PyFAI's
`pyFAI-calib2` GUI or the recalibration notebook:

```
https://www.silx.org/doc/pyFAI/dev/usage/tutorial/Recalib/Recalib_notebook.html
```

See [PyFAI](../software/pyfai.md) for installation and usage details.

---

## Re-Calibration Triggers

Re-run sample calibration when any of the following occur:

- The detector is moved to a new distance along the translation stage
- The sample holder is removed and replaced
- Data quality or peak positions appear systematically off
- After a power cycle (note: power cycling can cause a slight timestamp shift — see
  [Troubleshooting](../troubleshooting.md))

---
## Changelog

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0 | March 2025 | Harrison Park | Initial draft |

---
title: MAXIMA sample handling
status: needs-review
owner_team: maxima-team
primary_contact: Harrison Park
reviewers:
  - maxima-team
last_reviewed: null
review_cycle: 6 months
safety_level: operational
---

# Sample Handling

**Relevant to:** All operators loading and running samples on MAXIMA  

---

## Overview

MAXIMA is designed for **high-throughput, transmission-mode XRD** of bulk structural metals and
ceramics, with simultaneous XRF in reflection geometry. Sample handling is fully automated once
a scan script is submitted: a robot arm inside the X-ray enclosure moves the sample to each
programmed scan point.

This document covers the coordinate system, sample mounting, scan point specification, and
important constraints on sample geometry.

---

## Coordinate System

The MAXIMA coordinate system is defined in the plane of the sample holder. Coordinates are given
as `[x, y]` pairs in millimeters.

| Axis | Direction |
|------|-----------|
| +X   | *TODO: confirm direction* |
| −Y   | Toward the lab bench (opposite side from Joseph's office) |
| +Y   | Toward Joseph's office side |

**Sample holder center:** `[6, 0]`

> **TODO:** Add a labeled diagram of the sample holder showing axis directions, center point,
> calibrant positions, and approximate usable area.

---

## Sample Requirements

MAXIMA performs measurements in **transmission geometry**, meaning the X-ray beam passes through
the full thickness of the specimen. This has direct implications for sample preparation:

- **Thickness:** Optimal specimen thickness is approximately **one absorption length** for the
  material being measured at 24 keV. For structural metals, this is typically on the order of
  **100 µm** (e.g., a 100 µm thick steel specimen is practical). Thicker specimens reduce
  transmitted intensity significantly.
- **Surface preparation:** Because XRD measurements are made in transmission through the full
  thickness, **no surface preparation is required** for diffraction data. This is a key
  advantage over surface-sensitive techniques like SEM/EBSD.
- **Spatial resolution:** The focused beam provides a spatial resolution of approximately
  **200 µm**, meaning measurements are localized to that footprint on the sample.
- **Sample size:** *TODO: document maximum sample dimensions and any fixture constraints.*

---

## Sample Mounting

> **TODO:** Document the physical mounting procedure — how samples are fixtured to the sample
> holder, acceptable holder configurations, how to confirm a sample is flat and properly seated.

---

## Scan Point Specification

Scan points are passed to the controller as a list of `[x, y]` coordinates. The robot moves the
sample holder so that each coordinate is centered on the beam in sequence.

Example scan point list:

```python
"scan_points": [
    [3, -2],
    [4, -2],
    [5, -2],
]
```

**Guidelines for planning scan points:**

- Confirm all points fall within the usable area of the sample holder. Points outside the
  physical range will cause a robot fault.
- Sample center is `[6, 0]`. Plan your grid relative to this reference.
- Calibrant positions (`[6, 31]`, `[-23, 0]`, `[6, -32]`, `[35, 0]`) are reserved. Do not
  include these in your sample scan list.
- For combinatorial specimens, a regular rectangular grid is typical. See [Running an
  Experiment](experiment.md) for a full script example.

---

## Sample Removal

> **TODO:** Document safe sample removal procedure after a run is complete — confirm X-rays are
> off, confirm robot has returned to home position, confirm auto-door can be safely opened.

---

## Changelog

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0 | March 2025 | Harrison Park | Initial draft |

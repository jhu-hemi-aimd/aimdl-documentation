---
title: "Example run scripts"
status: needs-review
owner_team: software-team
primary_contact: null
last_reviewed: null
review_cycle: 6 months
safety_level: operational
tags: [software, controls]
---

# Example run scripts

Download these JSON files for syntax and controller-input examples. They are derived from supplied code and `SMHM.json`; confirm device readiness, method files, mounting and experimental parameters before execution.

| File | Purpose |
| --- | --- |
| [maxima.json](maxima.json) | One holder-frame point and combined XRD/XRF collection |
| [helix.json](helix.json) | Three flyer-grid positions, three paired angles, PDV probe 10 |
| [sphinx.json](sphinx.json) | Four holder-frame indentation points using the supplied method path |
| [coord.json](coord.json) | Acquire and publish a sample-to-holder transform |
| [coord-photo-only.json](coord-photo-only.json) | Save images and metadata without a transform |
| [coord-maxima.json](coord-maxima.json) | Measure a transform, then collect at sample-frame coordinates |
| [smhm.json](smhm.json) | Complete supplied example, preserved byte-for-byte |

## Full SMHM sequence

| Instruction | Station | Purpose in the supplied file |
| ---: | --- | --- |
| 0 | SPHINX | Four closely spaced holder-frame indentations |
| 1 | MAXIMA | 25 holder-frame points, `XRDXRF`, 150-second count time |
| 2 | HELIX | 25 flyer-grid points, seven PDV probes, paired waveplate angles |
| 3 | MAXIMA | The same 25 holder-frame points, `XRD`, 15-second count time |

The SPHINX input includes `batch_location` and `is_batch_process`; the current parser does not consume them. They remain in `smhm.json` to preserve the supplied example. The smaller SPHINX example omits them. The full example uses holder coordinates and flyer indices, so it does not require COORD or a sample-frame transform.

Controller pages explain each input and its API/SDK effect: [MAXIMA](../controllers/maxima.md), [HELIX](../controllers/helix.md), [SPHINX](../controllers/sphinx.md), [COORD](../controllers/coord.md).

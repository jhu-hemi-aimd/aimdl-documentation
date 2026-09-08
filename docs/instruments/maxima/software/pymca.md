---
title: PyMCA
status: needs-review
owner_team: maxima-team
primary_contact: Harrison Park
reviewers:
  - maxima-team
last_reviewed: null
review_cycle: 12 months
safety_level: informational
---

# PyMCA

**Relevant to:** Users performing XRF data analysis on MAXIMA output  

---

## Overview

**PyMCA** (Python Multi-Channel Analyzer) is an open-source Python library and GUI application
for analyzing X-ray fluorescence (XRF) spectra. For MAXIMA, it is used to fit elemental peaks
in XRF data collected by the silicon drift detector (SDD) and to convert raw spectra into
quantitative elemental concentrations.

In the automated MAXIMA data pipeline, PyMCA runs a **fundamental parameters** fitting pipeline
inside a containerized Dagster workflow, triggered automatically when new XRF data is streamed.

PyMCA documentation: [https://www.silx.org/doc/PyMca/](https://www.silx.org/doc/PyMca/)

---

## Installation

```bash
# Create and activate a dedicated environment
conda create -n pymca python=3.10
conda activate pymca

# Install PyMCA
pip install PyMca5

# Install GUI dependencies if using the PyMCA graphical interface
pip install pyqt5
```

> **Note:** PyMCA5 is the current maintained version. Do not install the older `pymca` package.

---

## File Format: `.mca`

XRF output from MAXIMA is saved as `.mca` files — a plain-text multi-channel analyzer format.
Each file contains a spectrum of X-ray intensity counts as a function of energy channel, along
with header metadata.

A MAXIMA `.mca` file follows this general structure:

```
#MCA ...
#DATE ...
#CHANNELS ...
DATA -->
<channel 0 counts>
<channel 1 counts>
...
END
```

> **TODO:** Confirm the exact header format produced by the MAXIMA SDD and add a representative
> example file or excerpt here.

---

## Configuration File (`.cfg`)

PyMCA uses a `.cfg` configuration file to define the fitting parameters for a given experiment.
This includes the X-ray energy, detector properties, and which elements to fit. A correctly
configured `.cfg` file is required to produce quantitative concentration outputs.

### Key parameters to set in the `.cfg` file

| Section | Parameter | Value for MAXIMA |
|---------|-----------|-----------------|
| `[detector]` | `zero` | Energy calibration zero offset |
| `[detector]` | `gain` | Energy calibration gain (eV/channel) |
| `[tube]` | `energy` | 24 keV (incident beam energy) |
| `[attenuators]` | — | Add any beam path attenuators present |
| `[concentrations]` | `usematrix` | Set to enable fundamental parameters quantification |

> **TODO:** Add a complete example `.cfg` file configured for a standard MAXIMA XRF run,
> with annotations explaining each section.

### Enabling Concentration Output

To output elemental concentrations (not just peak counts), the `[concentrations]` section of
the `.cfg` file must be properly configured with the fundamental parameters method. In the GUI:

1. Open the **Concentrations** tab.
2. Enable **Fundamental Parameters**.
3. Set the **flux**, **time**, **area**, and **distance** values matching your MAXIMA geometry.
4. Save the configuration to a `.cfg` file for reuse.

> **TODO:** Document the MAXIMA-specific flux, detector solid angle, and geometry values to
> use in the concentrations configuration.

---

## Using the PyMCA GUI

```bash
conda activate pymca
pymca
```

Workflow:
1. Load an `.mca` file via **File → Open**.
2. Load your `.cfg` configuration via **File → Load Configuration**.
3. Run the peak fit.
4. View results in the **Concentrations** table.
5. Export results as a CSV or HTML report.

---

## Batch Processing

For high-throughput analysis of many `.mca` files (as generated during a MAXIMA scan), PyMCA
supports batch fitting via the `PyMcaBatch` tool:

```bash
PyMcaBatch
```

Or programmatically:

```python
from PyMca5.PyMcaPhysics.xrf import McaAdvancedFit

# TODO: add working batch script example for MAXIMA .mca files
```

> **TODO:** Add or link to a working batch processing script from the AIMD-L GitHub repository.

---

## Automated Pipeline

In normal MAXIMA operation, XRF data is streamed and processed automatically by the Dagster
workflow using a PyMCA fundamental parameters pipeline. Processed concentrations and metadata
are written back to the data platform. Manual PyMCA analysis is a fallback for offline
reprocessing or debugging.

See [Dagster](dagster.md) for details on the automated pipeline.

---

## Known Issues

**XRF files not saving, or all intensities are zero:**  
Disconnect and reconnect all cables from the XRF detector, then power cycle MAXIMA. This is
a known workaround and not a permanent fix — contact Proto if the issue recurs. See
[Troubleshooting](../troubleshooting.md).

---

## Changelog

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0 | March 2025 | Harrison Park | Initial draft |

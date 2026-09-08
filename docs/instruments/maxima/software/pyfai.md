---
title: PyFAI
status: needs-review
owner_team: maxima-team
primary_contact: Harrison Park
reviewers:
  - maxima-team
last_reviewed: null
review_cycle: 12 months
safety_level: informational
---

# PyFAI

**Relevant to:** Users performing XRD data reduction on MAXIMA output  

---

## Overview

**PyFAI** (Python Fast Azimuthal Integration) is an open-source Python library for integrating
2D X-ray diffraction patterns into 1D intensity profiles. For MAXIMA, it is the primary tool for
converting raw `.h5` detector images from the Dectris Eiger 2R 1M CdTe into plots of intensity
versus scattering vector magnitude *q* (or 2θ).

In the automated MAXIMA data pipeline, PyFAI runs inside a containerized Dagster workflow that
is triggered automatically when new XRD data is streamed. It performs:

- Correction for detector tilt
- Beam center localization
- Sample-to-detector distance calibration
- Azimuthal integration to 1D output

PyFAI documentation: [https://www.silx.org/doc/pyFAI/latest/](https://www.silx.org/doc/pyFAI/latest/)  
Recalibration tutorial: [https://www.silx.org/doc/pyFAI/dev/usage/tutorial/Recalib/Recalib_notebook.html](https://www.silx.org/doc/pyFAI/dev/usage/tutorial/Recalib/Recalib_notebook.html)

---

## Installation (Local / Manual Environment)

For local analysis outside of the automated pipeline, install PyFAI in a dedicated conda
environment.

```bash
# Create and activate a dedicated environment
conda create -n pyfai python=3.10
conda activate pyfai

# Install pip inside the environment
conda install pip

# Install PyFAI
pip install pyFAI

# Install optional but commonly required dependencies
pip install silx fabio pyopencl

# Install GUI support (required for pyFAI-calib2 and other graphical tools)
pip install pyqt5
```

> **Note:** If `pip install pyFAI` fails due to missing dependencies like `silx` or `fabio`,
> install them explicitly before retrying. On some systems, `pyopencl` requires a matching
> OpenCL runtime to be installed separately (e.g., Intel or AMD OpenCL drivers).

---

## Detector Configuration for MAXIMA

MAXIMA uses a **Dectris Eiger 2R 1M CdTe** detector with:

- Pixel size: **75 µm × 75 µm**
- Active area: ~77 mm × 79 mm (1028 × 1062 pixels)
- CdTe detection layer: high efficiency at 24 keV
- Photon-counting: no readout noise, no dark current

When setting up a calibration in PyFAI, select `Eiger2_1M` as the detector type, or define
a custom detector if needed.

X-ray energy: **24 keV** (wavelength ≈ 0.5166 Å)

> **TODO:** Confirm exact wavelength value used in calibration files and add here.

---

## Calibration Workflow (Manual)

Use this when the automated Dagster pipeline is unavailable or when re-calibrating manually.

### Using `pyFAI-calib2` (GUI)

```bash
conda activate pyfai
pyFAI-calib2
```

1. Load a calibrant diffraction image (collected from one of the alumina pucks — see
   [Calibration](../procedures/calibration.md)).
2. Set the detector type to `Eiger2_1M`.
3. Set the energy to **24 keV**.
4. Select `Al2O3` (alumina/corundum) as the calibrant material.
5. Pick calibrant rings and fit the geometry.
6. Save the `.poni` file — this stores the calibrated geometry (beam center, detector distance,
   tilt parameters).

### Using the Recalibration Notebook

The silx recalibration tutorial notebook provides a scripted alternative to the GUI:

```
https://www.silx.org/doc/pyFAI/dev/usage/tutorial/Recalib/Recalib_notebook.html
```

> **TODO:** Create a MAXIMA-specific calibration notebook with correct detector, energy, and
> calibrant settings pre-filled.

---

## Integration Workflow (Manual)

Once a `.poni` calibration file exists, azimuthal integration can be run programmatically:

```python
import pyFAI
import fabio

# Load calibration
ai = pyFAI.load("calibration.poni")

# Load detector image
img = fabio.open("data_00001.h5").data

# Integrate to 1D
q, I = ai.integrate1d(img, 1000, unit="q_A^-1")
```

> **TODO:** Add a MAXIMA-specific integration script that handles the `.h5` file format from
> the Dectris Eiger, including any master file / data file pairing logic.

---

## Known Issues

- The automated pipeline performs calibration and integration automatically for new data. Manual
  calibration is a fallback, not routine.
- PyFAI's OpenCL acceleration may not work on all hardware. If you see OpenCL errors, integration
  still works without GPU acceleration — it will be slower.

---

## Changelog

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0 | March 2025 | Harrison Park | Initial draft |

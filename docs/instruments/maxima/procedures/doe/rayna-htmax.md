---
title: "DOE: HTMAX Ti-V (Rayna)"
status: needs-review
owner_team: maxima-team
primary_contact: Harrison Park
reviewers:
  - maxima-team
last_reviewed: null
review_cycle: 6 months
safety_level: operational
---

**Relevant to:** Operators running Rayna's Ti-V HTMAX samples  

# DOE: HTMAX – Ti-V (Rayna)

## Overview

This page documents sample-specific procedures, known limitations, and run considerations
for Rayna's Ti-V sputter-deposited samples characterized on MAXIMA as part of the HTMAX
campaign. As of May 2026, these samples have not been successfully produced in a reliably
flat form, which introduces non-standard handling requirements at every stage.

---

## Sample Preparation and Mounting

These samples do not conform to the standard flat form factor. Mounting is performed using
**Sample Holder Design 2** (prototype by Joseph Nkansah-Mahaney) with a PLA backing.

**Procedure:**

1. Lay a strip of wide Kapton tape across the sample in the **X-direction**, pressing the
   sample flat against the PLA backing.
2. Repeat with a second strip in the **Y-direction** to constrain warping in both axes.
3. When loading into MAXIMA, orient the sample so it **faces outward** (away from the PLA
   backing, toward the front of the instrument).

> **Critical:** The sample must face the **XRF detector**, not the XRD detector. The 24.21 keV
> primary beam can diffract through PLA and reach the XRD detector, but Ti and V fluorescence
> is heavily attenuated by PLA. Incorrect orientation will result in loss of XRF signal.

---

## Known Sample Quality Issues

### Heat Treatment Compatibility

Ti-V samples cannot use alumina (Al₂O₃) clamping plates during heat treatment, as Ti reacts
with Al. The current workaround — TiO₂ plates — partially mitigates this, but TiO₂ still
reacts with Ti at elevated temperatures, forming a brittle surface crust that alters the
expected near-surface composition.

As a result, warping during heat treatment is heavier and less uniform than in other sample
systems (e.g., Rohit's Cu-Ti or Chris Styles' Ti-6Al-4V).

### Non-Standard Sample Geometry

The lower sample yield means that viable candidates frequently come from the **edges** of the
deposition substrate — outside the standard rows 1–6, columns 1–3 form factor. Edge pieces
(e.g., row 0 or column 4) do not match the standard geometry and will cause coordinate
mismatches with default run scripts.

**Before running:** Inspect each sample's panel position and adjust run script coordinates
to match the actual sample geometry. Do not assume standard form factor.

---

## XRF Considerations

V Kα fluorescence is strongly attenuated by the Ti matrix in these samples because the V Kα
emission energy falls just below the Ti K absorption edge. As a result, **V Kβ fluorescence
must be used instead**, which has significantly lower signal intensity.

Longer dwell times are required compared to standard samples. Optimal scan time has not yet
been established as of May 2026 — monitor the V Kβ counts directly during test scans and
adjust accordingly.

> **Open item:** Determine a reliable minimum dwell time that yields acceptable V Kβ signal
> quality. Document findings here once established.

---

## Known Issues During Runs

### Sample Holder Lean → E3802

The Mark 2 holder with a taped PLA backing has an uneven weight distribution. When the UR10
transfers the sample from the buffer tray into the auto-door sample holder, the holder can
lean at an angle, preventing the UR3e from picking it up and triggering **E3802 (Robot pickup
timed out)**.

**Workaround:** During buffer-to-buffer sample transfers, manually reach into the auto-door
and press the sample holder flush against the **back wall** of the auto-door tray. This
corrects the lean before the UR3e attempts pickup.

See also: [Troubleshooting → E3802](../../troubleshooting.md#e3802-robot-pickup-timed-out)

---

## Changelog

| Version | Date      | Author        | Notes         |
|---------|-----------|---------------|---------------|
| 1.0     | May 2026  | Harrison Park | Initial draft |

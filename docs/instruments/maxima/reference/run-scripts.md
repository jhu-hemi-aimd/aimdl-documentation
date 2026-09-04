---
title: Run scripts
status: needs-review
owner_team: maxima-team
primary_contact: Harrison Park
reviewers:
  - maxima-team
last_reviewed: null
review_cycle: 12 months
safety_level: operational
---

Run scripts are commands given through either the AIMD-L run manager or MAXIMA manual run mode, and give the coordinates and settings for a MAXIMA run. 

Here is an example: 

{"sample": {"scan\_points": [[6, 31], [6, -32], [-23, 0], [35, 0], [6, 13], [6, 12], [6, 11], [6, 10], [6, 9], [6, 8], [6, 7], [6, 6], [6, 5], [6, 4], [6, 3], [6, 2], [6, 1], [6, 0], [6, -1], [6, -2], [6, -3], [6, -4], [6, -5], [6, -6], [6, -7], [6, -8], [6, -9], [6, -10], [6, -11], [6, -12], [6, -13]]}, "xray\_settings": {"current": 4.375, "voltage": 160, "beam\_x": 80, "beam\_y": 120}, "collection\_settings": {"detector\_distance": 0.0, "count\_time": 30.0, "collection\_mode": "XRDXRF"}}

Coordinates are based on an x,y coordinate system where the index 0 is the x position. The positive direction is towards Joseph's office, while the negative is towards the laboratory bench. Note that these coordinate systems can be quite confusing with the often changing orientation of samples going into MAXIMA. 

Current and voltage are can be controlled through the run script. Beam\_x and beam\_y, however, are not. This means that we have to be careful about what we put into these values, as much of the metadata is pulled from the run script rather than from a direct connection to MAXIMA. 

Detector\_distance is an important value. While it currently defaults to 0, it used to default to a value of 70 (back from Michael Wall and Timothy Long's time at AIMD-L, where they used a separate reference frame that placed 0 at the base of the X-ray source(?)... I'm not quite sure). It denotes where MAXIMA places the sample between the detector and the X-ray source. 

While there are several safeguards in place to stop MAXIMA from ramming the sample against the detectors or X-ray source, there are still several ways in which this can cause issues. 

There are no good safeguards for the XRF detector, which has a beryllium window (highly carginogenic). The current MAXIMA safeguards stop it from moving in the -x direction (towards the X-ray source and XRF detector). However, if the XRF detector is placed at a relative x value greater than or equal to 0 on the UR3e, it will hit. 


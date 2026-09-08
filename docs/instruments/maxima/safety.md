---
title: MAXIMA safety
status: needs-review
owner_team: maxima-team
primary_contact: Harrison Park
reviewers:
  - maxima-team
  - lab-safety-team
last_reviewed: null
review_cycle: 6 months
safety_level: safety-critical
---

# Safety Procedures

**Relevant to:** All personnel operating or entering AIMD-L during X-ray or robotic operations  

---

## Overview

MAXIMA is a high-energy X-ray instrument operating at **24 keV**(In Kalpha peak) with a focused beam capable of penetrating bulk structural metals. All personnel must understand and follow the safety procedures below before working in AIMD-L. This document does not replace in-person safety training.

---

## General Lab Safety

The following requirements apply to all personnel at all times in AIMD-L:

- **Buddy system:** Never operate MAXIMA alone. A second person must be present during all X-ray
  operations.
- **PPE:** Lab coat and safety goggles must be worn whenever you are in the lab.
- **Dosimeter:** Based on X-ray safety protocols, on-person dosimeters are not required after a certain period of time in which dosimeters have not shown high doses. Rather, we have several dosimeters placed around MAXIMA, while Proto comes in for leak checks once a year. 
- **Warning lights:** Always confirm the correct light state (see [Indication System](#indication-system))
  before starting or stopping any procedure.
- **Closing the lab:** If you are the last group to leave for the day, turn off all warning indicators lights (laser, X-ray, and conveyance systems) using the switch near the lab door, and turn off all office lights. Laboratory level indicator lights are switched off at the entrance of AIMD-L, while office lights can be turned off from the control room. 
---

## Indication System

A four-color light tower on top of the MAXIMA enclosure provides real-time visual status of the instrument.
Always check the light state before any procedure.

| Light | Status | Meaning |
|-------|--------|---------|
| 🔴 Red | On | Shutter is open |
| 🟡 Yellow | On | X-rays are on |
| ⚪ White | On | Interlock Fault|
| 🟢 Green | On | System safe / standby |
---

## Interlock System

The interlock system is the primary hardware safety barrier preventing X-ray radiation from reaching personnel outside the enclosure.

**How it works:** The system enforces a fail-safe condition such that the X-ray shutter and the
auto-door lock cannot both be open simultaneously. The shutter — not the door — is what contains
X-ray exposure.

**Critical implication:** The X-ray beam can be active while the auto-door is open. Although the
shutter should contain all exposure, this is an unsafe and uncomfortable condition, especially for other researchers in the laboratory. **Lab operating
procedure requires the auto-door to be closed during all experimental operations**, regardless of
shutter state.

**E-stop:** An emergency stop is available. Note that the E-stop may have a bi-stable latch behavior (hardware or software — currently unclear). If the interlock does not reset after an E-stop, contact Proto for remote assistance. Do not attempt to override the interlock manually. It should also be mentioned that the UR3e has some safety switches that are activated if the detector is accidentally touched. Resetting this takes an extended amount of time (requires sending a command from the control computer). 

---

## Radiation Safety

MAXIMA uses a focused, high-brightness liquid-metal-anode X-ray source (Excillum MetalJet E1+)
operating at **24 keV**. While the enclosure and interlock system are designed to contain all
radiation during normal operation, the following practices are mandatory:

- Never defeat or bypass the interlock system under any circumstances.
- Never place any part of your body inside the enclosure when X-rays may be active.
- Report any suspected radiation exposure to Todd Hufnagel and JHU Radiation Safety immediately.
- The dosimeter reading should be checked periodically. If unusual exposure is recorded, escalate
  immediately.

> For questions on JHU Radiation Safety policy, contact the JHU Radiation Safety office directly.
> MAXIMA operates under JHU's existing X-ray safety program.

---

## Points of Contact

Contact the appropriate person based on the nature of the issue. For hardware or safety-critical
issues during off-hours, Proto support is the first point of escalation.

| Name | Organization | Role | Email |
|------|-------------|------|-------|
| Brodie Bere | Proto | Robotics | bbere@protoxrd.com |
| Eric Schober | Proto | Hardware | eshober@protoxrd.com |
| Rob Drake | Proto | Proto Lead | rdrake@protoxrd.com |
| Shaun Ostoic | Proto | Software | sostoic@protoxrd.com |
| Proto Support | Proto | General Support | support@protoxrd.com |
| Matt Shaeffer | JHU / AIMD-L | AIMD Engineer | mshaeff1@jhu.edu |
| Todd Hufnagel | JHU / AIMD-L | AIMD Director | hufnagel@jhu.edu |
| Joseph Nkansah-Mahaney | JHU / AIMD-L | AIMD Engineer | tnkansa1@jhu.edu |
| Eric Walker | JHU / AIMD-L | AIMD Software | ewalke31@jhu.edu |
| Harrison Park | JHU / AIMD-L | Hardware / Software | hpark108@jhu.edu |
| Alexander Dejong | JHU / AIMD-L | Hardware / Software | adejong2@jhu.edu |

---

## Changelog

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0 | March 2025 | Harrison Park | Initial draft |

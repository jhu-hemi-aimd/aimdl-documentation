---
title: "HELIX controller"
status: needs-review
owner_team: software-team
primary_contact: null
last_reviewed: null
review_cycle: 6 months
safety_level: operational
tags: [software, controls]
---

# HELIX controller

HELIX performs laser shock experiments by coordinating package assembly, motion, flyer tracking, waveplate rotation, PDV, pulse triggering, energy measurement and waveform acquisition. `NAME='helix'` maps to physical station 1.

## Run inputs

| Field | Default / accepted input | Effect |
| --- | --- | --- |
| `sample.points.frame` | `flyer_grid` only | Grid addressing; physical units must be omitted |
| `sample.points.values` | Serpentine 25-point grid, rows/columns 2–6 | Ordered flyer positions; each coordinate must be a finite integer within those bounds |
| `waveplate_angles` | Five 30°, five 32.5°, five 35°, five 37.5°, five 40° | Angle paired with each original point; values clamped to 0–45° |
| `pdv_probes` | All configured probes | Selects probe configuration and associated oscilloscope channels |
| `flyer_stack.material` | Empty string on missing/invalid material | Material metadata; expected string |
| `flyer_stack.thickness` | null on missing/invalid thickness | Integer metadata recorded in µm; Boolean is not accepted |
| `sample.transform` | Injected by AIMDRM when available | Optional runtime sample-to-holder transform for output coordinates; do not author it in a script |

The preferred angle/probe representation is a JSON numeric array. The parser also accepts comma-separated strings. Missing/invalid angles or points trigger warnings and defaults. If too few angles are supplied, the last repeats; extra angles are ignored. Duplicate positions are removed **after pairing**, retaining the first point and its paired angle. Invalid probes are removed, duplicates retain their first occurrence, and the default set is used if no valid probes remain.

Configured probe IDs are 10, 6, 9, 15, 3, 8 and 19. Their physical channels and laser settings are maintained in `pdv/constants.py`. The script selects probes; it does not directly specify PDV wavelengths, source powers, scope trigger settings, heating-laser settings or UR robot programs.

## Device mapping

| Component | API/SDK boundary | Role |
| --- | --- | --- |
| UR10e | Universal Robots RTDE and register handshake | Assemble/disassemble the experimental package |
| Motion stage | Async command transport implemented in `motion_stage/` | Placement, home and corrected flyer positions |
| Top camera | IDS peak SDK | Image acquisition for flyer detection/alignment |
| Flyer tracking | Image/model detection plus motion adapter | Locate flyer and iteratively align it |
| Waveplate | `pylablib` Thorlabs / FTDI support | Set paired angle and home rotator |
| PDV | SCPI/VXI-11 instrument communication | Configure selected lasers and read probe signals |
| Power meter | Gentec-EO serial protocol through pySerial | Select range and measure shot energy |
| Pulse generator | SCPI command transport | Trigger pulse, then return output off |
| Oscilloscope | PyVISA, current `oscilloscope.infiniium.Oscilloscope` | Run/stop and waveform save |
| Heating laser | Adapter present | Connection/disconnection excluded from active `connect_all()` / `disconnect_all()` |

## Run sequence

Warmup, open and close are no-ops. During run the controller connects active devices concurrently, moves to package placement, assembles with UR10e, moves home, homes the waveplate, configures/enables PDV and starts the selected scope channels.

For each flyer it rotates the waveplate, selects the meter range and aligns the flyer. Failed detection/alignment records a skipped shot and does not trigger the laser. Successful alignment proceeds through shot execution and waveform saving. The shot number advances when the laser was actually triggered. The result writer records every attempted flyer and its status.

Normal/error cleanup stops acquisition and PDV, attempts package disassembly when the package state is assembled, and disconnects hardware. Cancellation stops acquisition and disconnects; it does **not** run the normal disassembly sequence. Review physical package state before subsequent work.

## Outputs

Under `/opt/aimdrc/data/{igsn}_{sample_id}_{instruction_no}_{run_id}_{timestamp}/`, `captures/` holds alignment images and `data_files/` holds the experiment CSV. The CSV records attempts, status, timing, coordinates, PDV/energy values and waveform references.

Current Infiniium waveform saving uses `:DISK:SAVE:WAVeform ALL,"{filename}",CSV,ON` and returns one file descriptor listing all contained channels. The shared `OscilloscopeWaveformFile(filename, channels)` contract also supports adapters that return several per-channel files (such as LeCroy). Scope files live on the scope's configured `SAVE_DIR`, not automatically in the controller data directory.

The CSV includes holder X/Y and optional sample X/Y in millimeters. Missing/invalid optional transform metadata leaves sample coordinates unavailable. A completed experiment may contain skipped or unsuccessful shots; use `successful_shot_count` and per-shot CSV status.

## Example

[Download helix.json](../examples/helix.json).

```json
{
  "schema_version": 2,
  "instructions": [
    [
      "helix",
      {
        "sample": {
          "points": {
            "frame": "flyer_grid",
            "values": [
              [
                2,
                2
              ],
              [
                2,
                3
              ],
              [
                2,
                4
              ]
            ]
          }
        },
        "flyer_stack": {
          "material": "Al",
          "thickness": 100
        },
        "pdv_probes": [
          10
        ],
        "waveplate_angles": [
          30,
          32.5,
          35
        ]
      }
    ]
  ]
}
```

## Setup and source map

Follow [station setup](../setup/stations.md#helix) and the existing [laser safety plan](../../instruments/helix/safety/safety.md). Source files: `controller.py`, `experiment/settings.py`, `experiment/constants.py`, `shot_executor/`, `flyer_tracking/`, `pdv/constants.py`, `oscilloscope/{infiniium,types,constants}.py`, `result_writer.py`. [Errors: 1000–1999](../reference/error-codes.md).

---
title: "MAXIMA controller"
status: needs-review
owner_team: software-team
primary_contact: null
last_reviewed: null
review_cycle: 6 months
safety_level: operational
tags: [software, controls]
---

# MAXIMA controller

MAXIMA coordinates the Proto X-ray system, sample robot, enclosure, shutter, detector and XRF collection through the generated `maxima.client` SDK. It is installed as the station controller in AIMDRC with `NAME='maxima'` (physical station 4).

## Run inputs

| Field | Default | Interpretation and handling |
| --- | --- | --- |
| `sample.points` | 7×7 grid at 5, 10, …, 35 mm along each axis | Controller requires resolved `sample_holder` / `mm` points; AIMDRM performs script-frame conversion |
| `collection_settings.collection_mode` | `XRDXRF` | `XRD`, `XRF`, `XRDXRF`; invalid mode warns and defaults |
| `collection_settings.count_time` | 10.0 | Seconds; numeric conversion, minimum 1.0 |
| `collection_settings.detector_distance` | 0 | Integer millimeter offset used by robot transform; accepted range 0–20; otherwise default 0 |
| `collection_settings.calibrate` | false | Parsed, but calibration execution is bypassed in current `warmup()` |
| `collection_settings.adaptive_ct` | false | Parsed and returned by validation, then discarded by the controller; does not change collection time |
| `xray_settings.current` | 4.375 | mA; accepted range 0.1–5.0; above 4.375 raises an advisory warning |
| `xray_settings.voltage` | 160.0 | kV; accepted range 100–160 |
| `xray_settings.beam_x` | 120.0 | Requested spot width in µm; accepted range 1–120 |
| `xray_settings.beam_y` | 120.0 | Requested spot height in µm; accepted range 1–120 |

The controller defaults invalid/missing point input. Numeric setting conversion failures use configured defaults and out-of-range values are replaced with the corresponding configured default and a warning. These are software normalization rules, not a determination that an experiment is physically appropriate.

!!! warning "Calibration currently bypassed"
    After readiness checks, `warmup()` returns before its calibration implementation even when calibration is requested. The older README example with detector distance 70 is outside the current 0–20 bound. Use current code behavior when interpreting a run.

## API mapping

| Input or operation | SDK effect |
| --- | --- |
| Current, voltage and beam size | Populate `ExcillumSettings` fields `current_m_a`, `voltage_k_v`, `spot_width_um`, `spot_height_um`; source-on submits settings via `xrays_on_with_http_info` |
| Points and detector distance | Convert holder point with `Robot.transform_point()` and submit `move_to_with_http_info` |
| Collection mode | `Collection.xrayTechnique = XrayTechnique(...)` |
| Count time | `EigerExposureConfig.exposureTimeSeconds` |
| Acquisition path | `EigerExposureConfig.saveToPath`; one image with raw and corrected saves enabled |
| Collect / poll / cancel | `image_with_http_info`, `ongoing_collection_with_http_info`, `cancel_with_http_info` |
| Sample pickup / return | Robot automated-collection and stop-collecting API calls |
| Door / shutter | Poll actual state; toggle through the corresponding Proto API |

The code sends beam dimensions to Proto. Older documentation says the physical beam is not controlled by those values; the source alone cannot establish whether the deployed vendor server applies them physically. Confirm the instrument configuration when that distinction affects an experiment.

## Lifecycle

Readiness waits for API availability, no retained robot sample, no ongoing collection, an idle/filewriter-ready detector, closed door/interlocks and calibrated source status. Warmup then returns with the calibration bypass described above.

Run validation creates the output folder and saves `instructions.txt`. The robot picks the sample, the door closes, X-rays turn on and the shutter opens. For each point the robot moves, collection executes and XRD output is cleaned when applicable. A failed move or hard collection failure skips that point; a soft timeout can still finish successfully. Normal cleanup closes the shutter, turns off X-rays, returns the sample and removes temporary timestamp metadata.

Cancellation cancels acquisition, closes the shutter, turns off X-rays and requests best-effort sample return. The run task skips its ordinary cleanup when canceled so the cancellation method owns that path.

## Outputs and interpretation

Automatic data are saved under `/opt/aimdrc/data/automatic_mode/{igsn}_{sample_id}_{instruction_no}_{run_id}_{timestamp}/`, including `raw/` and `instructions.txt`. Manual mode uses `manual_mode/`. The run output contains `data_directory`; AIMDRC logs it but does not automatically upload it.

A completed instruction does not guarantee every requested point produced data. Inspect per-point files and collection errors for skipped points. The detector share and container data mount must refer to the same intended dataset location.

## Example

[Download maxima.json](../examples/maxima.json).

```json
{
  "schema_version": 2,
  "instructions": [
    [
      "maxima",
      {
        "sample": {
          "points": {
            "frame": "sample_holder",
            "units": "mm",
            "values": [
              [
                5,
                5
              ]
            ]
          }
        },
        "collection_settings": {
          "adaptive_ct": false,
          "calibrate": false,
          "collection_mode": "XRDXRF",
          "count_time": 10,
          "detector_distance": 0
        },
        "xray_settings": {
          "beam_x": 80,
          "beam_y": 120,
          "current": 4.375,
          "voltage": 160
        }
      }
    ]
  ]
}
```

## Setup and source map

[Station setup](../setup/stations.md#maxima) covers the Proto host and detector share. Relevant files: `controller.py`, `collection/{collection,constants}.py`, `xray_source/{xray_source,constants}.py`, `robot/robot.py`, `utils.py`. Error definitions occupy 4000–4999 in the [catalog](../reference/error-codes.md).

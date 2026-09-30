---
title: "SPHINX controller"
status: needs-review
owner_team: software-team
primary_contact: null
last_reviewed: null
review_cycle: 6 months
safety_level: operational
tags: [software, controls]
---

# SPHINX controller

SPHINX controls the nanoindenter through the InView HTTP command interface and verifies sample presence through a LabJack vacuum sensor. The controller composes `InViewClient`, `MotionStage`, `IndentationExecutor` and `VacuumSensor`. `NAME='sphinx'` maps to physical station 5.

## Run inputs

| Field | Default | Effect |
| --- | --- | --- |
| `sample.points` | `[5,5]`, `[4.95,5]`, `[4.95,5.05]`, `[5,5.05]` | Resolved holder-frame XY in millimeters, converted to microscope-stage coordinates |
| `indentation_settings.z_pos` | 0.0153 | Stage Z in **meters**, finite non-Boolean number |
| `indentation_settings.method_file` | Supplied `JHU_Noise_Analysis_AIMD_1sec.NMT` path | Nonempty path on the InView host |
| `indentation_settings.method_inputs` | `{}` | Named values supplied through `IV:SetInput` for the configured method |
| `indentation_settings.batch_location` | Not read | Present in older examples; no effect in this parser |
| `indentation_settings.is_batch_process` | Not read | Present in older examples; no effect in this parser |

Invalid recognized input fields produce warning errors and defaults. The exact configured method path appears in the example below. Confirm that it exists and that the method's named inputs are valid. The parser does not know the vendor method's complete input schema and does not enforce a physical Z envelope.

## Coordinate and command mapping

The controller converts holder XY millimeters into microscope meters using the configured origin: `stage_x = origin_x - x*0.001`, `stage_y = origin_y + y*0.001`. Motion-stage code owns the separate microscope-to-indenter offset. Do not apply that offset in the run script.

`InViewClient` POSTs a JSON envelope to `http://host.docker.internal:50031` with the command in `Args`. It distinguishes success, failure and an unknown motion outcome. Generic requests use a 10-second timeout and `IV:GoToLocation()` uses 30 seconds; a motion timeout requires checking measured position, not assuming the command never ran.

| Input / step | InView command |
| --- | --- |
| Configure mode | `IV:SwitchMode(MultiSample)` |
| Prepare project | `IV:ClearMultisample()` then `IV:NewMultisample(...)` |
| Converted points, method path and sample name | `IV:AddSample(...)` |
| Each method input | `IV:SetInput(...)` |
| Execute / cancel | `IV:StartTest()` / `IV:StopTest()` |
| End cleanup | `IV:ClearMultisample()` and explicit idle confirmation |

## Lifecycle and readiness

Warmup waits for InView idle, moves to and verifies the load position, then waits for an empty vacuum sensor. During run, SPHINX verifies load position and sample presence **before moving to the microscope**. This ordering comes from the code, correcting the older README sequence.

It moves through microscope and indenter positions, configures a multisample project and monitors final-test completion. It returns through the final microscope position to load, clears the completed project and confirms idle before returning normally. Expected communication/motion/vacuum failures report errors and continue waiting for recovery.

The vacuum adapter reads configured LabJack channels `FIO4` and `AIN4`; the supplied analog threshold is 1.0 V, with sample presence below that threshold. Channel addresses and thresholds are deployment calibration, not run-script options.

## Cancellation limitation

SPHINX asks InView to stop and waits up to 10 seconds for explicit idle. If stop is unconfirmed it returns `Not Cancelled`. If interrupted near the indenter, during a test or in an unknown state, it reports `CANCEL_REQUIRES_VERIFICATION` and suppresses automatic stage recovery until an operator verifies tip clearance. Known safe states can return through microscope to load.

However, the shared AIMDRC client does not interpret these returned status strings and still advances its software cancellation state on a normal return. It also uses a 20-second cancellation timeout. Treat the logged SPHINX outcome and physical stage state as essential recovery information; `CNLD` alone does not establish successful stop or return to load.

## Outputs

InView owns the experiment files. The project folder name is `{igsn}_{instruction_no}_{run_id}_{timestamp}` and the sample name includes IGSN and timestamp. SPHINX returns `{}` after completion; it does not publish a reserved OPC UA result or return a data directory. Inspect InView's configured output location.

## Example

[Download sphinx.json](../examples/sphinx.json).

```json
{
  "schema_version": 2,
  "instructions": [
    [
      "sphinx",
      {
        "sample": {
          "points": {
            "frame": "sample_holder",
            "units": "mm",
            "values": [
              [
                5.0,
                5.0
              ],
              [
                4.95,
                5.0
              ],
              [
                4.95,
                5.05
              ],
              [
                5.0,
                5.05
              ]
            ]
          }
        },
        "indentation_settings": {
          "method_file": "C:/Users/Public/Documents/Nanomechanics/Profiles/AIMD-L/Methods/Mostafa/JHU_Noise_Analysis_AIMD_1sec.NMT",
          "method_inputs": {},
          "z_pos": 0.0153
        }
      }
    ]
  ]
}
```

## Setup and source map

[Station setup](../setup/stations.md#sphinx). Files: `controller.py`, `coordinates.py`, `state.py`, `indentation/{settings,executor,constants}.py`, `inview/{client,parsers}.py`, `motion_stage/`, `vacuum_sensor/`. [Errors: 5000–5499](../reference/error-codes.md).

---
title: "Error symbols and coverage"
status: needs-review
owner_team: software-team
primary_contact: null
last_reviewed: null
review_cycle: 12 months
safety_level: informational
tags: [software, controls]
---

# Error symbols and coverage

The following names come from controller and shared-client error declarations. Canonical severity, message and action are in the [generated catalog](error-codes.md). A declared symbol is not necessarily emitted by the active experiment path.

## MAXIMA

| Code | Symbol | Source file | Registry |
| ---: | --- | --- | --- |
| 4000 | `SystemAPIErrors.API_FAILURE` | `system/errors.py` | [Definition](error-codes.md#error-4000) |
| 4001 | `SystemAPIErrors.GENERIC_WARNING` | `system/errors.py` | [Definition](error-codes.md#error-4001) |
| 4110 | `PLCErrors.INTERLOCK_OPEN` | `plc/errors.py` | [Definition](error-codes.md#error-4110) |
| 4301 | `XRaySourceErrors.TIMEOUT` | `xray_source/errors.py` | [Definition](error-codes.md#error-4301) |
| 4302 | `XRaySourceErrors.NEEDS_CALIBRATION` | `xray_source/errors.py` | [Definition](error-codes.md#error-4302) |
| 4310 | `XRaySourceErrors.CURRENT_BOUNDS` | `xray_source/errors.py` | [Definition](error-codes.md#error-4310) |
| 4311 | `XRaySourceErrors.CURRENT_RECOMMEND` | `xray_source/errors.py` | [Definition](error-codes.md#error-4311) |
| 4320 | `XRaySourceErrors.VOLTAGE_BOUNDS` | `xray_source/errors.py` | [Definition](error-codes.md#error-4320) |
| 4330 | `XRaySourceErrors.BEAM_X_BOUNDS` | `xray_source/errors.py` | [Definition](error-codes.md#error-4330) |
| 4331 | `XRaySourceErrors.BEAM_Y_BOUNDS` | `xray_source/errors.py` | [Definition](error-codes.md#error-4331) |
| 4390 | `XRaySourceErrors.CAST_ERROR` | `xray_source/errors.py` | [Definition](error-codes.md#error-4390) |
| 4401 | `ShutterErrors.FAILED_TO_OPEN` | `shutter/errors.py` | [Definition](error-codes.md#error-4401) |
| 4402 | `ShutterErrors.FAILED_TO_CLOSE` | `shutter/errors.py` | [Definition](error-codes.md#error-4402) |
| 4501 | `DetectorErrors.FAILED_TO_INITIALIZE` | `detector/errors.py` | [Definition](error-codes.md#error-4501) |
| 4510 | `DetectorErrors.FILEWRITER_FAILED_TO_ENABLE` | `detector/errors.py` | [Definition](error-codes.md#error-4510) |
| 4701 | `AutoDoorErrors.FAILED_TO_OPEN` | `autodoor/errors.py` | [Definition](error-codes.md#error-4701) |
| 4702 | `AutoDoorErrors.FAILED_TO_CLOSE` | `autodoor/errors.py` | [Definition](error-codes.md#error-4702) |
| 4801 | `RobotErrors.PICKUP_REQUEST_FAILED` | `robot/errors.py` | [Definition](error-codes.md#error-4801) |
| 4802 | `RobotErrors.PICKUP_TIMEOUT` | `robot/errors.py` | [Definition](error-codes.md#error-4802) |
| 4803 | `RobotErrors.DROPOFF_REQUEST_FAILED` | `robot/errors.py` | [Definition](error-codes.md#error-4803) |
| 4804 | `RobotErrors.DROPOFF_TIMEOUT` | `robot/errors.py` | [Definition](error-codes.md#error-4804) |
| 4805 | `RobotErrors.MOVE_REQUEST_FAILED` | `robot/errors.py` | [Definition](error-codes.md#error-4805) |
| 4806 | `RobotErrors.MOVE_TIMEOUT` | `robot/errors.py` | [Definition](error-codes.md#error-4806) |
| 4810 | `RobotErrors.PROTECTIVE_STOP` | `robot/errors.py` | [Definition](error-codes.md#error-4810) |
| 4820 | `RobotErrors.HAS_PART` | `robot/errors.py` | [Definition](error-codes.md#error-4820) |
| 4901 | `CollectionErrors.COLLECTION_REQUEST_FAILED` | `collection/errors.py` | [Definition](error-codes.md#error-4901) |
| 4902 | `CollectionErrors.COLLECTION_SOFT_TIMEOUT` | `collection/errors.py` | [Definition](error-codes.md#error-4902) |
| 4903 | `CollectionErrors.COLLECTION_HARD_TIMEOUT` | `collection/errors.py` | [Definition](error-codes.md#error-4903) |
| 4904 | `CollectionErrors.COLLECTION_MONITOR_FAILED` | `collection/errors.py` | [Definition](error-codes.md#error-4904) |
| 4905 | `CollectionErrors.COLLECTION_CANCEL_FAILED` | `collection/errors.py` | [Definition](error-codes.md#error-4905) |
| 4910 | `CollectionErrors.COLLECTION_MODE_INVALID` | `collection/errors.py` | [Definition](error-codes.md#error-4910) |
| 4920 | `CollectionErrors.SCAN_POINTS_INVALID` | `collection/errors.py` | [Definition](error-codes.md#error-4920) |
| 4930 | `CollectionErrors.COUNT_TIME_BOUNDS` | `collection/errors.py` | [Definition](error-codes.md#error-4930) |
| 4940 | `CollectionErrors.DETECTOR_DISTANCE_BOUNDS` | `collection/errors.py` | [Definition](error-codes.md#error-4940) |
| 4990 | `CollectionErrors.CAST_ERROR` | `collection/errors.py` | [Definition](error-codes.md#error-4990) |

## HELIX

| Code | Symbol | Source file | Registry |
| ---: | --- | --- | --- |
| 1010 | `ExperimentSettingsErrors.FLYER_STACK_INVALID` | `experiment/errors.py` | [Definition](error-codes.md#error-1010) |
| 1011 | `ExperimentSettingsErrors.FLYER_MATERIAL_INVALID` | `experiment/errors.py` | [Definition](error-codes.md#error-1011) |
| 1012 | `ExperimentSettingsErrors.FLYER_THICKNESS_INVALID` | `experiment/errors.py` | [Definition](error-codes.md#error-1012) |
| 1020 | `ExperimentSettingsErrors.PULSE_POINTS_INVALID` | `experiment/errors.py` | [Definition](error-codes.md#error-1020) |
| 1021 | `ExperimentSettingsErrors.PULSE_POINTS_DUPLICATE` | `experiment/errors.py` | [Definition](error-codes.md#error-1021) |
| 1030 | `ExperimentSettingsErrors.WAVEPLATE_ANGLES_INVALID` | `experiment/errors.py` | [Definition](error-codes.md#error-1030) |
| 1031 | `ExperimentSettingsErrors.WAVEPLATE_ANGLES_BOUNDS` | `experiment/errors.py` | [Definition](error-codes.md#error-1031) |
| 1040 | `ExperimentSettingsErrors.PDV_PROBES_INVALID` | `experiment/errors.py` | [Definition](error-codes.md#error-1040) |
| 1041 | `ExperimentSettingsErrors.PDV_PROBES_DUPLICATE` | `experiment/errors.py` | [Definition](error-codes.md#error-1041) |
| 1051 | `HeatingLaserErrors.CONNECTION_FAILED` | `heating_laser/errors.py` | [Definition](error-codes.md#error-1051) |
| 1060 | `HeatingLaserErrors.START_FAILED` | `heating_laser/errors.py` | **Missing definition** |
| 1061 | `HeatingLaserErrors.STOP_FAILED` | `heating_laser/errors.py` | **Missing definition** |
| 1101 | `MotionStageErrors.CONNECTION_FAILED` | `motion_stage/errors.py` | [Definition](error-codes.md#error-1101) |
| 1110 | `MotionStageErrors.MOTORS_FAILED_TO_ENABLE` | `motion_stage/errors.py` | [Definition](error-codes.md#error-1110) |
| 1111 | `MotionStageErrors.MOTORS_FAILED_TO_DISABLE` | `motion_stage/errors.py` | [Definition](error-codes.md#error-1111) |
| 1120 | `MotionStageErrors.MOVE_REQUEST_FAILED` | `motion_stage/errors.py` | [Definition](error-codes.md#error-1120) |
| 1121 | `MotionStageErrors.MOTION_FAILED` | `motion_stage/errors.py` | [Definition](error-codes.md#error-1121) |
| 1151 | `OscilloscopeErrors.CONNECTION_FAILED` | `oscilloscope/errors.py` | [Definition](error-codes.md#error-1151) |
| 1160 | `OscilloscopeErrors.STOP_FAILED` | `oscilloscope/errors.py` | [Definition](error-codes.md#error-1160) |
| 1161 | `OscilloscopeErrors.RUN_FAILED` | `oscilloscope/errors.py` | [Definition](error-codes.md#error-1161) |
| 1170 | `OscilloscopeErrors.WAVEFORM_SAVE_FAILED` | `oscilloscope/errors.py` | [Definition](error-codes.md#error-1170) |
| 1201 | `PDVErrors.CONNECTION_FAILED` | `pdv/errors.py` | [Definition](error-codes.md#error-1201) |
| 1210 | `PDVErrors.SHUTDOWN_FAILED` | `pdv/errors.py` | [Definition](error-codes.md#error-1210) |
| 1211 | `PDVErrors.CONFIGURATION_FAILED` | `pdv/errors.py` | [Definition](error-codes.md#error-1211) |
| 1212 | `PDVErrors.OUTPUT_ENABLE_FAILED` | `pdv/errors.py` | [Definition](error-codes.md#error-1212) |
| 1213 | `PDVErrors.READ_FAILED` | `pdv/errors.py` | [Definition](error-codes.md#error-1213) |
| 1251 | `PowerMeterErrors.CONNECTION_FAILED` | `power_meter/errors.py` | [Definition](error-codes.md#error-1251) |
| 1260 | `PowerMeterErrors.RANGE_CHANGE_FAILED` | `power_meter/errors.py` | [Definition](error-codes.md#error-1260) |
| 1301 | `PulseGeneratorErrors.CONNECTION_FAILED` | `pulse_generator/errors.py` | [Definition](error-codes.md#error-1301) |
| 1310 | `PulseGeneratorErrors.PULSE_DISABLE_FAILED` | `pulse_generator/errors.py` | [Definition](error-codes.md#error-1310) |
| 1351 | `TopCameraErrors.CONNECTION_FAILED` | `top_camera/errors.py` | [Definition](error-codes.md#error-1351) |
| 1360 | `TopCameraErrors.ACQUISITION_FAILED` | `top_camera/errors.py` | [Definition](error-codes.md#error-1360) |
| 1401 | `UR10eErrors.CONNECTION_FAILED` | `ur10e/errors.py` | [Definition](error-codes.md#error-1401) |
| 1410 | `UR10eErrors.ASSEMBLY_REQUEST_FAILED` | `ur10e/errors.py` | [Definition](error-codes.md#error-1410) |
| 1411 | `UR10eErrors.ASSEMBLY_FAILED_TO_START` | `ur10e/errors.py` | [Definition](error-codes.md#error-1411) |
| 1412 | `UR10eErrors.ASSEMBLY_FAILED_TO_COMPLETE` | `ur10e/errors.py` | [Definition](error-codes.md#error-1412) |
| 1420 | `UR10eErrors.DISASSEMBLY_REQUEST_FAILED` | `ur10e/errors.py` | [Definition](error-codes.md#error-1420) |
| 1421 | `UR10eErrors.DISASSEMBLY_FAILED_TO_START` | `ur10e/errors.py` | [Definition](error-codes.md#error-1421) |
| 1422 | `UR10eErrors.DISASSEMBLY_FAILED_TO_COMPLETE` | `ur10e/errors.py` | [Definition](error-codes.md#error-1422) |
| 1451 | `WaveplateRotatorErrors.CONNECTION_FAILED` | `waveplate_rotator/errors.py` | [Definition](error-codes.md#error-1451) |
| 1460 | `WaveplateRotatorErrors.POSITION_INVALID` | `waveplate_rotator/errors.py` | [Definition](error-codes.md#error-1460) |
| 1470 | `WaveplateRotatorErrors.HOMING_FAILED` | `waveplate_rotator/errors.py` | [Definition](error-codes.md#error-1470) |
| 1471 | `WaveplateRotatorErrors.MOVEMENT_FAILED` | `waveplate_rotator/errors.py` | [Definition](error-codes.md#error-1471) |
| 1501 | `FlyerTrackerErrors.DETECTION_FAILED` | `flyer_tracking/errors.py` | [Definition](error-codes.md#error-1501) |
| 1551 | `ShotExecutorErrors.SHOT_FAILED` | `shot_executor/errors.py` | [Definition](error-codes.md#error-1551) |

## SPHINX

| Code | Symbol | Source file | Registry |
| ---: | --- | --- | --- |
| 5001 | `InViewErrors.UNREACHABLE` | `inview/errors.py` | [Definition](error-codes.md#error-5001) |
| 5002 | `InViewErrors.STATUS_UNAVAILABLE` | `inview/errors.py` | [Definition](error-codes.md#error-5002) |
| 5003 | `InViewErrors.COMMAND_FAILED` | `inview/errors.py` | [Definition](error-codes.md#error-5003) |
| 5101 | `MotionStageErrors.MOVE_FAILED` | `motion_stage/errors.py` | [Definition](error-codes.md#error-5101) |
| 5102 | `MotionStageErrors.LOCATION_UNAVAILABLE` | `motion_stage/errors.py` | [Definition](error-codes.md#error-5102) |
| 5201 | `IndentationErrors.CONFIGURATION_FAILED` | `indentation/errors.py` | [Definition](error-codes.md#error-5201) |
| 5202 | `IndentationErrors.START_FAILED` | `indentation/errors.py` | [Definition](error-codes.md#error-5202) |
| 5204 | `IndentationErrors.EXECUTION_TIMEOUT` | `indentation/errors.py` | [Definition](error-codes.md#error-5204) |
| 5205 | `IndentationErrors.CLEANUP_FAILED` | `indentation/errors.py` | [Definition](error-codes.md#error-5205) |
| 5250 | `IndentationErrors.POINTS_INVALID` | `indentation/errors.py` | [Definition](error-codes.md#error-5250) |
| 5251 | `IndentationErrors.SETTINGS_INVALID` | `indentation/errors.py` | [Definition](error-codes.md#error-5251) |
| 5252 | `IndentationErrors.Z_POSITION_INVALID` | `indentation/errors.py` | [Definition](error-codes.md#error-5252) |
| 5253 | `IndentationErrors.METHOD_FILE_INVALID` | `indentation/errors.py` | [Definition](error-codes.md#error-5253) |
| 5254 | `IndentationErrors.METHOD_INPUTS_INVALID` | `indentation/errors.py` | [Definition](error-codes.md#error-5254) |
| 5301 | `VacuumSensorErrors.READ_FAILED` | `vacuum_sensor/errors.py` | [Definition](error-codes.md#error-5301) |
| 5310 | `VacuumSensorErrors.SAMPLE_NOT_DETECTED` | `vacuum_sensor/errors.py` | [Definition](error-codes.md#error-5310) |
| 5311 | `VacuumSensorErrors.STAGE_NOT_EMPTY` | `vacuum_sensor/errors.py` | [Definition](error-codes.md#error-5311) |
| 5450 | `ControllerErrors.CANCEL_STOP_UNCONFIRMED` | `errors.py` | [Definition](error-codes.md#error-5450) |
| 5451 | `ControllerErrors.CANCEL_REQUIRES_VERIFICATION` | `errors.py` | [Definition](error-codes.md#error-5451) |

## COORD

| Code | Symbol | Source file | Registry |
| ---: | --- | --- | --- |
| 6510 | `ExperimentSettingsErrors.PHOTO_ONLY_INVALID` | `experiment/errors.py` | [Definition](error-codes.md#error-6510) |
| 6601 | `TopCameraErrors.CONNECTION_FAILED` | `top_camera/errors.py` | [Definition](error-codes.md#error-6601) |
| 6610 | `TopCameraErrors.ACQUISITION_FAILED` | `top_camera/errors.py` | [Definition](error-codes.md#error-6610) |
| 6700 | `DetectionErrors.TRANSFORM_REFUSED` | `detection/errors.py` | [Definition](error-codes.md#error-6700) |

## AIMDRC

| Code | Symbol | Source file | Registry |
| ---: | --- | --- | --- |
| 10111 | `Station.HELIX` | `src/api/apps/opcua/errors.py` | [Definition](error-codes.md#error-10111) |
| 10141 | `Station.MAXIMA` | `src/api/apps/opcua/errors.py` | [Definition](error-codes.md#error-10141) |
| 10151 | `Station.SPHINX` | `src/api/apps/opcua/errors.py` | [Definition](error-codes.md#error-10151) |
| 10156 | `Station.PROFILOMETER` | `src/api/apps/opcua/errors.py` | [Definition](error-codes.md#error-10156) |
| 10161 | `Station.ENGRAVER` | `src/api/apps/opcua/errors.py` | [Definition](error-codes.md#error-10161) |
| 10166 | `Station.COORDINATE` | `src/api/apps/opcua/errors.py` | [Definition](error-codes.md#error-10166) |

## Manager and robotics

Client disconnect codes: HELIX 10110, MAXIMA 10140, SPHINX 10150, profilometer 10155, engraver 10160, COORD 10165. Corresponding cancel-timeout codes are 10111, 10141, 10151, 10156, 10161 and 10166. These are defined in `run_client_monitor.py` and AIMDRC `opcua/errors.py`.

Robotics code 10200 is generated by the manager when the machine is not running; 10201–10208 map the global safety/conveyor alarm nodes. For physical station `n` (1–6), base code is `10200 + 10*n`:

| Offset | Meaning |
| ---: | --- |
| 0 | Robot off |
| 1 | Robot not in remote |
| 2 | Protective stop |
| 3 | Robot fault |
| 4 | Robot violation |
| 5 | Barcode error |
| 6 | Ingress error |
| 7 | Egress error |

The generated catalog expands all 48 station-specific entries. Manager source: `apps/opcua/robotics/errors.py`; canonical source: AIMDDS `apps/system/errors/run_manager/robotics.py`.

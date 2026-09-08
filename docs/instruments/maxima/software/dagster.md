---
title: Dagster
status: needs-review
owner_team: maxima-team
primary_contact: Harrison Park
reviewers:
  - maxima-team
last_reviewed: null
review_cycle: 12 months
safety_level: informational
---

# Dagster

MAXIMA uses [Dagster](https://dagster.io/) as its workflow orchestration framework. The [`MAXIMADagsterModules`](https://github.com/harrison1125/MAXIMADagsterModules) repository contains the full Dagster project for sensor-driven XRD and XRF experiment processing against Girder-backed data from MAXIMA. It detects new experiments arriving in Girder, materializes partitioned assets through the XRD pipeline, caches model and calibration artifacts locally, and publishes processed outputs back to Girder.

---

## Overview

### What It Does

At a high level, the system:

- Watches a Girder root folder for new experiment subfolders containing raw scan files matching the pattern `raw/scan_point_*_data_*.h5`.
- Triggers one Dagster run per new experiment by issuing dynamic partition keys equal to the Girder experiment folder ID.
- Executes the XRD pipeline: scan loading → calibration model inference → PONI file generation → azimuthal integration → lattice parameter extraction.
- Publishes result artifacts (a run manifest and CSV outputs) back into each experiment's Girder folder.
- Caches heavy artifacts locally to avoid repeated downloads and recomputation: ML model weights in `data/models/` and PONI files with index metadata in `data/calibrations/`.

### Current Pipeline Scope

The XRD sensor-driven flow is fully operational. XRF-related assets exist in the codebase under `src/MaximaDagster/modules/` but are not yet part of the primary sensor-driven `xrd_test_job` execution path.

---

## Architecture

The system is built around four core Dagster objects:

**`experiment_folder_sensor`** — Polls the Girder root folder (identified by `GIRDER_ROOT_FOLDER_ID`) for new experiment subfolders. When a new folder containing qualifying `.h5` scan files is detected, the sensor emits a `RunRequest` with the Girder folder ID as the dynamic partition key and launches `xrd_test_job`.

**`calibration_scan_sensor`** — Polls the Girder calibrants folder (identified by `GIRDER_CALIBRANTS_FOLDER_ID`) for updated calibrant scan files matching the pattern `xrd_calibrant_data_<id>.h5`. On detection it launches `calibration_precompute_job` to refresh the PONI file and calibration index cache.

**`xrd_test_job`** — The primary processing job. For a given partition (experiment folder ID), it materializes the full sequence of XRD assets: raw scan loading, calibration model application, PONI generation, azimuthal integration, and lattice parameter extraction. Results are written back to Girder and to the local cache.

**`calibration_precompute_job`** — A supporting job that precomputes and stores calibration prerequisites (PONI files, calibration metadata) so that `xrd_test_job` runs can retrieve them from cache rather than recomputing from scratch.

---

## Repository Layout

```
MAXIMADagsterModules/
├── src/
│   └── MaximaDagster/
│       ├── definitions.py       # Dagster Definitions object: job wiring, resource binding
│       ├── assets.py            # Software-defined assets for the XRD pipeline
│       ├── sensors.py           # experiment_folder_sensor and calibration_scan_sensor
│       ├── resources.py         # Dagster resource definitions (GirderClient, model loader, etc.)
│       ├── io_manager.py        # Custom IOManager for Girder-backed asset storage
│       ├── modules/             # XRD and XRF processing step implementations
│       └── utils/               # Shared helpers: Girder I/O, PONI utilities, filename patterns,
│           │                    #   and results publishing
│       └── defs/                # Package namespace for Dagster definition exports
├── tests/                       # pytest test suite (assets, modules, sensor/integration)
├── data/
│   ├── models/                  # Local cache for ML model weights (.pth files)
│   └── calibrations/            # Local cache for PONI files and calibration index metadata
├── dagster_home/                # Dagster instance config, run storage, and event log artifacts
├── .env.example                 # Template for required environment variables
├── workspace.yaml               # Dagster workspace: points to MaximaDagster.definitions
├── Dockerfile                   # Container image definition
├── docker-compose.yml           # Multi-service deployment (webserver, daemon, postgres)
└── pyproject.toml               # Package metadata and pinned dependencies
```

The entry point for Dagster is `workspace.yaml`, which loads the project via:

```yaml
load_from:
  - python_module:
      module_name: MaximaDagster.definitions
```

---

## Prerequisites

- Python `>=3.11, <3.15` (Python 3.11 is recommended and used in the container image)
- Access to the target Girder instance with read/write permissions on relevant folders
- The five required environment variables described below
- Docker and Docker Compose (optional, for containerized deployment)

---

## Environment Variables

Copy `.env.example` to `.env` and populate all five variables before running locally or in Docker:

```dotenv
GIRDER_API_URL=
GIRDER_API_KEY=
GIRDER_ROOT_FOLDER_ID=
GIRDER_CALIBRANTS_FOLDER_ID=
GIRDER_MODEL_ITEM_ID=
```

| Variable | Description |
|---|---|
| `GIRDER_API_URL` | Base URL of the Girder REST API (e.g., `https://girder.example.org/api/v1`) |
| `GIRDER_API_KEY` | API key for an account with read/write access to relevant Girder folders |
| `GIRDER_ROOT_FOLDER_ID` | Girder folder ID of the parent folder containing experiment subfolders |
| `GIRDER_CALIBRANTS_FOLDER_ID` | Girder folder ID of the folder containing calibrant `.h5` scan files |
| `GIRDER_MODEL_ITEM_ID` | Girder item ID for the `.pth` calibration model file |

> **Note:** In `docker-compose.yml` the daemon service uses the variable name `GIRDER_MODEL_ITEM_OR_FILE_ID` rather than `GIRDER_MODEL_ITEM_ID`. Ensure both are set consistently in `.env` if running via Docker.

---

## Dependencies

All dependencies are pinned in `pyproject.toml` (version `2026.3.0`):

| Package | Version | Purpose |
|---|---|---|
| `dagster` | `1.12.12` | Orchestration framework |
| `numpy` | `2.4.1` | Numerical array operations |
| `pandas` | `>=2.2,<3` | Tabular data handling and CSV output |
| `torch` | `2.10.0` | ML model inference (calibration model) |
| `torchvision` | `0.25.0` | Supporting torch utilities |
| `transformers` | `4.57.6` | Transformer model support |
| `fabio` | `2025.10.0` | Scientific image file I/O |
| `girder-client` | `3.0.0` | Girder REST API client |
| `h5py` | `>=3.11,<4` | HDF5 scan file reading |
| `pyFAI` | `2025.12.1` | Azimuthal integration and PONI calibration |
| `scikit-image` | `0.26.0` | Image processing utilities |
| `scikit-learn` | `1.8.0` | ML utilities |
| `scipy` | `1.17.0` | Scientific computing |
| `matplotlib` | `3.10.8` | Plotting and visualization |
| `PyMca5` | `5.9.5` | XRF spectral analysis |

Development extras (not installed in production):

```
dagster-webserver
dagster-dg-cli
pytest
```

---

## Local Development Setup

### 1. Create and Activate a Python Environment

Using Conda (recommended):

```bash
conda create -n dagster python=3.11 -y
conda activate dagster
```

### 2. Install the Package and Dev Dependencies

```bash
pip install -e .
pip install dagster-webserver dagster-dg-cli pytest
```

The editable install (`-e .`) makes changes to `src/MaximaDagster/` immediately reflected without reinstalling.

### 3. Configure Environment Variables

```powershell
# PowerShell
Copy-Item .env.example .env
# Edit .env and fill in all five Girder values
```

```bash
# Bash/Zsh
cp .env.example .env
# Edit .env and fill in all five Girder values
```

Then set `DAGSTER_HOME` for the current shell session so Dagster knows where to store run history and logs:

```powershell
# PowerShell
$env:DAGSTER_HOME = (Resolve-Path .\dagster_home)
```

```bash
# Bash/Zsh
export DAGSTER_HOME=$(pwd)/dagster_home
```

### 4. Launch Dagster

```bash
dagster dev -w workspace.yaml
```

Open the Dagster UI at [http://localhost:3000](http://localhost:3000).

Navigate to the **Automation** tab and enable both sensors:

- `experiment_folder_sensor` — begins polling Girder for new experiments
- `calibration_scan_sensor` — begins polling for calibrant scan updates

---

## Docker Deployment

The Docker deployment runs three services defined in `docker-compose.yml`: a PostgreSQL metadata store, the Dagster webserver, and the Dagster daemon (which evaluates sensors and submits runs).

### Services

| Service | Container Name | Description |
|---|---|---|
| `postgres` | `maxima_postgres` | PostgreSQL 16 metadata database for Dagster run/event storage |
| `dagster-webserver` | `maxima_dagster_webserver` | Dagster UI, accessible at port 3000 |
| `dagster-daemon` | `maxima_dagster_daemon` | Evaluates sensors and schedules, submits run requests |

Both the webserver and daemon share the same Docker image built from the local `Dockerfile`. They mount `./dagster_home` and `./data` as volumes so that run state and local caches persist across container restarts.

### Quickstart

**1. Configure environment:**

```bash
cp .env.example .env
# Edit .env with your Girder values
```

**2. Build and start all services:**

```bash
docker compose up --build -d
```

**3. Open the Dagster UI:**

Navigate to [http://localhost:3000](http://localhost:3000).

**4. Enable sensors:**

In the **Automation** tab, enable `experiment_folder_sensor` and `calibration_scan_sensor`.

**5. Monitor logs:**

```bash
docker compose logs -f dagster-daemon dagster-webserver
```

**6. Stop services:**

```bash
docker compose down
```

### Docker Image Details

The image is built from `python:3.11-slim`. PyTorch CPU wheels are installed separately from the PyTorch index before the remainder of the package:

```dockerfile
pip install --extra-index-url https://download.pytorch.org/whl/cpu torch==2.10.0 torchvision==0.25.0
pip install .
pip install dagster-webserver==1.12.12 dagster-postgres==0.28.12
```

System libraries installed in the image: `build-essential`, `libgl1`, `libglib2.0-0`, `libsm6`, `libxext6`, `libxrender1`. These are required by pyFAI and scikit-image for scientific image processing.

The image creates two cache directories at build time: `/opt/dagster/app/data/models` and `/opt/dagster/app/data/calibrations`.

---

## Operational Notes

### Partitioning

Experiment partition keys are the Girder folder IDs of individual experiment subfolders. Each `RunRequest` emitted by `experiment_folder_sensor` carries a unique folder ID as its partition key, which flows through `xrd_test_job` and identifies exactly which experiment's data to process.

### Caching

The local cache reduces repeated Girder downloads and avoids rerunning expensive calibration computations:

- **`data/models/`** — stores the downloaded `.pth` model file keyed by `GIRDER_MODEL_ITEM_ID`.
- **`data/calibrations/`** — stores PONI files and calibration index metadata produced by `calibration_precompute_job`.

To force a cache refresh, delete the relevant files under these directories and re-trigger the appropriate job. In Docker, the `./data` directory is bind-mounted, so deletions on the host are immediately visible to the containers.

### Running Tests

```bash
pytest
```

The test suite in `tests/` covers asset materializations, processing module behavior, and sensor/integration behavior against mock Girder responses.

---

## Troubleshooting

**No sensor runs are being triggered.**
Verify that all five `GIRDER_*` environment variables are set and contain valid values. The sensor will silently skip ticks if it cannot authenticate to or contact the Girder API. Check `dagster-daemon` logs for authentication or network errors.

**Runs fail with an asset loading error.**
Confirm that `workspace.yaml` correctly resolves `MaximaDagster.definitions` in your Python environment. If running locally, ensure the package was installed with `pip install -e .` and that the correct conda/venv is active. If running in Docker, verify the image was rebuilt after any source changes (`docker compose up --build`).

**Calibration is not refreshing or PONI files are stale.**
Ensure new calibrant scan files in Girder match the expected filename pattern `xrd_calibrant_data_<id>.h5`. The `calibration_scan_sensor` uses this pattern for detection. Files with non-conforming names will be ignored. If the pattern needs to be adjusted for your specific calibrant file naming, update the relevant pattern helper in `src/MaximaDagster/utils/`.

**XRF assets are not processing.**
XRF-related assets exist in the codebase but are not currently wired into the primary sensor-driven execution path. They are not part of `xrd_test_job`. XRF processing will require additional job and sensor configuration when that feature is promoted to operational status.

---

## Related Resources

- [`MAXIMADagsterModules` repository](https://github.com/harrison1125/MAXIMADagsterModules)
- [Dagster documentation](https://docs.dagster.io/)
- [Girder documentation](https://girder.readthedocs.io/)
- [pyFAI documentation](https://pyfai.readthedocs.io/)

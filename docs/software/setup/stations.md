---
title: "Station client setup"
status: needs-review
owner_team: software-team
primary_contact: null
last_reviewed: null
review_cycle: 6 months
safety_level: operational
tags: [software, controls]
---

# Station client setup

Install one AIMDRC instance for each logical controller. Keep generic client code separate from the controller package so state-machine fixes can be deployed consistently.

## Common installation

1. Prepare the AIMDRC checkout and station host. On Windows, the source README uses Git Bash, Docker Desktop with the WSL backend, Unix-style commit line endings and symlink support.
2. Copy the selected controller repository contents into `aimdrc/src/api/apps/controller/`. Preserve AIMDRC's `interface.py`; do not nest the repository one extra level or remove the shared interface.
3. Select `config/settings/local.py` or `prod.py` using `main.py`, and set `NAME` to `maxima`, `helix`, `sphinx` or `coord`. Set manager domain and station/server certificate paths.
4. Install controller-provided host support and vendor dependencies described below.
5. Build the image after copying the controller. The Dockerfile copies its dependency artifacts, runs its OS installer, and installs its Python requirements.
6. Run with persistent source/data mounts and the required device/network access. Verify identity and client heartbeat in System status and the client log.

The factory path defaults to `apps.controller.controller.Controller`. The generalized Python build script specifies 3.14.5 in this snapshot; COORD requires a station-specific CPython 3.12 build because its vendor wheel is ABI-specific.

## Certificates

The supplied production example generates a station-specific self-signed certificate and key. Substitute the actual station for `maxima` and verify the certificate template's identity fields:

```bash
openssl req \
  -config ~/aimdrc/src/certs/prod/station-aimd-hemi-jhu-edu.conf \
  -newkey rsa:4096 -nodes -x509 -sha256 -days 365 \
  -keyout ~/aimdrc/src/private/prod/maxima-aimd-hemi-jhu-edu.key \
  -out ~/aimdrc/src/certs/prod/maxima-aimd-hemi-jhu-edu.cert
```

Copy only the public station certificate into AIMDRM's configured certificate directory, and copy the manager public certificate into AIMDRC. Keep the station private key on its station host. For local setup use the corresponding `station-aimd-test.conf` template and `*-aimd-test` filenames. AIMDRM station registration is in `apps/stations.py`; restart its server after planned certificate/registry changes.

## Common build and service commands

```bash
docker build ~/aimdrc -f ~/aimdrc/docker/prod/Dockerfile -t aimdrc
docker exec -it --user aimdrc aimdrc bash
cd /opt/aimdrc
. venv/bin/activate
./src/api/manage.py test --debug-mode
tail -f /opt/aimdrc/logs/opcua/client.log
```

`/home/aimdrc/opcua-restart.sh` restarts the client process. On Git Bash, the README uses `winpty docker exec` for an interactive terminal and `MSYS_NO_PATHCONV=1` to preserve Linux paths in Docker commands. Do not run hardware diagnostic/manual-mode scripts as a software smoke test without the applicable instrument procedure.

## MAXIMA

Install the Proto SDK/controller dependencies from `requirements/`. Configure `constants.PROTO_HOST_IP` for the reachable Proto service; the supplied value is `http://192.168.75.14:8010`. The detector filesystem must be mounted so its output and the controller's `/opt/aimdrc/data` refer to the intended shared data.

The MAXIMA README uses a CIFS volume called `detector` backed by `//protosystem/protoshare/data`. Provision that volume with protected deployment credentials and verify write permissions. Its embedded example password is deliberately omitted here.

```bash
MSYS_NO_PATHCONV=1 docker run \
  --name aimdrc --restart always \
  --add-host host.docker.internal:host-gateway \
  -v //c/Users/PROTO/aimdrc/src:/opt/aimdrc/src \
  -v detector:/opt/aimdrc/data \
  -d aimdrc
```

Use the actual checkout user/path. Validate mount visibility independently from acquisition. [Controller behavior](../controllers/maxima.md).

## HELIX

Install the provided host files before starting the container:

* `requirements/host/99-docker-tty.rules` → `/etc/udev/rules.d/99-docker-tty.rules`.
* `requirements/host/docker_tty.sh` → `/usr/local/bin/docker_tty.sh`, root-owned and executable.
* `requirements/host/udevadm-trigger.service` → `/etc/systemd/system/udevadm-trigger.service`, root-owned.

```bash
sudo systemctl daemon-reload
sudo systemctl enable udevadm-trigger.service
sudo systemctl start udevadm-trigger.service
```

The source deployment uses host networking, USB bus exposure and character-device rules:

```bash
docker run --name aimdrc --restart always --network=host \
  --device=/dev/ttyACM0 \
  --device-cgroup-rule='c 166:* rmw' \
  --device-cgroup-rule='c 188:* rmw' \
  --device-cgroup-rule='c 189:* rmw' \
  -v /dev/bus/usb:/dev/bus/usb \
  -v /mnt/c/Users/Administrator/Documents/HELIX:/opt/aimdrc/data \
  -v /opt/aimdrc/src:/opt/aimdrc/src \
  -d aimdrc
```

Confirm the configured device endpoints and IDs in subsystem constants, IDS peak camera support, PyVISA backend, FTDI/Thorlabs support, RTDE configuration and tracking assets. The scope's Windows `SAVE_DIR` is a separate data location; coordinate waveform transfer/storage with the instrument setup. Heating-laser code is present but inactive in the main connection list. [Controller behavior](../controllers/helix.md).

## SPHINX

The supplied SPHINX README focuses on behavior and does not provide a full vendor installation procedure. Complete common AIMDRC setup, install InView and its command server on the instrument host, and make `http://host.docker.internal:50031` reachable from the container. Verify the selected `.NMT` file on that Windows host.

Python requirements are `requests` and `labjack-ljm`. Provide the compatible LabJack native LJM runtime required by the Python binding; the supplied `requirements/os-dependencies.sh` does not install it. Verify the LabJack address/channels in `vacuum_sensor/constants.py`, load/offset calibration in `motion_stage/constants.py`, and microscope origin in `constants.py` against the commissioned instrument configuration.

Use the generic Windows container pattern with the actual SPHINX checkout path and `host.docker.internal` mapping. InView owns the measurement data location, so a generic container data mount alone does not preserve those files. Exact native driver installation and InView output configuration must come from the station's maintained vendor setup. [Controller behavior](../controllers/sphinx.md).

## COORD

Install the matching artifacts from `requirements/deps/`:

* `spinnaker-4.4.0.246-jammy-amd64-pkg.tar.gz`.
* `spinnaker_python-4.4.0.246-cp312-cp312-linux_x86_64.whl`.

Set the station image's Python build to CPython 3.12, matching the wheel's ABI and x86_64 architecture. The controller OS installer retains Rocky Linux 9 while supplying the compatible Spinnaker runtime, isolated FFmpeg 4 and C++ runtime. Do not install an unrelated package named `pyspin` from PyPI.

For the Windows/WSL host, follow the supplied camera attachment steps. In elevated PowerShell:

```powershell
winget install --interactive --exact dorssel.usbipd-win
usbipd list
usbipd bind --busid <BUSID>
```

Identify the actual Blackfly S device BUSID. Reopen PowerShell after installing usbipd-win. The bind is persistent, but attachment must be restored after reboot/disconnection. Install the supplied monitor as the `coord` account from elevated PowerShell:

```powershell
cd C:\Users\coord\aimdrc\src\api\apps\controller\requirements\host
.\install_camera_monitor.ps1
```

The monitor creates the `AIMDRC Coordinate Camera Monitor` scheduled task, locates the camera by VID:PID `1e10:4000` or description, reattaches to WSL when necessary, and restarts an existing `aimdrc` container. Supply `-BusId` only when automatic identification is ambiguous. Logs are under `C:\Users\coord\AppData\Local\AIMDRC\coordinate-camera-monitor.log`; `connect_camera.ps1` supports one-shot recovery.

The supplied Git Bash container example is:

```bash
MSYS_NO_PATHCONV=1 docker run \
  --name aimdrc --restart always \
  --add-host host.docker.internal:host-gateway \
  --privileged -v /dev/bus/usb:/dev/bus/usb \
  -v //c/Users/coord/aimdrc/src:/opt/aimdrc/src \
  -v //c/Users/coord/Documents/data:/opt/aimdrc/data \
  -d aimdrc
```

Configure camera serial/exposure/gain in `top_camera/constants.py` and calibration/geometry in `detection/constants.py`. The supplied `CALIBRATION=None` remains a commissioning limitation. [Controller behavior](../controllers/coord.md).

## Source map

AIMDRC and controller `README.md`, controller `requirements/`, AIMDRC `docker/prod/Dockerfile`, `docker/install-scripts/python.sh` and `config/settings/`. Values and commands are source-backed examples; this documentation build does not connect to devices.

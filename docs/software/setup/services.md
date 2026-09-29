---
title: "Central service setup"
status: needs-review
owner_team: software-team
primary_contact: null
last_reviewed: null
review_cycle: 6 months
safety_level: operational
tags: [software, controls]
---

# Central service setup

Use the supplied Dockerfiles and configuration files as the deployment baseline. Build and run the services in the sequence described on the [setup overview](index.md).

## Common build preparation

For each repository, inspect the selected `docker/local/Dockerfile` or `docker/prod/Dockerfile`. Set `max_cores` for dependency compilation and `<service>_uid` to the intended host user ID (`id -u`). Build arguments can be supplied without editing line-number-specific Dockerfile locations:

```bash
docker build ~/aimdas -f ~/aimdas/docker/local/Dockerfile -t aimdas --build-arg aimdas_uid="$(id -u)"
docker build ~/aimdds -f ~/aimdds/docker/local/Dockerfile -t aimdds --build-arg aimdds_uid="$(id -u)"
docker build ~/aimdrm -f ~/aimdrm/docker/local/Dockerfile -t aimdrm --build-arg aimdrm_uid="$(id -u)"
```

Use the matching local settings and certificates. The following commands retain the source READMEs' bridge-address assumptions; change them to actual host networking.

## AIMDAS local

```bash
docker run \
  --name aimdas \
  --add-host aimd.test:127.0.0.1 \
  --add-host db.aimd.test:172.17.0.2 \
  --add-host ds.aimd.test:172.17.0.4 \
  -v ~/aimdas/src:/opt/aimdas/src \
  -d aimdas
```

Open `https://aimd.test` after configuring host DNS/hosts and local certificate trust. The container example does not publish a host port; host-to-container connectivity must be configured. The source README supplies `chipmk/tap/docker-mac-net-connect` for its macOS bridge workflow.

Enter with `docker exec -it --user aimdas aimdas bash`. Angular code is under `/opt/aimdas/src/ng/`; builder logs are `/opt/aimdas/logs/ng/builder_log`. The README notes that SASS errors can leave the builder stuck; fix the error and run `ng build` from the Angular directory.

## AIMDDS local

```bash
docker run \
  --name aimdds \
  --add-host db.aimd.test:172.17.0.2 \
  --add-host ds.aimd.test:172.17.0.4 \
  --add-host rm.aimd.test:172.17.0.5 \
  -v ~/aimdds/data:/opt/aimdds/data \
  -v ~/aimdds/src:/opt/aimdds/src \
  -v ~/shibboleth:/opt/aimdds/shib \
  -d aimdds
```

Run initial Django setup as the service user inside the container:

```bash
docker exec -it --user aimdds aimdds bash
cd /opt/aimdds
. venv/bin/activate
./src/api/manage.py migrate
./src/api/manage.py collectstatic
./src/api/manage.py createsuperuser
./src/api/scripts/init_api.local.py
```

Inspect initialization-script inputs before first use; initialization is separate from routine restart. The README also lists `makemigrations`; generate migrations when intentionally changing models, and use checked-in migrations for deployment. Confirm `https://ds.aimd.test/admin/` and application authentication.

```bash
./src/api/manage.py test --debug-mode
/home/aimdds/celery-restart.sh
/home/aimdds/daphne-restart.sh
```

The last two commands restart background processes; use them when maintaining those services, not as mandatory steps after every test.

## AIMDRM local

```bash
docker run \
  --name aimdrm \
  --add-host ds.aimd.test:172.17.0.4 \
  -v ~/aimdrm/src:/opt/aimdrm/src \
  -d aimdrm

docker exec -it --user aimdrm aimdrm bash
cd /opt/aimdrm
. venv/bin/activate
./src/api/manage.py collectstatic
./src/api/manage.py test --debug-mode
```

Configure the robotics endpoint, namespace and manager certificates in the selected settings. The local schema UI is `https://rm.aimd.test/api/schema/swagger-ui/`. `/home/aimdrm/opcua-restart.sh` restarts the OPC UA process and rebuilds its volatile state.

## Production configuration

On the central host, the READMEs use `/opt/aimdas`, `/opt/aimdds` and `/opt/aimdrm` checkouts. Select production Django settings for the Python services:

```bash
ln -sf /opt/aimdds/src/api/config/settings/prod.py /opt/aimdds/src/api/config/settings/main.py
ln -sf /opt/aimdrm/src/api/config/settings/prod.py /opt/aimdrm/src/api/config/settings/main.py
```

Populate the protected `/opt/env/prod.env` using the settings' required environment variables:

| Variable | Consumer / purpose |
| --- | --- |
| `AIMDDB_PASSWORD` | AIMDDS PostgreSQL connection |
| `AIMDDS_DJANGO_SECRET_KEY` | AIMDDS Django signing key |
| `AIMDRM_DJANGO_SECRET_KEY` | AIMDRM Django signing key |
| `AIMDRM_SECRET` | Shared AIMDDS/AIMDRM service authentication |
| `AIMDDS_HOST_IP` | AIMDRM data-service host configuration |
| `OPCUA_ROBOTICS_HOST_IP` | AIMDRM robotics endpoint |
| `DATA_PORTAL_SECRET` | Data-portal inbound service authentication |
| `DATA_PORTAL_TOKEN` | AIMDDS outbound data-portal access |
| `SLACK_WEBHOOK_URL` | Base AIMDDS notification setting; review environment-specific overrides |

Inspect environment overrides rather than assuming every base setting is honored; the supplied production AIMDDS settings include a notification override. Do not publish its credential.

Build each production image using `docker/prod/Dockerfile`. The source deployment commands are:

```bash
docker build /opt/aimdas -f /opt/aimdas/docker/prod/Dockerfile -t aimdas
docker build /opt/aimdds -f /opt/aimdds/docker/prod/Dockerfile -t aimdds
docker build /opt/aimdrm -f /opt/aimdrm/docker/prod/Dockerfile -t aimdrm

docker run --name aimdas \
  --add-host ds.aimd.hemi.jhu.edu:172.17.0.4 \
  -p 3443:443 \
  -v /opt/aimdas/src:/opt/aimdas/src \
  -v /etc/ssl/certs:/opt/aimdas/src/certs/prod \
  -v /etc/ssl/private:/opt/aimdas/src/private/prod \
  -d aimdas

docker run --name aimdds \
  --add-host db.aimd.hemi.jhu.edu:172.17.0.2 \
  --add-host rm.aimd.hemi.jhu.edu:172.17.0.5 \
  --env-file /opt/env/prod.env -p 4443:443 \
  -v /opt/aimdds/data:/opt/aimdds/data \
  -v /opt/aimdds/src:/opt/aimdds/src \
  -v /etc/shibboleth:/opt/aimdds/shib \
  -v /etc/ssl/certs:/opt/aimdds/src/certs/prod \
  -v /etc/ssl/private:/opt/aimdds/src/private/prod \
  -d aimdds

docker run --name aimdrm \
  --add-host ds.aimd.hemi.jhu.edu:172.17.0.4 \
  --env-file /opt/env/prod.env -p 4843:4843 -p 5443:443 \
  -v /opt/aimdrm/src:/opt/aimdrm/src \
  -v /etc/ssl/certs:/opt/aimdrm/src/certs/prod \
  -v /etc/ssl/private:/opt/aimdrm/src/private/prod \
  -d aimdrm
```

Run the AIMDDS migration/static/superuser steps using production configuration and `init_api.prod.py` when bootstrapping that environment. Configure the host reverse proxy from AIMDAS `docker/prod/host/httpd/`; its README identifies ports 80, 443 and 4843 and the SELinux `httpd_can_network_connect` setting. Configure Postfix from the adjacent host configuration if using those notification routes. These host changes require matching local infrastructure policy.

## Cameras and go2rtc

AIMDAS uses a separate go2rtc container. The supplied production invocation is:

```bash
docker run -d --name go2rtc -p 1984:1984 \
  --env-file /opt/env/go2rtc.env \
  -v /opt/aimdas/docker/prod/go2rtc/go2rtc.yaml:/config/go2rtc.yaml:ro \
  ghcr.io/alexxit/go2rtc:latest
```

For local use, the README uses `~/aimdas/docker/local/go2rtc/go2rtc.env` and the matching YAML path. Configure actual camera credentials through the environment file. This streaming service does not substitute for the controller SDK camera setup.

## Logs and process maintenance

| Service | Paths / commands |
| --- | --- |
| AIMDAS | `/opt/aimdas/logs/ng/builder_log`; production rebuild `/home/aimdas/ng-rebuild.sh` |
| AIMDDS HTTP | `/opt/aimdds/logs/httpd/logs/api.error_log` |
| AIMDDS Celery | `/opt/aimdds/logs/celery/async.log`; `/home/aimdds/celery-restart.sh` |
| AIMDDS Daphne | `/opt/aimdds/logs/daphne/error.log`; `/home/aimdds/daphne-restart.sh` |
| Shibboleth | `/var/log/shibboleth/shibd.log` |
| AIMDRM HTTP | `/opt/aimdrm/logs/httpd/logs/api.error_log` |
| AIMDRM OPC UA | `/opt/aimdrm/logs/opcua/server.log`, `client.log`, `robotics-client.log` |

Use `docker container stop <service>` and `docker container start <service>` for container lifecycle management. Refer to [recovery](../operations/data-and-recovery.md) before restarting a manager with active hardware state.

## Source map

AIMDAS/AIMDDS/AIMDRM `README.md`, `docker/`, and Python `config/settings/`. Deployment values above are source examples, not observations of the running lab.

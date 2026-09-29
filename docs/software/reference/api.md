---
title: "HTTP and WebSocket API"
status: needs-review
owner_team: software-team
primary_contact: null
last_reviewed: null
review_cycle: 12 months
safety_level: informational
tags: [software, controls]
---

# HTTP and WebSocket API

This reference inventories the explicitly implemented view actions in the supplied sources. Paths include the trailing slash. It does not imply generic CRUD support: an absent `PUT`, `DELETE` or detail `GET` is not implemented merely because a router registers the resource.

Production AIMDDS base URL: `https://ds.aimd.hemi.jhu.edu`. Local base URL: `https://ds.aimd.test`. Production AIMDRM base URL: `https://rm.aimd.hemi.jhu.edu`.

## Authentication

| Caller | Scheme and scope |
| --- | --- |
| Browser | HttpOnly `access_token` cookie; configured OAuth2 authentication also accepted for ordinary resources |
| AIMDRM → AIMDDS | `Authorization: Bearer <AIMDRM_SECRET>` for run/status/error/transform writes |
| AIMDDS → AIMDRM | Shared `AIMDRM_SECRET`; manager API is for trusted service callers |
| Data portal → AIMDDS | `DATA_PORTAL_SECRET` authentication for sample creation/deletion; optional on reads |

AIMDDS defaults to `IsAuthenticated`. Additional role and ownership checks appear below. `SYS` and `ADMIN` are distinct profile roles.

| Authentication route | Method | Behavior |
| --- | --- | --- |
| `/auth/login/` | POST | OAuth2 token issuance with session cookies for local development; returns 401 when DEBUG is false |
| `/auth/logout/` | POST | Revoke cookie token and clear session cookies |
| `/auth/sso/` | GET | Federated sign-in using trusted upstream Shibboleth headers |
| `/auth/` delegated routes | Provider-defined | Includes `oauth2_provider.urls`; exact DOT subroutes depend on the installed dependency |

## API schemas and admin

AIMDDS and AIMDRM register GET `/api/schema/`, `/api/schema/swagger-ui/` and `/api/schema/redoc/`. AIMDDS also mounts Django admin at `/admin/`. Production manager schema access is service-authenticated; its README expects an unauthenticated request to return 401. Use the deployed schema for dependency-specific fields and renderer behavior.

## Base resources

| Method | Path | Access / condition | Operation |
| --- | --- | --- | --- |
| POST | `/base/appointment/` | Authenticated | Create an appointment. |
| GET | `/base/appointment/` | Authenticated | Get the appointments. |
| GET | `/base/appointment/<id>/` | Authenticated | Get an appointment. |
| PATCH | `/base/appointment/<id>/` | Owner | Update an appointment. |
| DELETE | `/base/appointment/<id>/` | Owner | Delete an appointment. |
| POST | `/base/appointment/<appointment_id>/comment/` | Authenticated | Create an appointment comment. |
| DELETE | `/base/appointment/<appointment_id>/comment/<id>/` | Owner | Delete an appointment comment. |
| POST | `/base/media-file/` | SYS | Create a media file. |
| GET | `/base/media-file/` | Authenticated | Get the media files. |
| GET | `/base/media-file/<id>/` | Authenticated | Get a media file. |
| GET | `/base/media-file/<id>/data/` | Authenticated | Download a media file. |
| PATCH | `/base/media-file/<id>/` | SYS + owner | Update a media file. |
| DELETE | `/base/media-file/<id>/` | SYS + owner | Delete a media file. |
| POST | `/base/profile/` | ADMIN | Create a profile. |
| GET | `/base/profile/` | ADMIN | Get the profiles. |
| GET | `/base/profile/<id>/` | Self or ADMIN | Get a profile. |
| PATCH | `/base/profile/<id>/` | ADMIN | Update a profile. |
| POST | `/base/sample/` | Data portal service | Create a sample. |
| GET | `/base/sample/` | Authenticated | Get the samples. |
| GET | `/base/sample/<id>/` | Authenticated | Get a sample. |
| DELETE | `/base/sample/<id>/` | Data portal service | Delete a sample. |

## System resources

| Method | Path | Access / condition | Operation |
| --- | --- | --- | --- |
| POST | `/sys/coordinate-transform/` | AIMDRM service | Persist a coordinate transform submitted by AIMDRM. |
| GET | `/sys/coordinate-transform/` | Authenticated | Return coordinate-transform history. |
| GET | `/sys/coordinate-transform/<id>/` | Authenticated | Return one coordinate-transform record. |
| POST | `/sys/run/` | SYS | Create a sample run. |
| GET | `/sys/run/` | Authenticated | Get the sample runs. |
| GET | `/sys/run/<id>/` | Authenticated | Get a sample run. |
| PATCH | `/sys/run/<id>/` | AIMDRM service | Update a sample run. |
| PATCH | `/sys/run/<id>/cancel/` | SYS; nonterminal, not canceling | Cancel a sample run. |
| PATCH | `/sys/run/<id>/clear/` | SYS; terminal | Clear a sample run from the run manager. |
| PATCH | `/sys/run/<id>/pause/` | Unsupported (403) | Pause a sample run. |
| PATCH | `/sys/run/<id>/resume/` | Unsupported (403) | Resume a paused sample run. |
| POST | `/sys/run/<run_id>/error/` | AIMDRM service | Create a sample run error. |
| PATCH | `/sys/run/<run_id>/error/<id>/` | AIMDRM service; active occurrence | Update a sample run error. |
| GET | `/sys/run/<run_id>/error/` | Registered but defective; see below | Get the sample run errors. |
| POST | `/sys/run/<run_id>/note/` | SYS | Create a sample run note. |
| PATCH | `/sys/run/<run_id>/note/<id>/` | SYS + owner | Update a sample run note. |
| DELETE | `/sys/run/<run_id>/note/<id>/` | SYS + owner | Delete a sample run note. |
| PATCH | `/sys/run/<run_id>/status/<id>/` | AIMDRM service | Update a run sample's instruction status. |
| POST | `/sys/run-script/` | SYS | Create a run script. |
| GET | `/sys/run-script/` | Authenticated | Get the run scripts. |
| GET | `/sys/run-script/<id>/` | Authenticated | Get a run script. |
| GET | `/sys/run-script/<id>/data/` | Authenticated | Get a run script file. |
| PATCH | `/sys/run-script/<id>/` | SYS | Update a run script. |
| DELETE | `/sys/run-script/<id>/` | SYS | Delete a run script. |
| PATCH | `/sys/station/<id>/` | SYS | Update a station. |
| PATCH | `/sys/restart/` | SYS; no nonterminal database runs | Restart the run manager's OPC UA server. |


`<id>` is normally an integer database primary key; a sample ID is a hexadecimal string representing the external sample identifier. A station `<id>` is the physical station number, 1–6. Nested routes also carry the parent ID shown in the path.

### Current nested-error list defect

`RunError.list(self, request)` is registered beneath `run/<run_id>/error` but does not accept the router's `run_pk` keyword, and its queryset is not filtered by that parent. Treat this as a source defect, not a working run-scoped list contract. Run detail serialization includes the run's related errors. No backend fix is included in this documentation change.

## Important request and response contracts

| Resource | Request fields / constraints | Response behavior |
| --- | --- | --- |
| Run create | `script` ID, `infeed`, `outfeed`, `samples` slot-to-ID object; initial `status` is `INIT` | Expanded script metadata, selected samples and run status; normal start response is 200 |
| Run patch | Trusted service status updates; other run inputs are immutable | Terminal transitions set end time once; terminal records reject further status mutations |
| Run script create | Multipart `file`, `name`; schema and instruction metadata derived from file | Metadata includes `schema_version`, `requires_initial_transform`, instruction line ranges, size and counts |
| Run script patch | Metadata only | File content replacement rejected |
| Coordinate transform create | `sample_instruction_status`, `algorithm_version`, finite 2×2 `matrix`, 2-value `translation`, nonnegative finite `rms_error_mm` | 201 for new record; 200 with existing record on repeated instruction-status submission |
| Error create | `error_code`, optional `details`; `active` must be true and `acked` false | Canonical severity/message/source/recommended action derived from registry |
| Error patch | `active` and `acked` only | Only an active occurrence may be updated |
| Run note | `content` | Creator and timestamps supplied by service |
| Station patch | Optional Boolean `enabled`, `robot_auto` | Command submission; inspect live station state for effect |
| Media create | Multipart upload; see `MediaFileSerializer` for metadata | Separate metadata and `/data/` download responses |
| Profile | Profile/user fields and roles | Administrator writes; detail reads limited to self/admin |
| Sample | External sample ID and IGSN metadata | Detail combines local history and data-portal data |

Example run-create JSON, using illustrative identifiers that must be replaced:

```json
{
  "script": 123,
  "infeed": 5,
  "outfeed": 5,
  "status": "INIT",
  "samples": {"0": "000000000000000000000001"}
}
```

AIMDDS starts the run inside the database transaction. An upstream exception rolls back database creation, but a network failure after remote acceptance is not a distributed rollback. Inspect system state before blindly retrying a start.

## Filtering, sorting and paging

List endpoints using `filter_sort_slice()` return `{begin, end, total, results}`. `begin` is a zero-based offset; page size comes from `QUERY_SLICE_SIZE`; `all=true` disables slicing. `order` is a comma-separated field list with `-` for descending order. Omitting `order` retains the queryset's ordering.

Field filters use supported Django-style paths, for example `igsn__icontains=TEST` or `schema_version=2`. Integers, decimals and Booleans are coerced and invalid values produce 400 errors. `q` is a comma-separated list of **filter keys** to OR together; it is not arbitrary full-text search. Keys outside `q` are ANDed.

```text
/base/sample/?igsn__icontains=TEST&order=igsn&begin=0
/sys/run-script/?schema_version=2&order=-date_modify
```

The documentation-only query serializer advertises `simple`, but the shared filtering helper does not implement it as a reserved parameter. Do not assume it works on every list route. Appointment listing has its own time-range handling; inspect its view/schema for the booking query.

## AIMDRM service API

| Method | Path | Payload | Behavior |
| --- | --- | --- | --- |
| POST | `/rms/run/` | Multipart `id`, `infeed`, `outfeed`, `samples`, `script`, `statuses`, `transforms` | Create OPC UA nodes and await preload/start result |
| PATCH | `/rms/run/<id>/` | `{"operation":"cancel"}` or `clear`, `pause`, `resume` | Submit operation; pause/resume remain stubs |
| PATCH | `/rms/station/<station_no>/` | Boolean `enabled` and/or `robot_auto` | Submit physical-station settings |
| PATCH | `/rms/restart/` | No required body | Spawn manager restart script |

`samples` maps buffer-slot keys to serialized sample objects, `statuses` maps sample IDs to ordered instruction-status IDs, and `transforms` maps sample IDs to initial canonical transforms. JSON fields are encoded within the multipart request. The script is a file upload, not a database ID on this internal endpoint.

## WebSocket routes

Use `wss://ds.aimd.hemi.jhu.edu` (or the configured local host).

| Path | Message behavior |
| --- | --- |
| `/wss/sys/run/<run_id>/` | Authorized service publish triggers fresh `RunDetailSerializer` data from the database |
| `/wss/sys/status/` | Relays manager system-state payload: active runs, stations, buffers, conveyor |
| `/wss/base/appointments/` | Appointment refresh/broadcast channel |

Ordinary clients receive updates. Service-user checks restrict publishing; an unauthorized publisher is closed with 4403. Authentication and origin middleware remain part of the deployment boundary. WebSocket messages are not a persistent event log and do not provide replay of every transition.

## Failures

Validation errors generally return 400; permission/role failures 403; missing records 404; occupied buffer preload 409; exhausted transient upstream requests may return 504. Source-specific structured start errors also carry `code`, `detail` and optional metadata. Outbound retry helpers retry connection/timeouts and 5xx responses with bounded backoff; 4xx responses are returned without retry.

These HTTP statuses and symbolic start-error strings are separate from the numeric [hardware/control error catalog](error-codes.md).

## Source map

AIMDDS `config/urls.py`, `config/routing.py`, `apps/{auth,base,system}/urls.py`, `views.py`, `serializers.py`, `apps/utils.py`; AIMDRM `apps/rms/{urls,views,serializers}.py` and `apps/opcua/admin_client.py`. [Source snapshot](source-snapshot.md).

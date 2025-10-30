# File: docs/api-edgelink-gateway.md
---
title: API Spec — EdgeLink IoT Gateway
owner: iot@techco
status: review
last-updated: 2025-06-28
tags: [API, IoT Core, MQTT, REST, Auth]
---

## Protocols
- Device telemetry: MQTT via **AWS IoT Core** (`devices/{deviceId}/telemetry`).
- Control plane: REST via API Gateway → Lambda.

## Auth
- Devices: IoT X.509 certs; thing policy scoped to deviceId.
- Control: Cognito user pools + JWT.

## REST Endpoints
- `POST /v1/devices/{id}/commands` — send command.
- `GET /v1/devices/{id}/shadow` — fetch desired/reported state.
- `GET /v1/firmware/releases` — list OTA artifacts.

### Example: Send Command
```http
POST /v1/devices/abc123/commands
{
  "name": "set_threshold",
  "params": { "temp": 72 }
}
```

## MQTT Topics
- Telemetry pub: `devices/{id}/telemetry`
- Shadow delta sub: `$aws/things/{id}/shadow/update/delta`

## Quotas
- Telemetry ≤ 5 msgs/sec/device; payload ≤ 64 KB.
- Commands fan-out limited to 50 devices/request.

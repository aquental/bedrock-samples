# File: docs/observability-standard.md
---
title: Observability Standard — App & RAG
owner: sre@techco
status: approved
last-updated: 2025-07-03
tags: [Observability, CloudWatch, X-Ray, OTEL]
---

## Logging
- JSON logs with fields: `tenantId`, `requestId`, `model`, `topK`, `latencyMs`, `tokenIn`, `tokenOut`.
- PII redaction before emit.

## Tracing
- OpenTelemetry SDK → X-Ray; spans for `retrieve` and `generate`.

## Metrics
- `Rag/RetrievalHitRate`, `Rag/EmptyRetrievals`, `Rag/CitationCount`.
- SLO dashboard with burn-rate alerts.

## Sampling
- 100% errors, 10% success; adjustable via env var.

## Dashboards
- Per-tenant latency heatmap.
- Cost per 100 queries (join with usage).

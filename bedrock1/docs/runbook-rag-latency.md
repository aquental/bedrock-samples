# File: docs/runbook-rag-latency.md
---
title: Runbook — Elevated RAG Latency
owner: sre@techco
status: approved
last-updated: 2025-07-20
tags: [Runbook, SRE, Latency, Bedrock]
---

## Symptoms
- P95 > 2.5s for `/ask`.
- Timeouts from model runtime or retrieval.

## Dashboards
- CloudWatch `API/Latency`, `Retrieval/TopK`, `Model/InferenceTime`.
- X-Ray traces tagged `component=rag`.

## Triage Steps
1. Check regional throttling in Bedrock service quotas.
2. Verify OpenSearch collection health; shard/segment pressure.
3. Inspect recent deploys; rollback if regression aligned.
4. Reduce `top_k` by 2 and disable rerank temporarily.
5. Enforce circuit breaker → respond with last cached answer if hit rate > 0.6.

## Common Fixes
- Increase OpenSearch capacity and refresh interval.
- Trim prompt/system text; enforce 3500 token budget.
- Batch embed re-ingestion off peak (nightly).

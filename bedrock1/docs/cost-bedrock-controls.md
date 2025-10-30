# File: docs/cost-bedrock-controls.md
---
title: Cost Controls — Bedrock & Retrieval
owner: finops@techco
status: approved
last-updated: 2025-07-18
tags: [FinOps, Cost, Bedrock, Quotas]
---

## Strategy
- **Tiered models**: default mid-tier model; auto-escalate for “critical” intents only.
- **Prompt budget**: cap at 3500 tokens; truncate context by score.
- **Top-k policy**: 8→5 during load spikes; disable rerank if P95 > target.
- **Caching**: hash(question+filters) → DynamoDB (TTL 60m) for FAQ-like queries.
- **Budgets & Alerts**: AWS Budgets on Bedrock usage; anomaly detection via Cost Explorer.

## Governance
- Change to model family requires FinOps review.
- Every new source ingested must specify retention and freshness policy.

## Example Quota Guard (pseudocode)
```json
{
  "maxRequestsPerMinute": 900,
  "maxTokensPerMinute": 120000,
  "actionOnBreach": "shed_load"
}
```

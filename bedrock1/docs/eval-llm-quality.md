# File: docs/eval-llm-quality.md
---
title: Evaluation Plan — Answer Quality & Safety
owner: ml-eval@techco
status: draft
last-updated: 2025-07-12
tags: [Evaluation, QA, Safety, Bedrock]
---

## Test Set
- 300 questions across 8 intents (billing, setup, limits, account).
- 20% adversarial (trick wording, unsupported topics).
- Each item includes canonical answer + valid citations.

## Metrics
- **Answer F1** vs canonical.
- **Citation Coverage** (% with ≥1 correct source).
- **Hallucination Rate** (manual adjudication).
- **Safety Violations** (guardrail triggers).
- Cost per 100 queries.

## Procedure
1. For each item, run retrieve+generate, collect JSON outputs.
2. Score automatically where possible; sample 15% for human review.
3. Track regressions per commit; block deploys over thresholds.

## Thresholds (v1)
- F1 ≥ 0.72, Citation ≥ 0.9, Hallucinations ≤ 0.03.

## Tooling
- Offline harness (Lambda invoked by Step Functions) + Athena for results rollup; QuickSight dashboard.

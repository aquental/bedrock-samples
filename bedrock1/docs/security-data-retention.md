# File: docs/security-data-retention.md
---
title: Data Classification & Retention
owner: compliance@techco
status: approved
last-updated: 2025-07-01
tags: [Policy, Security, Retention]
---

## Classification
- **Public**, **Internal**, **Restricted**, **Regulated**.

## Retention
- Chat transcripts: 90 days Internal; redact PII at ingest.
- Training/eval datasets: 1 year Internal.
- Audit logs: 7 years Regulated.

## Storage
- S3 bucket per class with KMS keys and lifecycle rules.
- Access via IAM conditions on `aws:RequestTag/classification`.

## Disposal
- S3 Object Lock + retention mode for regulated records.
- Cryptographic erasure by key rotation where supported.

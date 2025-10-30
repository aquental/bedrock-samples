# File: docs/tenant-isolation-strategy.md
---
title: Multi-Tenant Isolation Strategy
owner: security@techco
status: review
last-updated: 2025-07-08
tags: [Security, SaaS, KMS, IAM, S3, DynamoDB]
---

## Isolation Layers
- **Identity**: tenant-scoped IAM roles; STS session tags `tenantId`.
- **Data**:
  - S3 prefixes `tenants/{id}/...` + bucket policies on `s3:prefix`.
  - DynamoDB composite key `{tenantId, sortKey}`.
  - OpenSearch: filter clause `tenantId = :id`.
- **Crypto**: KMS per-tenant CMKs; grants only to tagged roles.

## Example: IAM Condition (snippet)
```json
{
  "Condition": { "StringEquals": { "aws:PrincipalTag/tenantId": "${aws:ResourceTag/tenantId}" } }
}
```

## Testing
- Canary tests impersonate each tenant and attempt cross-read; must fail.
- Audit with CloudTrail Lake queries by `tenantId`.

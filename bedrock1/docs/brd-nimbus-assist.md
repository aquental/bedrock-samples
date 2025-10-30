# File: docs/brd-nimbus-assist.md
---
title: Business Requirements — Nimbus Assist (AI Support Agent)
owner: cx-platform@techco
status: draft
last-updated: 2025-07-14
tags: [BRD, Support, Bedrock, RAG]
---

## Summary
Nimbus Assist reduces human ticket volume by answering customer questions using curated internal knowledge. It must deliver fast, accurate, citeable answers and hand off seamlessly to humans.

## Problems
- 32% of tickets are “known answers” buried in wikis/Runbooks.
- Agents spend 18–25 minutes searching per ticket.

## Users & Use Cases
- **Customers**: self-service answers in-app and on the help center.
- **Agents**: suggested replies inside Zendesk.
- **Compliance**: exported citations for audits.

## Success Metrics (90 days post-launch)
- ≥35% deflection on Tier-0/Tier-1 topics.
- ≥4.3/5 answer helpfulness (in-product thumbs).
- ≤2% unresolved due to hallucinations (spot-check sample).
- P50 latency ≤ 1200 ms; P95 ≤ 2500 ms.

## High-Level Requirements
- Retrieval-augmented generation (RAG) with **Bedrock Knowledge Bases**.
- Answer must include top 1–3 citations.
- Guardrails for PII leakage and unsupported topics.
- Multilingual (EN primary; ES/DE fallback).
- Admin console for source curation and eval dashboards.

## Constraints
- Data residency: primary in eu-west-1.
- No cross-tenant leakage (multi-tenant SaaS).

## Non-Functional
- SLO: 99.9% availability (monthly).
- Security: KMS-encrypted at rest; TLS 1.2+ in transit.

# File: docs/prd-nimbus-assist-v1.md
---
title: PRD — Nimbus Assist v1
owner: product@techco
status: draft
last-updated: 2025-07-15
tags: [PRD, Support, Bedrock, RAG]
---

## Goals
Deliver a production AI assistant that answers customer questions from curated sources with citations and safe content handling.

## v1 Scope
- **Sources**: S3 docs, product manuals, runbooks (Markdown/PDF/HTML).
- **Retrieval**: Bedrock Knowledge Bases with OpenSearch Serverless vector index.
- **Generation**: Bedrock-hosted model (family configurable) with system prompt and JSON-serializable citations.
- **Guardrails**: Block payment/credential collection; redact PII in prompts.
- **Channels**: Web widget (React), Agent assist (Zendesk macro + sidebar).
- **Observability**: Request/response traces, retrieval debug view, feedback buttons.

## Out of Scope
- Voice, mobile SDKs, automatic translation quality guarantees.

## Metrics
- Deflection %, answer rating, citation coverage %, latency (P50/P95), cost per 100 sessions.

## Acceptance Criteria
- Answers include at least one valid citation.
- Admin can enable/disable sources and re-ingest content.
- Latency budgets enforced via circuit breaker.

## Release Plan
- Beta: internal help center.
- GA: all help center + agent assist for Tier-1 queues.

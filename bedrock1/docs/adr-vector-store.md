# File: docs/adr-vector-store.md
---
title: ADR-017 — Vector Store: OpenSearch Serverless vs Aurora pgvector
owner: architecture@techco
status: accepted
decided: 2025-07-10
tags: [ADR, OpenSearch, Aurora, Vector]
---

## Context
RAG for Nimbus Assist needs hybrid (sparse + dense) retrieval, filtering, and serverless scale.

## Decision
Adopt **OpenSearch Serverless** with Bedrock Knowledge Bases integration.

## Rationale
- Native hybrid search (BM25 + kNN) with filters.
- No index servers to manage; scales with traffic.
- Bedrock KB supports automated ingestion and re-chunking.

## Consequences
- SQL-style joins not available; denormalize metadata at ingest.
- Index warm-up may add minutes after schema changes.
- Keep Aurora PostgreSQL for transactional data, not vector search.

## Alternatives Considered
- **Aurora pgvector**: strong transactional joins; weaker hybrid search and operational overhead for scale.
- **Self-managed Elasticsearch**: more control; non-serverless, higher ops burden.

# Tech Company Inc. — Sample Knowledge Base Corpus

This archive contains 12 short Markdown documents suitable for ingestion into **AWS Bedrock Knowledge Bases** as a Retrieval-Augmented Generation (RAG) dataset.

- Location: `docs/`
- Format: `.md` with light front-matter and clear sections
- Mix of BRD/PRD/design/ADR/runbook/policies and more
- AWS-forward content plus a couple non-AWS policies for negative/control cases

Suggested ingestion hints:
- Chunk size 1200–1800 tokens with ~150 overlap
- Metadata: parse `title`, `tags`, `owner`, `status`, `last-updated` from the header block
- Recommended filters: `tags`, `owner`, `status`

Have fun stress-testing retrieval, citations, and guardrails.

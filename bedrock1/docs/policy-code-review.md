# File: docs/policy-code-review.md
---
title: Engineering Policy — Code Review
owner: eng-leadership@techco
status: approved
last-updated: 2025-06-30
tags: [Policy, Process, Non-AWS]
---

## Purpose
Ensure maintainable, secure, and well-tested code.

## Requirements
- Every PR requires two approvals or one from a code owner.
- Tests and lint must pass before review.
- PR description must include risk, rollback plan, and screenshots for UI changes.

## Review Guidelines
- Focus on correctness, readability, and blast radius.
- Prefer small, incremental PRs (< 400 lines diff).
- Block on security and data-handling issues.

## SLA
- First response ≤ 4 working hours; merge within 2 business days unless blocked.

## Anti-Patterns
- Drive-by nitpicks without suggestions.
- “LGTM” without rationale.

---
title: Paid research participation Data Product Charter
status: local-source-pilot
created: 2026-08-08
updated: 2026-09-07
tags: [template, data-engineering, data-product, governance]
description: Outcome, consumers, ownership, contract, quality, privacy, and operating boundary for a data product.
---

# Data Product Charter

## Document control

| Field | Value |
|---|---|
| Data product ID/version | book-paid-study-data / paid_study.v1 |
| Product owner | bookchaowalit |
| Data owner/steward | bookchaowalit |
| Producer team | Domain repository |
| Status/review date | Local source pilot / 2026-09-07 |
| Evidence boundary | schema.json, demo.json, source policy, capture adapter and tests in this repository |

## Product contract

- Decision or user outcome: Find compensated participation with screening, time and privacy terms.
- Consumers and use cases: Discovery applications; integration planned.
- Source systems and lake layers: Prolific, Respondent, UserTesting, YouGov and NIH public participant or policy pages → landing → Bronze; synthetic fixtures remain for offline contract tests.
- In scope/out of scope: Public study listings only; personal screening answers and health records never enter this product.
- Freshness, availability, and volume expectation: Source capture is manually reviewed no more than once per six hours; the page documents platform terms rather than a current study inventory, so availability remains unknown; open filter rejects checks older than 72h; no live SLA.
- Data classification, residency, retention, and access: Public platform metadata; raw bytes stay in the private local operational lake; no user profile, screening answer, study response or health record.
- Quality thresholds and incident route: All contract tests pass; live quality/replay gates pending; owner handles source failures.
- Cost/capacity guardrail: Offline only, zero provider calls; max 10,000 records per envelope.
- Versioning, deprecation, and migration policy: Draft v1; breaking changes version separately; no legacy migration or live consumer yet.

## Acceptance and ownership

| Gate | Evidence | Owner | Result/status |
|---|---|---|---|
| Contract | Versioned schema and compatibility rules | bookchaowalit | Passed locally |
| Quality | Checks and threshold report | bookchaowalit | Contract and source tests pass |
| Lineage | Source-to-consumer map | bookchaowalit | Captured landing/Bronze lineage verified |
| Access/privacy | Classification and access review | bookchaowalit | Public read; no participant payloads |
| Operations | Runbook, alert, replay, and recovery | bookchaowalit | Manual capture/replay verified |

## Approval

| Role | Name/date | Decision |
|---|---|---|
| Product/data owner |  | Approve charter / revise |
| Producer owner |  | Accept delivery boundary |
| Consumer representative |  | Accept use and SLA |

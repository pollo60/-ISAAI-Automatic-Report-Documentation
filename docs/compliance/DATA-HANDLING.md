# Data handling and pseudonymization

## Default rule

**Pseudonymize before any payload is sent to an internal LLM or external AI API.**

## Categories to pseudonymize

| Category | Examples in ISAAI scope | Treatment |
|----------|-------------------------|-----------|
| Person names | Analyst identifiers, mail recipients | Replace with `USER_###` |
| Account / entity IDs | Counterparty codes in invoices | Hash or tokenize |
| Mail addresses | Distribution lists | Replace with `DL_###` |
| File paths with org structure | Internal SharePoint paths | Generic bucket names |
| Free-text email bodies | Summary mails | Strip or summarize |

## Invoice module (ISA)

- OCR output: redact IBAN, tax IDs, personal signatures before model inference.
- Charts for presentation: aggregate only; no row-level PII in prompts.

## Financial report module (A+I)

- XML: retain structure and numeric thresholds; replace party identifiers with tokens.
- Exception reports: store pseudonymized copy for AI draft review; retain full copy only in controlled mock DMS.

## Logging

- No raw PII in CI logs or GitHub Actions output.
- Use `X-Request-Id` correlation without embedding personal data (see OpenAPI mocks).

## Status

Production DLP and LLM gateway policies are **stakeholder-owned** — this document defines project defaults until interfaces are confirmed.

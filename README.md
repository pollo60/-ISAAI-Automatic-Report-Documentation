# ISAAI Project — Automatic Report Documentation

Primary focus: daily automation of **Report A** and **Report B** XML financial-report validation (**A+I**). Parallel university track: exchange-invoice OCR and charts (**ISA**).

## Canonical layout

| Path | Contents |
|------|----------|
| [`docs/Documentation/`](docs/Documentation/) | ArchiMate, BPMN, university & stakeholder requirements |
| [`docs/compliance/`](docs/compliance/) | Audit trail, data handling, stakeholder interface Q&A |
| [`docs/api/openapi/`](docs/api/openapi/) | OpenAPI v3 mock specifications |
| [`src/isa/`](src/isa/) | ISA module (planned): PDF/OCR, charts |
| [`src/ai/`](src/ai/) | A+I module (planned): XML parser, GOAL validation |
| [`presentations/`](presentations/) | Boardroom deck and narrative |
| [`Project Charter.html`](Project%20Charter.html) | Living project charter (HTML, DE) |
| [`Project-Charter-ISAAI.tex`](Project-Charter-ISAAI.tex) | Project charter (English LaTeX, Report A/B focus) |
| [`Project-Charter-ISAAI.pdf`](Project-Charter-ISAAI.pdf) | Built PDF (`./scripts/build-charter-pdf.sh`) |
| [`MASTER_PROMPT.md`](MASTER_PROMPT.md) | Phased AI session contract (image limits) |

## Branches

- `main` — submission-ready
- `develop` — integration
- `feature/isa-module` — ISA development
- `feature/ai-module` — A+I development

## Source of truth

This folder (`ISA und A+I Projekt/GitHub/-ISAAI-Automatic-Report-Documentation`) is the authoritative working copy. Sync status: [`docs/SYNC-STATUS.md`](docs/SYNC-STATUS.md).

## Quick start for AI agents

Read [`MASTER_PROMPT.md`](MASTER_PROMPT.md) before opening images or parent folders (`Projektdateien/`, lecture PDFs).

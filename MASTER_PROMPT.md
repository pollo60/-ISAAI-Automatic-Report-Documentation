# ISAAI Master Prompt — AI Session Contract

Use this document at the start of every Cursor/Composer session on this repository.

## Problem this solves

API requests fail with `Exceeded maximum number of images (50)` when too many PNG/JPG files are attached in one turn. This repo has **8** diagram images; the limit is usually exceeded by `@`-referencing parent folders or batch-reading images.

## Hard rules

1. **Never** `@`-attach parent folders (`FUAS/`, `Projektdateien/`, lecture PDF directories) in the same message as this repo.
2. **Never** `Read` image files in batch; **never** glob `**/*.{png,jpg,jpeg}`.
3. Prefer **BPMN** (`.bpmn`) and **ArchiMate** (`.archimate`) XML over exported PNG.
4. Maximum **2 images per request**, **8 images per session** — only when text sources are insufficient; use explicit paths from [`docs/AI-SESSION-IMAGE-INDEX.md`](docs/AI-SESSION-IMAGE-INDEX.md).
5. Do not open [`docs/official-archive/`](docs/official-archive/) unless explicitly asked for grading originals.

## Phased workflow

| Phase | Goal | Allowed reads | Image budget |
|-------|------|---------------|--------------|
| **P0 Scope** | README, roadmap, issue-list, charter (HTML/text) | `.md`, `.html`, `.txt` | **0** |
| **P1 Process** | IST/SOLL process narrative | `.bpmn`, `.md` | **0** |
| **P2 Architecture** | ArchiMate models | `.archimate` | **0** |
| **P3 Visuals** | Diagram review only if needed | Named PNG/JPG only | **≤2 / request** |
| **P4 Implementation** | Code, tests, OpenAPI | `.py`, `.yaml`, `.yml` | **0** |

## Session opener (copy for user)

```
Work on ISAAI using MASTER_PROMPT.md phases.
Start at P0. Do not read any images until P3 and only if necessary.
Canonical docs: docs/Documentation/
```

## Project context (text-only)

- **ISA:** Exchange invoice PDF/OCR → structured data → charts; ArchiMate enterprise alignment.
- **A+I:** XML financial reports → GOAL validation → exception governance → archive; BPMN operable model.
- **Stakeholder language:** Use censored docs (`STAKEHOLDER-*`); no employer branding in outputs.

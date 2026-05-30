# Boardroom presentation narrative

**Deck:** `ISAAI-Boardroom-Manual-to-Automated.pptx`  
**Style:** English, executive / boardroom  
**Arc:** Question → evidence → answer (professor bookend)

## Opening question (slide 2)

> **Can we eliminate 30–40 minutes of daily manual report work—and still strengthen auditability and control?**

**Speaker note:** Pause 3–5 seconds. Do not answer yet.

## Three proof pillars (middle slides)

1. **Cost of today** — Manual IST process, error and archive risk (`process as is.md`).
2. **Operable target** — GOAL BPMN: automate ingest → validate → archive; humans only on exceptions.
3. **Dual-module fit** — ISA (alignment, invoices, charts) + A+I (BPMN, XML, integration mocks).

## Closing answer (slide 15)

Repeat the question, then:

- **Yes, with scope discipline** — automate the repeatable path; reserve human judgment for exception governance (HITL).
- **ISA** delivers enterprise ArchiMate alignment and invoice/chart automation for the exchange-invoice track.
- **A+I** delivers GOAL-conform XML validation, operable BPMN, and OpenAPI-described integration mocks.
- **Residual decisions** — production LLM gateway, DMS credentials, probe sandbox (documented in `docs/compliance/STAKEHOLDER-INTERFACE-QUESTIONS.md`).

## 30-second elevator

We mapped a daily 30–40 minute manual control process and designed governed automation: machines handle ingest and rules; supervisors only see exceptions. Two university modules—ISA and A+I—cover architecture and integration without blurring accountability.

## 5-minute walkthrough

1. Hook with the opening question (30 s)  
2. IST pain — four phases, naming friction, archive gap (60 s)  
3. SOLL BPMN — swimlanes and exception path (90 s)  
4. ISA vs A+I matrix — who owns which artifact (60 s)  
5. Compliance — audit trail fields and pseudonymization default (45 s)  
6. Close with the answer slide (45 s)

# Roadmap: ISA & A+I Dual-Module Automation

## Projektziel
Vollständige GitHub-basierte Implementierung zweier separater Automatisierungsmodule:
- **ISA (Information Systems Architecture)**: Automatisierte Rechnungsextraktion aus PDF/OCR, Datenstrukturierung und Chart-Generierung für Präsentationen
- **A+I (Architecture & Integration)**: Vollautomatisierte Finanzberichtsverarbeitung mit GOAL-SOLL Architektur, Validierung und Governance

## Kernresultate
- ISA-Modul: Python-basierte Extraktion und Visualisierung von Rechnungsdaten
- A+I-Modul: GOAL-konforme Validierung, Exception-Handling und SharePoint/DMS-Integration
- Vollständige GitHub-Implementierung mit separaten Branches für ISA und A+I
- Architekturbeschreibung, Prozessmodelle und integrierte Präsentation für beide Module
- Prüfungsfertige Abgabe mit dualer Moduldokumentation

## Roadmap

### Phase 1: ISA & A+I Requirements Split
- Analyse der separaten ISA- und A+I-Anforderungen aus dem Briefing
- Definition von ISA-Workflow: PDF/OCR → Datenextraktion → Chart-Generierung
- Definition von A+I-Workflow: XML-Ingestion → GOAL-Validierung → Governance & Archive
- GitHub-Setup mit separaten Branches für ISA und A+I Module
- Resultate: Getrennte Requirements-Dokumente, GitHub-Repo-Struktur

### Phase 2: ISA Module Development
- Aufbau der PDF/OCR-Extraktionspipeline in `/src/isa`
- Implementierung der Datenstrukturierung in JSON/CSV
- Entwicklung der automatisierten Chart- und Präsentationsgenerierung
- Resultate: Vollständiges ISA-Modul, Testdaten und Unit-Tests

### Phase 3: A+I Module Development
- XML-Parser für Report Type A und B in `/src/ai`
- GOAL-SOLL Regelengine für Validierung und Exception-Erkennung
- Integration von SharePoint-API und DMS-Archivierung
- Resultate: Vollständiges A+I-Modul mit Governance-Workflow

### Phase 4: Dual-Module Integration
- Vereinigung der ISA- und A+I-Workflows in einem GitHub-Repo
- End-to-End-Integrationstests für beide Module
- Cross-Module-Datenflüsse und gemeinsame Präsentationsausgabe
- Resultate: Integrierte GitHub-Implementierung, vollständige Automatisierung

### Phase 5: Documentation & Submission
- ISA-Architektur- und Prozessdokumentation
- A+I-GOAL-Modellbeschreibung und Governance-Narrative
- Erstellung der kombinierten Präsentation und Abgabeunterlagen
- Finalisierung der GitHub-Repo für Submission
- Resultate: Prüfungsfertige Dokumentation und GitHub-Implementierung

## Zeitplan
- 18.05.–24.05.: ISA/A+I Requirements Split und GitHub-Setup
- 25.05.–01.06.: ISA-Modul Entwicklung (PDF/OCR, Charts)
- 02.06.–08.06.: A+I-Modul Entwicklung (Validierung, Archive)
- 09.06.–15.06.: Integration, Tests und Dokumentation
- 16.06.: Submission

## Wichtige Risiko- und Erfolgsfaktoren
- Klare Trennung von ISA- und A+I-Implementierungen bei gemeinsamer GitHub-Basis
- Vollständige Automatisierung beider Module ohne manuelle Eingriffe (außer A+I-Governance)
- Stabile GitHub-Integration und Branching-Strategie für parallele Entwicklung
- Nachvollziehbare Architekturmodelle und Prozessdokumentation für beide Module
- Zeitliche Synchronisation der ISA- und A+I-Entwicklung für finale Integration

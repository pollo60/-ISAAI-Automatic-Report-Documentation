# Issue List

## M1: ISA & A+I Requirements Split
- [ ] Review ISA requirements: PDF/OCR extraction, data structuring, chart generation for invoice automation
- [ ] Review A+I requirements: XML validation, GOAL rules, exception governance, SharePoint/DMS integration
- [ ] Set up GitHub branches: `feature/isa-module` and `feature/ai-module` for separate development
- [ ] Define ISA workflow: Input (PDF/website) → Extraction → JSON/CSV → Charts → Presentation
- [ ] Define A+I workflow: Email/XML input → Validation → Exceptions → Archive
- [ ] Create separate requirement docs for ISA and A+I modules

## M2: ISA Module Development
- [ ] Implement PDF/OCR ingestion pipeline in `/src/isa`
- [ ] Build data extraction logic for invoice fields (amounts, dates, vendors)
- [ ] Create JSON/CSV transformation schema for ISA data
- [ ] Develop automated chart generation (bar charts, pie charts, trends)
- [ ] Implement presentation export functionality (PowerPoint/PDF)
- [ ] **Implement "Bereitstellung für Operator": Magic chart system for professor requirements**
- [ ] Add unit tests for ISA extraction and visualization components

## M3: A+I Module Development
- [ ] Implement XML parser for Report Type A (daily snapshot) in `/src/ai`
- [ ] Implement XML parser for Report Type B (month-to-date) in `/src/ai`
- [ ] Build GOAL rule evaluator: primary violation markers, secondary thresholds
- [ ] Create exception detection and alerting logic
- [ ] Integrate SharePoint API for evidence storage
- [ ] Integrate DMS API for final archiving and sign-off

## M4: Dual-Module Integration
- [ ] Merge ISA and A+I branches into `develop` branch
- [ ] Create unified workflow orchestration in GitHub Actions
- [ ] Implement cross-module data flows and shared components
- [ ] Run end-to-end integration tests for combined ISA+A+I pipeline
- [ ] Optimize GitHub CI/CD for automated testing and deployment
- [ ] Verify complete automation without manual intervention (except A+I exceptions)

## M5: Documentation & Submission
- [ ] Write ISA architecture description and process documentation
- [ ] Write A+I GOAL model description and governance narrative
- [ ] Create combined presentation deck covering both modules
- [ ] Prepare submission package with GitHub repo, docs, and models
- [ ] Final integration testing and bug fixing
- [ ] Ensure GitHub repo is submission-ready with all code, tests, and documentation

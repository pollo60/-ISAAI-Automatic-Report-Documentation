# Roadmap: ISA & A+I Dual-Module Automation

## Project Objective
Complete GitHub-based implementation of two separate automation modules:
- **ISA (Information Systems Architecture)**: Automated invoice extraction from PDF/OCR, data structuring, and chart generation for presentations
- **A+I (Architecture & Integration)**: Fully automated financial report processing with GOAL architecture, validation, and governance

## Key Deliverables
- ISA module: Python-based extraction and visualization of invoice data
- A+I module: GOAL-compliant validation, exception handling, and SharePoint/DMS integration
- Complete GitHub implementation with separate branches for ISA and A+I
- Architecture descriptions, process models, and integrated presentation for both modules
- Exam-ready submission with dual module documentation

## Roadmap

### Phase 1: ISA & A+I Requirements Split
- Analyze separate ISA and A+I requirements from the briefing
- Define ISA workflow: PDF/OCR → Data extraction → Chart generation
- Define A+I workflow: XML ingestion → GOAL validation → Governance & Archive
- GitHub setup with separate branches for ISA and A+I modules
- Deliverables: Separate requirement documents, GitHub repo structure

### Phase 2: ISA Module Development
- Build PDF/OCR extraction pipeline in `/src/isa`
- Implement data structuring in JSON/CSV
- Develop automated chart and presentation generation
- **Operator Deployment**: Implement the "Magic Chart" system for professor-specific visualizations
- Deliverables: Complete ISA module, test data, and unit tests

### Phase 3: A+I Module Development
- XML parser for Report Type A and B in `/src/ai`
- GOAL rule engine for validation and exception detection
- SharePoint API and DMS archiving integration
- Deliverables: Complete A+I module with governance workflow

### Phase 4: Dual-Module Integration
- Merge ISA and A+I workflows in a single GitHub repo
- End-to-end integration tests for both modules
- Cross-module data flows and shared presentation output
- Deliverables: Integrated GitHub implementation, complete automation

### Phase 5: Documentation & Submission
- ISA architecture and process documentation
- A+I GOAL model description and governance narrative
- Creation of combined presentation and submission materials
- Finalization of GitHub repo for submission
- Deliverables: Exam-ready documentation and GitHub implementation

## Timeline
- May 18–24: ISA/A+I requirements split and GitHub setup
- May 25–Jun 1: ISA module development (PDF/OCR, charts)
- Jun 2–8: A+I module development (validation, archive)
- Jun 9–15: Integration, testing, and documentation
- Jun 16: Submission

## Key Risk and Success Factors
- Clear separation of ISA and A+I implementations on a shared GitHub base
- Complete automation of both modules without manual intervention (except A+I governance)
- Stable GitHub integration and branching strategy for parallel development
- Traceable architecture models and process documentation for both modules
- Timeline synchronization of ISA and A+I development for final integration

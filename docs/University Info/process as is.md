# Report: Daily financial report validation (as-is / IST)

## 1. Management summary

Validation of financial reports (Report A and Report B) is a manual, time-critical workflow with high repetitive load. Processing is sequential by an operations analyst across heterogeneous systems (mail client, spreadsheet, collaboration storage, document repository). Manual data transfer and naming conventions increase error risk and archival delay.

## 2. Detailed process (step-by-step)

### Phase 1: Input and extraction

- **Inbound check:** Process starts in the organizational mail system. Daily verification that the control-function mailbox received Report A (daily violations) and Report B (monthly violations) as ZIP attachments.
- **Download:** ZIP files saved to the workstation.
- **Extraction:** One XML file per ZIP; filenames encode report date in an opaque pattern.

### Phase 2: Preparation and validation (spreadsheet)

- **Import:** XML files imported manually into a spreadsheet for tabular review.
- **Business logic:** Analyst checks violation markers and threshold columns (e.g. values below agreed limits).
- **Report types:** Same steps for Report A (daily) and Report B (monthly), with distinct rule sets.

### Phase 3: Documentation and communication (collaboration storage)

- **Evidence:** Validated workbooks stored in the reporting folder with date-prefixed names (`YYYYMMDD_Type`).
- **Distribution:** Summary email with attachments to the agreed distribution list.
- **Mail archive:** Sent message saved as evidence in the mailing folder.

### Phase 4: Governance and archival (document repository)

- **Access:** Analyst signs into the enterprise document management system.
- **Navigation:** Supervisor review area → regulatory row → sponsor review.
- **Identification:** Analyst enters daily processing identifier.
- **Upload:** Evidence messages and related quota report linked to the day cell.
- **Sign-off:** Final irreversible sign-off after upload completeness.
- **Close:** Session ended.

## 3. Architectural reasoning

- **Media break:** Collaboration storage (files) vs. document repository (structured records) weakens process integrity.
- **Critical state change:** Upload-to-sign-off relies on human diligence, not system-enforced constraints.
- **Automation lever:** Naming-convention friction is the highest-yield target for an automated reporting service.

## 4. Risks and weaknesses

- Manual date naming causes archive inconsistency.
- Strong person dependency (daily identifier entry).
- Gap between email send and repository upload leaves data integrity exposed.

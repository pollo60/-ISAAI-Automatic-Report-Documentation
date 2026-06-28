# Guide: SharePoint & Microsoft Power Automate Setup

This guide walks you step by step through setting up the SharePoint list and manually creating the flow in Power Automate (Microsoft Flow), based on the project requirements and the uploaded CSV schema.

---

## 1. Create the SharePoint List "Report Processing Log"

Your list should use exactly the column names from `src/report_template/Report Processing Log (1).csv`.

### Step-by-Step Creation via CSV Import:
1. Open your SharePoint site: [ISAAIDailyReportProcessing](https://studfrauasde.sharepoint.com/sites/ISAAIDailyReportProcessing).
2. Click **New** → **List**.
3. Select **From CSV**.
4. Click **Upload file** and select the file `src/report_template/Report Processing Log (1).csv` from your local Git repository.
5. SharePoint will automatically read the column names. Verify the column types in the preview:
   - **Title**: Single line of text — *Used as the primary column (Title)*.
   - **ReceivedDateTime**: Date and Time.
   - **SenderEmail**: Single line of text.
   - **ReportDate**: Date and Time (or Date only).
   - **ReportA_Status** & **ReportB_Status**: Choice with options: `Pass`, `Violation`, `Error`, `Pending`.
   - **ReportA_ViolationDetails** & **ReportB_ViolationDetails**: Multiple lines of text.
   - **OverallStatus**: Choice with options: `Completed`, `Exception`, `Processing`, `Failed`.
   - **ExceptionFlag**: Yes/No or Single line of text.
   - **EvidenceA_Link**, **EvidenceB_Link**, **Presentation_Link**: Hyperlink.
6. Name the list **Report Processing Log** and click **Create**.

---

## 2. Prepare the SharePoint Document Library

Create a document library named **Evidence Archive** in SharePoint and set up the following folder structure:
- `Evidence Archive/Templates/` → Upload your PowerPoint template `daily_run_template.pptx` here.
- `Evidence Archive/Presentations/` → Power Automate will save the generated presentations here.
- `Evidence Archive/Evidence/` → The Excel evidence files will be stored here.

---

## 3. Build the Power Automate Flow Manually

Since the Copilot import can throw errors on complex branching flows, build the flow in the Power Automate designer step by step as follows:

### Phase A: Trigger & Initialize Variables
1. **Trigger**: *When a new email arrives (V3)* (Outlook).
   - **Folder**: `Inbox`.
   - **Subject filter**: `Financial Report`.
   - **Only with attachments**: `Yes`.
   - **Include attachments**: `Yes`.
2. **Action**: *Initialize variable* `LogItemID` (Type: `Integer`).
3. **Action**: *Initialize variable* `ReportDate` (Type: `String`).
   - Value (Expression): `substring(triggerOutputs()?['body/attachments'][0]['name'], 0, 8)`
4. **Action**: *Initialize variable* `ReportA_Result` (Type: `String`, Default: `Pass`).
5. **Action**: *Initialize variable* `ReportB_Result` (Type: `String`, Default: `Pass`).
6. **Action**: *Initialize variable* `ReportA_Details` (Type: `String`, Default: `No violation detected`).
7. **Action**: *Initialize variable* `ReportB_Details` (Type: `String`, Default: `No violation detected`).

### Phase B: Create SharePoint List Entry
1. **Action**: *Create item* (SharePoint → `Report Processing Log`).
   - **Title**: `@triggerOutputs()?['body/subject']`
   - **ReceivedDateTime**: `@triggerOutputs()?['body/receivedDateTime']`
   - **SenderEmail**: `@triggerOutputs()?['body/from']`
   - **OverallStatus**: `Processing`
   - **ExceptionFlag**: `No`
2. **Action**: *Set variable* `LogItemID`.
   - **Value**: `@outputs('Create_item')?['body/ID']` (the ID of the newly created list row).

### Phase C: Extract ZIP Attachment & Read XML
1. **Action**: *Apply to each* → Loop over email attachments: `triggerOutputs()?['body/attachments']`.
2. **Action (inside loop)**: *Condition* → Check if the attachment is a ZIP file (e.g., filename ends with `.zip`).
3. **In the Yes branch**:
   - **Action**: *Extract archive to folder* (OneDrive for Business).
     - **Archive file content**: `Attachment Content`.
     - **Target folder path**: `/Evidence Archive/Temp/`.
   - **Action**: *Get file content* (SharePoint or OneDrive) for the extracted XML files:
     - Find the file `*ReportTypeA.xml` and read the text into a Compose action `XML_A_Content`.
     - Find the file `*ReportTypeB.xml` and read the text into a Compose action `XML_B_Content`.

### Phase D: Parallel Validation
Create a **Parallel Branch** after closing the attachment loop:

#### Left Branch (Report Type A)
1. **Action**: *Compose* → `MarkerA`.
   - Value (Expression): `xpath(xml(outputs('XML_A_Content')), 'string(/Report/Data/Row/ViolationMarker)')`
2. **Action**: *Condition* → Check if `MarkerA` equals `V`.
3. **In the Yes branch (violation check)**:
   - Read the four threshold values (Threshold1 through Threshold4) with XPath conversions to integers. Example for Threshold1:
     `int(xpath(xml(outputs('XML_A_Content')), 'string(/Report/Data/Row/Threshold1)'))`
   - If a value is **less than 50**:
     - Set variable `ReportA_Result` = `Violation`.
     - Set variable `ReportA_Details` = *Details of the violation*.

#### Right Branch (Report Type B)
Perform the same steps analogously for `XML_B_Content` and set `ReportB_Result` and `ReportB_Details`.

### Phase E: Excel Evidence & PowerPoint Creation
After the parallel branches merge:
1. **Action**: *Run script* (Excel Online).
   - Execute your Office Script to write the rows and results to `evidence_log.xlsx`.
2. **Action**: *Copy file* (SharePoint).
   - **Source**: `/Evidence Archive/Templates/daily_run_template.pptx`
   - **Destination**: `/Evidence Archive/Presentations/`
   - **New name**: `concat(variables('ReportDate'), '_Run_Summary.pptx')`
3. **Action**: *Populate a PowerPoint template* (PowerPoint Online).
   - Select the copied presentation.
   - Enter the variables into the detected tags:
     - `{{ReportDate}}` → `variables('ReportDate')`
     - `{{ReportA_Status}}` → `variables('ReportA_Result')`
     - `{{ReportB_Status}}` → `variables('ReportB_Result')`
     - `{{ReportA_Details}}` → `variables('ReportA_Details')`
     - `{{ReportB_Details}}` → `variables('ReportB_Details')`

### Phase F: Exception Gate & Completion
1. **Action**: *Condition* → Is `ReportA_Result` equal to `Violation` OR `ReportB_Result` equal to `Violation`?
2. **In the Yes branch (violation present)**:
   - **Action**: *Update item* (SharePoint `Report Processing Log` with `LogItemID`):
     - `OverallStatus`: `Exception`
     - `ExceptionFlag`: `Yes`
     - `EvidenceA_Link`, `EvidenceB_Link`, `Presentation_Link` → Links to the created files.
   - **Action**: *Send an email (V2)* (To supervisor, Importance: High) with links to the Excel and PowerPoint files.
3. **In the No branch (no errors)**:
   - **Action**: *Update item* (SharePoint `Report Processing Log` with `LogItemID`):
     - `OverallStatus`: `Completed`
     - `EvidenceA_Link`, `EvidenceB_Link`, `Presentation_Link` → Links to the files.
   - **Action**: *Send an email (V2)* (To standard distribution) with Excel and PowerPoint attachments.
   - **Action**: Export email as `.eml` and save to SharePoint.

#!/bin/bash

# Ensure gh CLI is authenticated
if ! gh auth status >/dev/null 2>&1; then
    echo "GitHub CLI not authenticated. Please run 'gh auth login' first."
    exit 1
fi

echo "Creating GitHub Issues..."

gh issue create \
  --title "Update BPMN - Separate Pool for 'Op Supervisor'" \
  --body "Currently, the operational model lacks a distinct separation for the Operational Supervisor. Professor Dietrich noted: 'Der Op Supervisor sollte als eigener Pool modellliert werden.'
**Tasks**:
- [ ] Open the current BPMN diagram.
- [ ] Create a new, separate Pool for the 'Op Supervisor'.
- [ ] Migrate the relevant tasks that belong to the Op Supervisor into this new pool.
- [ ] Ensure message flows between the Op Supervisor pool and the Automated Reporting System pool are correctly modeled."

gh issue create \
  --title "Update BPMN - Split compound tasks into atomic tasks" \
  --body "Some tasks in the BPMN model contain 'und' (e.g., 'Extract and Upload'), making them compound rather than atomic. Professor Dietrich noted: 'Die Tasks sollten kein 'und' enthalten. Das müssen eigene Tasks sein.'
**Tasks**:
- [ ] Identify all tasks containing 'und' or 'and' in their labels.
- [ ] Split these tasks into two or more distinct, sequential tasks (e.g., Task 1: 'Extract Data', Task 2: 'Upload Data').
- [ ] Ensure the process flow correctly links these new atomic tasks."

gh issue create \
  --title "Update BPMN - Clarify Financial Report Input" \
  --body "The origin of the Financial Report in the reporting system is currently unclear. Professor Dietrich asked: 'Wie kommt der Financial Report in das Automated Reporting System?'
**Tasks**:
- [ ] Identify how the Financial Report enters the system (e.g., Email received, File uploaded to SharePoint, API trigger).
- [ ] Add a start event or an external pool/message flow that clearly shows this trigger.
- [ ] Update the documentation to explicitly describe this input process."

gh issue create \
  --title "Update BPMN - Add Error Handling Paths (1-2 examples)" \
  --body "The current model assumes a 'happy path' and lacks error handling, making it too strategic. Professor Dietrich asked: 'Was passiert im Fehlerfall? z.b. Parsing schief gegangen. File konnte nicht erstellt werden.'
**Tasks**:
- [ ] Identify 1 or 2 critical points of failure (e.g., 'Data Parsing Failed', 'File Creation Failed').
- [ ] Add Error Boundary Events to the relevant tasks.
- [ ] Model the alternative path when an error occurs (e.g., 'Send Error Notification to Op Supervisor', 'Log Error', 'Abort Process')."

gh issue create \
  --title "Update BPMN - Specify actor for 'Archive Email'" \
  --body "There is a manual task for archiving emails in the DMS, but it is unclear who performs this action. Professor Dietrich asked: 'Ihr habt im DMS einen manual Task mit Archive Email wer macht das? Ist das auch ein User? Dann sollte der auch modelliert werden.'
**Tasks**:
- [ ] Determine who is responsible for the 'Archive Email' task.
- [ ] If it is a specific user role, create a Lane or Pool for this user.
- [ ] Move the 'Archive Email' task into this new Lane/Pool.
- [ ] If it is automated instead of manual, change the task type to a Service/Script Task."

gh issue create \
  --title "Documentation - Condense Final Report" \
  --body "The final report must meet the strict page limits specified in the Evaluation Matrix. Professor Dietrich requested shrinking to 10-12 pages, but the formal matrix states: 'Report stays within the limit of max 10 pages (BPMN operational model is excluded from the page count)'.
**Tasks**:
- [ ] Review the current draft of the Final Report (currently 14 pages).
- [ ] Remove overly generic 'strategic' filler content.
- [ ] Ensure the final page count (excluding Title, TOC, and BPMN operational model) is max 10 pages."

gh issue create \
  --title "Update BPMN - Final Operational Review" \
  --body "The overall feedback indicated the model was too 'Strategic'. 
**Tasks**:
- [ ] Review all Pools and Lanes for correctness.
- [ ] Ensure all tasks represent actual operational steps in the Power Automate flow.
- [ ] Cross-check the final BPMN model against the actual implemented system to ensure they match exactly."

gh issue create \
  --title "Cost Calculation - Correct compounding percentage errors" \
  --body "A detailed analysis of the 'ISAAI Cost Calculation (1).xlsx' and Page 10 of the Final Report revealed mathematical errors in the calculation for Change Management & Training (5%) and Contingency Buffer (10%). They are currently calculated as a percentage of the *previous row's value* instead of the base Developer Cost or the subtotal.
**Tasks**:
- [ ] Open 'ISAAI Cost Calculation (1).xlsx' and review formulas.
- [ ] Correct the formulas for Change Management & Training to calculate 5% of the base Developer Cost (e.g., 5% of €7,428 = €371.40).
- [ ] Correct the formulas for Contingency Buffer to calculate 10% of the base or subtotal.
- [ ] Update the quantitative benefits table on Page 10 of the Final Report with the corrected sums."

gh issue create \
  --title "Presentation - Align slides with grading rubrics" \
  --body "The evaluation matrices specifically require certain elements to be present in the presentation to achieve maximum points (60 for A+I, 40 for RPA).
**Tasks**:
- [ ] Ensure all 3 ArchiMate layers (Business, Application, Technology) are shown as screenshots (not in Archi itself).
- [ ] Include a clear 'Problem Statement: Situation / Complication / Solution' slide.
- [ ] Ensure action titles (McKinsey-style) with sub-headers are used on *every* slide.
- [ ] Include a slide that clearly describes the challenges faced before, during, and after implementation.
- [ ] Ensure the 'Magic Charts' are presented.
- [ ] Prepare a live demo of the working software for the RPA presentation."

gh issue create \
  --title "Documentation - Transparent documentation of AI usage" \
  --body "Criterion 25 of the RPA Matrix requires 'transparent documentation of any AI usage (which tools, for what, prompts where relevant)' for 4.0 points. The current report mentions Gemini, Claude, Antigravity, and CursorAI in the technology stack but doesn't elaborate.
**Tasks**:
- [ ] Add a specific section or appendix in the Final Report detailing exactly how AI tools were used.
- [ ] Include specific prompts or use cases where relevant to satisfy this rubric requirement."

echo "All GitHub Issues created successfully!"

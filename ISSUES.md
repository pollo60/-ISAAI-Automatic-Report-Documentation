# Project Improvement Action Plan & Issues

This document contains a structured list of actionable tasks based on Professor Dietrich's feedback and a detailed analysis of the Evaluation Matrices and Cost Calculation. These are formatted as issues that you can use as a team to-do list to achieve a 1.0 grade.

## Issue 1: Model the "Op Supervisor" as a distinct Pool
**Title**: Update BPMN - Separate Pool for "Op Supervisor"
**Description**: 
Currently, the operational model lacks a distinct separation for the Operational Supervisor. Professor Dietrich noted: "Der Op Supervisor sollte als eigener Pool modellliert werden." 
**Tasks**:
- [ ] Open the current BPMN diagram. 
- [ ] Create a new, separate Pool for the "Op Supervisor".
- [ ] Migrate the relevant tasks that belong to the Op Supervisor into this new pool.
- [ ] Ensure message flows between the Op Supervisor pool and the Automated Reporting System pool are correctly modeled.

## Issue 2: Ensure Task Atomicity (Remove "and" from tasks)
**Title**: Update BPMN - Split compound tasks into atomic tasks
**Description**: 
Some tasks in the BPMN model contain "und" (e.g., "Extract and Upload"), making them compound rather than atomic. Professor Dietrich noted: "Die Tasks sollten kein 'und' enthalten. Das müssen eigene Tasks sein."
**Tasks**:
- [ ] Identify all tasks containing "und" or "and" in their labels.
- [ ] Split these tasks into two or more distinct, sequential tasks (e.g., Task 1: "Extract Data", Task 2: "Upload Data").
- [ ] Ensure the process flow correctly links these new atomic tasks.

## Issue 3: Define Financial Report Input Trigger
**Title**: Update BPMN - Clarify Financial Report Input
**Description**: 
The origin of the Financial Report in the reporting system is currently unclear. Professor Dietrich asked: "Wie kommt der Financial Report in das Automated Reporting System?"
**Tasks**:
- [ ] Identify how the Financial Report enters the system (e.g., Email received, File uploaded to SharePoint, API trigger).
- [ ] Add a start event or an external pool/message flow that clearly shows this trigger.
- [ ] Update the documentation to explicitly describe this input process.

## Issue 4: Implement Operational Error Handling
**Title**: Update BPMN - Add Error Handling Paths (1-2 examples)
**Description**: 
The current model assumes a "happy path" and lacks error handling, making it too strategic. Professor Dietrich asked: "Was passiert im Fehlerfall? z.b. Parsing schief gegangen. File konnte nicht erstellt werden."
**Tasks**:
- [ ] Identify 1 or 2 critical points of failure (e.g., "Data Parsing Failed", "File Creation Failed").
- [ ] Add Error Boundary Events to the relevant tasks.
- [ ] Model the alternative path when an error occurs (e.g., "Send Error Notification to Op Supervisor", "Log Error", "Abort Process").

## Issue 5: Define Actor for "Archive Email" Manual Task
**Title**: Update BPMN - Specify actor for "Archive Email"
**Description**: 
There is a manual task for archiving emails in the DMS, but it is unclear who performs this action. Professor Dietrich asked: "Ihr habt im DMS einen manual Task mit 'Archive Email' wer macht das? Ist das auch ein User? Dann sollte der auch modelliert werden."
**Tasks**:
- [ ] Determine who is responsible for the "Archive Email" task.
- [ ] If it is a specific user role, create a Lane or Pool for this user.
- [ ] Move the "Archive Email" task into this new Lane/Pool.
- [ ] If it is automated instead of manual, change the task type to a Service/Script Task.

## Issue 6: Condense Final Report to max 10 Pages
**Title**: Documentation - Condense Final Report
**Description**: 
The final report must meet the strict page limits specified in the Evaluation Matrix. Professor Dietrich requested shrinking to 10-12 pages, but the formal matrix states: "Report stays within the limit of max 10 pages (BPMN operational model is excluded from the page count)".
**Tasks**:
- [ ] Review the current draft of the Final Report (currently 14 pages).
- [ ] Remove overly generic "strategic" filler content.
- [ ] Ensure the final page count (excluding Title, TOC, and BPMN operational model) is max 10 pages.

## Issue 7: Overall Operational Review
**Title**: Update BPMN - Final Operational Review
**Description**: 
The overall feedback indicated the model was too "Strategic". 
**Tasks**:
- [ ] Review all Pools and Lanes for correctness.
- [ ] Ensure all tasks represent actual operational steps in the Power Automate flow.
- [ ] Cross-check the final BPMN model against the actual implemented system to ensure they match exactly.

## Issue 8: Fix Math Errors in Cost Calculation Excel & Report
**Title**: Cost Calculation - Correct compounding percentage errors
**Description**: 
A detailed analysis of the "ISAAI Cost Calculation (1).xlsx" and Page 10 of the Final Report revealed mathematical errors in the calculation for Change Management & Training (5%) and Contingency Buffer (10%). They are currently calculated as a percentage of the *previous row's value* instead of the base Developer Cost or the subtotal. For example, Contingency is calculated as 10% of the €55.71 Change Management cost, resulting in €5.57, which is incorrect.
**Tasks**:
- [ ] Open `ISAAI Cost Calculation (1).xlsx` and review formulas.
- [ ] Correct the formulas for Change Management & Training to calculate 5% of the base Developer Cost (e.g., 5% of €7,428 = €371.40).
- [ ] Correct the formulas for Contingency Buffer to calculate 10% of the base or subtotal.
- [ ] Update the quantitative benefits table on Page 10 of the Final Report with the corrected sums.

## Issue 9: Align Presentation with Evaluation Matrices (A+I & RPA)
**Title**: Presentation - Align slides with grading rubrics
**Description**:
The evaluation matrices specifically require certain elements to be present in the presentation to achieve maximum points (60 for A+I, 40 for RPA). To get a 1.0, these criteria must be strictly followed.
**Tasks**:
- [ ] Ensure all 3 ArchiMate layers (Business, Application, Technology) are shown as screenshots (not in Archi itself).
- [ ] Include a clear "Problem Statement: Situation / Complication / Solution" slide.
- [ ] Ensure action titles (McKinsey-style) with sub-headers are used on *every* slide.
- [ ] Include a slide that clearly describes the challenges faced before, during, and after implementation.
- [ ] Ensure the "Magic Charts" are presented.
- [ ] Prepare a live demo of the working software for the RPA presentation.

## Issue 10: Citation and AI Usage Transparency
**Title**: Documentation - Transparent documentation of AI usage
**Description**:
Criterion 25 of the RPA Matrix requires "transparent documentation of any AI usage (which tools, for what, prompts where relevant)" for 4.0 points. The current report mentions Gemini, Claude, Antigravity, and CursorAI in the technology stack but doesn't elaborate.
**Tasks**:
- [ ] Add a specific section or appendix in the Final Report detailing exactly how AI tools were used.
- [ ] Include specific prompts or use cases where relevant to satisfy this rubric requirement.

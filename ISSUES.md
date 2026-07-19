# Project Improvement Action Plan & Issues

This document contains a structured list of actionable tasks based on Professor Dietrich's feedback. These are formatted as issues that you can directly copy-paste into your GitHub Issues tracker or use as a team to-do list.

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

## Issue 6: Condense Final Report to 10-12 Pages
**Title**: Documentation - Condense Final Report
**Description**: 
The final report must meet the strict page limits specified in the Evaluation Matrix. Professor Dietrich requested: "bitte versucht den Report auf 10 bis 12 Seiten (wie in der Evaluation Matrix angegeben) zu schrumpfen."
**Tasks**:
- [ ] Review the current draft of the Final Report.
- [ ] Remove overly generic "strategic" filler content.
- [ ] Focus heavily on technical depth, the revised BPMN model, cost calculation summaries, and the Power Automate architecture.
- [ ] Ensure the final page count (excluding title page/TOC) is exactly 10-12 pages.

## Issue 7: Overall Operational Review
**Title**: Update BPMN - Final Operational Review
**Description**: 
The overall feedback indicated the model was too "Strategic". 
**Tasks**:
- [ ] Review all Pools and Lanes for correctness.
- [ ] Ensure all tasks represent actual operational steps in the Power Automate flow.
- [ ] Cross-check the final BPMN model against the actual implemented system to ensure they match exactly.

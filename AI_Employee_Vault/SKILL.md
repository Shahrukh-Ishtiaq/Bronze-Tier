---
version: 1.0
created: 2026-03-01
tier: Bronze
---

# 🤖 AI Employee Agent Skills

This document defines the Agent Skills for the AI Employee Bronze Tier implementation. These skills enable Qwen Code to interact with the Obsidian vault and perform automated tasks.

---

## Overview

Agent Skills are predefined capabilities that allow Qwen Code to:
- Read from and write to the vault
- Process tasks from the Needs_Action folder
- Create plans and update the Dashboard
- Move files between folders
- Log all actions

---

## Skill 1: Read Vault Files

**Purpose:** Read any file from the Obsidian vault.

**Usage:**
```
Read the file: Dashboard.md
Read the file: Company_Handbook.md
Read the file: Needs_Action/EMAIL_example_2026-03-01.md
```

**Implementation:**
- Use file system read operations
- Return full content with frontmatter
- Handle errors gracefully

---

## Skill 2: Write Vault Files

**Purpose:** Create or update files in the vault.

**Usage:**
```
Write to: Plans/PLAN_task_2026-03-01.md
Content: [markdown content with frontmatter]
```

**Rules:**
- Always include frontmatter with type, created, status
- Use UTF-8 encoding
- Never overwrite without confirmation

---

## Skill 3: List Folder Contents

**Purpose:** List all files in a vault folder.

**Usage:**
```
List files in: Needs_Action
List files in: Pending_Approval
```

**Returns:**
- File names
- File count
- Last modified timestamps

---

## Skill 4: Move Files

**Purpose:** Move files between folders (e.g., Needs_Action → Done).

**Usage:**
```
Move file: Needs_Action/TASK_001.md
To: Done/
```

**Rules:**
- Verify source file exists
- Verify destination folder exists
- Log the move operation
- Update Dashboard after move

---

## Skill 5: Update Dashboard

**Purpose:** Update the Dashboard.md with current statistics.

**Usage:**
```
Update Dashboard with:
- Pending Tasks: 5
- Completed Today: 3
- Awaiting Approval: 2
```

**Fields to Update:**
- last_updated timestamp
- Pending Tasks count
- Completed Today count
- Awaiting Approval count
- Folder counts table

---

## Skill 6: Create Plan

**Purpose:** Create a Plan.md file for a task.

**Usage:**
```
Create Plan for: Needs_Action/EMAIL_client_2026-03-01.md
```

**Plan Structure:**
```markdown
---
created: <timestamp>
task_source: <source file>
status: pending
type: <task type>
---

# Plan for <task name>

## Objective
<Objective description>

## Steps
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Notes
*Add notes here*
```

---

## Skill 7: Create Approval Request

**Purpose:** Create a file in Pending_Approval for human review.

**Usage:**
```
Create Approval Request:
action: send_email
to: client@example.com
subject: Invoice #123
amount: 500.00
```

**Approval File Structure:**
```markdown
---
type: approval_request
action: <action_type>
created: <timestamp>
expires: <timestamp + 24 hours>
status: pending
---

### Details
<Full description of proposed action>

### To Approve
Move this file to /Approved folder.

### To Reject
Move this file to /Rejected folder.
```

---

## Skill 8: Log Action

**Purpose:** Log all actions to the Logs folder.

**Usage:**
```
Log Action:
type: email_sent
target: client@example.com
result: success
```

**Log Entry Format:**
```json
{
  "timestamp": "2026-03-01T10:30:00Z",
  "action_type": "email_sent",
  "actor": "qwen_code",
  "target": "client@example.com",
  "result": "success"
}
```

---

## Skill 9: Read Company Handbook

**Purpose:** Check rules and guidelines before taking action.

**Usage:**
```
Check Company Handbook for: payment rules
Check Company Handbook for: email guidelines
```

**Key Sections:**
- Financial Rules (payment thresholds)
- Communication Rules (email, WhatsApp, social)
- Security Rules (credential handling)
- Actions NEVER to take autonomously

---

## Skill 10: Read Business Goals

**Purpose:** Align actions with business objectives.

**Usage:**
```
Check Business Goals for: Q1 revenue targets
Check Business Goals for: active projects
```

**Key Sections:**
- Revenue Targets
- Key Metrics
- Active Projects
- Growth Objectives

---

## Workflow Patterns

### Pattern 1: Process New Task

```
1. List files in Needs_Action
2. For each file:
   a. Read the file content
   b. Check Company Handbook for rules
   c. Create Plan in /Plans
   d. Execute actions (or request approval)
   e. Update Dashboard
   f. Move file to Done
   g. Log the action
```

### Pattern 2: Handle Sensitive Action

```
1. Identify action requiring approval
2. Create Approval Request in /Pending_Approval
3. Update Dashboard
4. Wait for human decision:
   - If moved to /Approved: Execute action
   - If moved to /Rejected: Log and notify
5. Log final outcome
```

### Pattern 3: Daily Briefing

```
1. Read all files in Done (today's completions)
2. Read Business_Goals.md for targets
3. Calculate metrics (revenue, tasks completed)
4. Generate Briefing in /Briefings
5. Update Dashboard
```

---

## Error Handling

### When File Not Found
```
Error: File not found: Needs_Action/missing.md
Action: Check folder contents, report error, log issue
```

### When Approval Required But Not Received
```
Status: Awaiting approval for > 24 hours
Action: Create reminder file, notify human
```

### When Action Fails
```
Error: <error description>
Action: Log error, create error report in /Logs, notify human
```

---

## Security Boundaries

### Always Require Approval
- Payments ≥ $50 to new recipients
- Emails to new contacts or bulk sends
- Any action outside Company Handbook rules
- Irreversible actions

### Never Do Autonomously
- Access banking credentials
- Send emotional/negotiation messages
- Sign contracts or legal documents
- Delete files (move to Archive instead)

---

## Testing Commands

### Test Skill 1 (Read)
```
Read the file: Dashboard.md
```

### Test Skill 2 (Write)
```
Write to: Inbox/test_2026-03-01.md
Content: Test file created at <timestamp>
```

### Test Skill 4 (Move)
```
Move file: Inbox/test_2026-03-01.md
To: Done/
```

---

## Integration with Qwen Code

To use these skills with Qwen Code:

1. **Point Qwen Code at the vault:**
   ```bash
   cd AI_Employee_Vault
   qwen
   ```

2. **Reference this SKILL.md:**
   ```
   Refer to SKILL.md for available capabilities
   ```

3. **Use natural language commands:**
   ```
   Process all pending tasks in Needs_Action
   Create a plan for the email from Client A
   Update the Dashboard with current stats
   ```

---

*Skill Version: 1.0 (Bronze Tier)*  
*Last Updated: March 1, 2026*  
*Compatible with: Qwen Code*

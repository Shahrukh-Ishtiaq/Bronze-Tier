# Personal AI Employee - Qwen Implementation Guide

## Overview

This document outlines the implementation of a **Personal AI Employee** (Digital FTE) using Qwen Code as the reasoning engine, following the architectural blueprint from the "Personal AI Employee Hackathon 0" initiative.

**Tagline:** *Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.*

---

## What is a Digital FTE?

A **Digital FTE (Full-Time Equivalent)** is an AI agent that operates as if it were a human employee, working 24/7 to manage personal and business affairs.

### Human FTE vs Digital FTE

| Feature | Human FTE | Digital FTE |
|---------|-----------|-------------|
| Availability | 40 hours/week | 168 hours/week (24/7) |
| Monthly Cost | $4,000 – $8,000+ | $500 – $2,000 |
| Ramp-up Time | 3 – 6 months | Instant (via SKILL.md) |
| Consistency | Variable (85–95%) | Predictable (99%+) |
| Scaling | Linear | Exponential |
| Cost per Task | ~$3.00 – $6.00 | ~$0.25 – $0.50 |
| Annual Hours | ~2,000 hours | ~8,760 hours |

**Key Insight:** A Digital FTE works nearly 9,000 hours/year vs a human's 2,000, representing an 85–90% cost savings.

---

## Architecture: Perception → Reasoning → Action

```
┌─────────────────────────────────────────────────────────────────┐
│                    PERSONAL AI EMPLOYEE                         │
└─────────────────────────────────────────────────────────────────┘

EXTERNAL SOURCES
┌─────────────┬─────────────┬──────────────┬──────────┐
│   Gmail     │  WhatsApp   │  Bank APIs   │  Files   │
└──────┬──────┴──────┬──────┴───────┬──────┴────┬────┘
       │             │              │           │
       ▼             ▼              ▼           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PERCEPTION LAYER (Watchers)                  │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │ Gmail Watcher│ │WhatsApp Watch│ │Finance Watcher│            │
│  │  (Python)    │ │ (Playwright) │ │   (Python)   │            │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘            │
└─────────┼────────────────┼────────────────┼────────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OBSIDIAN VAULT (Local Memory)                │
│  /Needs_Action/  │  /Plans/  │  /Done/  │  /Logs/              │
│  Dashboard.md    │  Company_Handbook.md  │  Business_Goals.md   │
│  /Pending_Approval/  │  /Approved/  │  /Rejected/              │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    REASONING LAYER                              │
│                    QWEN CODE (Primary Engine)                   │
│   Read → Think → Plan → Write → Request Approval                │
└────────────────────────────────┬────────────────────────────────┘
                                 │
              ┌──────────────────┴───────────────────┐
              ▼                                      ▼
┌────────────────────────────┐    ┌────────────────────────────────┐
│    HUMAN-IN-THE-LOOP       │    │         ACTION LAYER           │
│  Review Approval Files     │    │    MCP SERVERS                 │
│  Move to /Approved         │    │  Email MCP │ Browser MCP       │
└────────────────────────────┘    │  Payment MCP │ Social MCP      │
                                  └────────────────────────────────┘
                                           │
                                           ▼
                                  ┌────────────────────────────────┐
                                  │     EXTERNAL ACTIONS           │
                                  │  Send Email │ Make Payment     │
                                  │  Post Social │ Update Calendar │
                                  └────────────────────────────────┘
```

---

## Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **The Brain** | Qwen Code | Primary reasoning engine |
| **The Memory/GUI** | Obsidian | Local Markdown dashboard & knowledge base |
| **The Senses** | Python Scripts | Watchers for Gmail, WhatsApp, filesystem |
| **The Hands** | MCP Servers | External actions (email, payments, browser) |
| **Automation Glue** | Python Orchestrator | Timing, folder watching, process management |

---

## Prerequisites

### Required Software

| Component | Version | Purpose |
|-----------|---------|---------|
| Qwen Code | Latest | Primary reasoning engine |
| Obsidian | v1.10.6+ | Knowledge base & dashboard |
| Python | 3.13+ | Sentinel scripts & orchestration |
| Node.js | v24+ LTS | MCP servers & automation |
| GitHub Desktop | Latest | Version control |

### Hardware Requirements

- **Minimum:** 8GB RAM, 4-core CPU, 20GB free disk space
- **Recommended:** 16GB RAM, 8-core CPU, SSD storage
- **Always-On:** Consider dedicated mini-PC or cloud VM

### Pre-Hackathon Checklist

1. Install all required software
2. Create Obsidian vault named "AI_Employee_Vault"
3. Verify Qwen Code works: `qwen --version`
4. Set up UV Python project
5. Join Wednesday Research Meetings (Zoom ID: 871 8870 7642, Passcode: 744832)

---

## Tiered Deliverables

### Bronze Tier: Foundation (8-12 hours)

- [ ] Obsidian vault with `Dashboard.md` and `Company_Handbook.md`
- [ ] One working Watcher script (Gmail OR filesystem)
- [ ] Qwen Code reading/writing to vault
- [ ] Basic folder structure: `/Inbox`, `/Needs_Action`, `/Done`
- [ ] All AI functionality as Agent Skills

### Silver Tier: Functional Assistant (20-30 hours)

- [ ] All Bronze requirements
- [ ] Two+ Watcher scripts (Gmail + WhatsApp + LinkedIn)
- [ ] Auto-post to LinkedIn for sales generation
- [ ] Qwen reasoning loop creating `Plan.md` files
- [ ] One working MCP server (e.g., email)
- [ ] Human-in-the-loop approval workflow
- [ ] Basic scheduling via cron/Task Scheduler

### Gold Tier: Autonomous Employee (40+ hours)

- [ ] All Silver requirements
- [ ] Full cross-domain integration (Personal + Business)
- [ ] Odoo Community accounting system with MCP integration
- [ ] Facebook/Instagram integration
- [ ] Twitter (X) integration
- [ ] Multiple MCP servers
- [ ] Weekly Business/Accounting Audit with CEO Briefing
- [ ] Error recovery & graceful degradation
- [ ] Comprehensive audit logging
- [ ] Ralph Wiggum loop for autonomous completion

### Platinum Tier: Always-On Cloud + Local Executive (60+ hours)

- [ ] All Gold requirements
- [ ] Cloud VM deployment (Oracle/AWS) for 24/7 operation
- [ ] Work-Zone Specialization:
  - **Cloud owns:** Email triage, draft replies, social post drafts
  - **Local owns:** Approvals, WhatsApp, payments, final send actions
- [ ] Delegation via Synced Vault (Git or Syncthing)
- [ ] Claim-by-move rule for task ownership
- [ ] Odoo on Cloud VM with HTTPS, backups, health monitoring
- [ ] Platinum demo: Email → Cloud drafts → Local approves → Local executes

---

## Core Components

### 1. The Watchers (Perception Layer)

Watchers are lightweight Python scripts that monitor external sources and create actionable files.

#### Base Watcher Pattern

```python
# base_watcher.py
import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod

class BaseWatcher(ABC):
    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def check_for_updates(self) -> list:
        """Return list of new items to process"""
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """Create .md file in Needs_Action folder"""
        pass

    def run(self):
        self.logger.info(f'Starting {self.__class__.__name__}')
        while True:
            try:
                items = self.check_for_updates()
                for item in items:
                    self.create_action_file(item)
            except Exception as e:
                self.logger.error(f'Error: {e}')
            time.sleep(self.check_interval)
```

#### Gmail Watcher

```python
# gmail_watcher.py
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from base_watcher import BaseWatcher
from datetime import datetime

class GmailWatcher(BaseWatcher):
    def __init__(self, vault_path: str, credentials_path: str):
        super().__init__(vault_path, check_interval=120)
        self.creds = Credentials.from_authorized_user_file(credentials_path)
        self.service = build('gmail', 'v1', credentials=self.creds)
        self.processed_ids = set()

    def check_for_updates(self) -> list:
        results = self.service.users().messages().list(
            userId='me', q='is:unread is:important'
        ).execute()
        messages = results.get('messages', [])
        return [m for m in messages if m['id'] not in self.processed_ids]

    def create_action_file(self, message) -> Path:
        msg = self.service.users().messages().get(
            userId='me', id=message['id']
        ).execute()
        
        headers = {h['name']: h['value'] for h in msg['payload']['headers']}
        
        content = f'''---
type: email
from: {headers.get('From', 'Unknown')}
subject: {headers.get('Subject', 'No Subject')}
received: {datetime.now().isoformat()}
priority: high
status: pending
---

### Email Content
{msg.get('snippet', '')}

### Suggested Actions
- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing
'''
        filepath = self.needs_action / f'EMAIL_{message["id"]}.md'
        filepath.write_text(content)
        self.processed_ids.add(message['id'])
        return filepath
```

#### WhatsApp Watcher (Playwright-based)

```python
# whatsapp_watcher.py
from playwright.sync_api import sync_playwright
from base_watcher import BaseWatcher
from pathlib import Path

class WhatsAppWatcher(BaseWatcher):
    def __init__(self, vault_path: str, session_path: str):
        super().__init__(vault_path, check_interval=30)
        self.session_path = Path(session_path)
        self.keywords = ['urgent', 'asap', 'invoice', 'payment', 'help']

    def check_for_updates(self) -> list:
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                self.session_path, headless=True
            )
            page = browser.pages[0]
            page.goto('https://web.whatsapp.com')
            page.wait_for_selector('[data-testid="chat-list"]')
            
            unread = page.query_selector_all('[aria-label*="unread"]')
            messages = []
            for chat in unread:
                text = chat.inner_text().lower()
                if any(kw in text for kw in self.keywords):
                    messages.append({'text': text, 'chat': chat})
            browser.close()
            return messages
```

#### Filesystem Watcher

```python
# filesystem_watcher.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import shutil

class DropFolderHandler(FileSystemEventHandler):
    def __init__(self, vault_path: str):
        self.needs_action = Path(vault_path) / 'Needs_Action'

    def on_created(self, event):
        if event.is_directory:
            return
        source = Path(event.src_path)
        dest = self.needs_action / f'FILE_{source.name}'
        shutil.copy2(source, dest)
        self.create_metadata(source, dest)

    def create_metadata(self, source: Path, dest: Path):
        meta_path = dest.with_suffix('.md')
        meta_path.write_text(f'''---
type: file_drop
original_name: {source.name}
size: {source.stat().st_size}
---

New file dropped for processing.
''')
```

### 2. The Reasoning Layer (Qwen Code)

Qwen Code reads from `/Needs_Action` and `/Accounting`, thinks about the context, and creates plans.

#### Example Reasoning Flow

1. **Read:** Check `/Needs_Action` and `/Accounting`
2. **Think:** "I see a WhatsApp message from a client asking for an invoice and a bank transaction showing a late payment fee."
3. **Plan:** Create `Plan.md` in Obsidian with checkboxes for next steps
4. **Write:** Update `Dashboard.md` with current status
5. **Request Approval:** For sensitive actions, create files in `/Pending_Approval`

### 3. The Action Layer (MCP Servers)

Model Context Protocol (MCP) servers are Qwen Code's hands for external actions.

#### Recommended MCP Servers

| Server | Capabilities | Use Case |
|--------|-------------|----------|
| filesystem | Read, write, list files | Built-in for vault |
| email-mcp | Send, draft, search emails | Gmail integration |
| browser-mcp | Navigate, click, fill forms | Payment portals |
| calendar-mcp | Create, update events | Scheduling |
| slack-mcp | Send messages, read channels | Team communication |

#### MCP Configuration

```json
// ~/.config/qwen-code/mcp.json
{
  "servers": [
    {
      "name": "email",
      "command": "node",
      "args": ["/path/to/email-mcp/index.js"],
      "env": {
        "GMAIL_CREDENTIALS": "/path/to/credentials.json"
      }
    },
    {
      "name": "browser",
      "command": "npx",
      "args": ["@anthropic/browser-mcp"],
      "env": {
        "HEADLESS": "true"
      }
    }
  ]
}
```

### 4. Human-in-the-Loop (HITL) Pattern

For sensitive actions, Qwen writes an approval request file instead of acting directly:

```markdown
# /Vault/Pending_Approval/PAYMENT_Client_A_2026-01-07.md
---
type: approval_request
action: payment
amount: 500.00
recipient: Client A
reason: Invoice #1234 payment
created: 2026-01-07T10:30:00Z
expires: 2026-01-08T10:30:00Z
status: pending
---

### Payment Details
- Amount: $500.00
- To: Client A (Bank: XXXX1234)
- Reference: Invoice #1234

### To Approve
Move this file to /Approved folder.

### To Reject
Move this file to /Rejected folder.
```

### 5. The Ralph Wiggum Loop (Persistence)

The Ralph Wiggum pattern keeps Qwen Code working autonomously until tasks are complete.

#### How It Works

1. Orchestrator creates state file with prompt
2. Qwen works on task
3. Qwen tries to exit
4. Stop hook checks: Is task file in `/Done`?
5. **YES** → Allow exit (complete)
6. **NO** → Block exit, re-inject prompt (loop continues)
7. Repeat until complete or max iterations

#### Usage

```bash
# Start a Ralph loop
qwen-ralph-loop "Process all files in /Needs_Action, move to /Done when complete" \
  --completion-promise "TASK_COMPLETE" \
  --max-iterations 10
```

#### Completion Strategies

1. **Promise-based (simple):** Qwen outputs `<promise>TASK_COMPLETE</promise>`
2. **File movement (advanced):** Stop hook detects when task file moves to `/Done`

---

## Folder Structure

```
AI_Employee_Vault/
├── Dashboard.md
├── Company_Handbook.md
├── Business_Goals.md
├── Inbox/
├── Needs_Action/
├── Plans/
├── Done/
├── Pending_Approval/
├── Approved/
├── Rejected/
├── Accounting/
│   └── Current_Month.md
├── Logs/
│   └── YYYY-MM-DD.json
├── Briefings/
│   └── 2026-01-06_Monday_Briefing.md
└── Invoices/
    └── 2026-01_Client_A.pdf
```

---

## Key Templates

### Business_Goals.md

```markdown
---
last_updated: 2026-01-07
review_frequency: weekly
---

### Q1 2026 Objectives

#### Revenue Target
- Monthly goal: $10,000
- Current MTD: $4,500

#### Key Metrics to Track
| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Client response time | < 24 hours | > 48 hours |
| Invoice payment rate | > 90% | < 80% |
| Software costs | < $500/month | > $600/month |

#### Active Projects
1. Project Alpha - Due Jan 15 - Budget $2,000
2. Project Beta - Due Jan 30 - Budget $3,500

#### Subscription Audit Rules
Flag for review if:
- No login in 30 days
- Cost increased > 20%
- Duplicate functionality with another tool
```

### CEO Briefing Template (Generated Output)

```markdown
---
generated: 2026-01-06T07:00:00Z
period: 2025-12-30 to 2026-01-05
---

# Monday Morning CEO Briefing

## Executive Summary
Strong week with revenue ahead of target. One bottleneck identified.

## Revenue
- **This Week**: $2,450
- **MTD**: $4,500 (45% of $10,000 target)
- **Trend**: On track

## Completed Tasks
- [x] Client A invoice sent and paid
- [x] Project Alpha milestone 2 delivered
- [x] Weekly social media posts scheduled

## Bottlenecks
| Task | Expected | Actual | Delay |
|------|----------|--------|-------|
| Client B proposal | 2 days | 5 days | +3 days |

## Proactive Suggestions

### Cost Optimization
- **Notion**: No team activity in 45 days. Cost: $15/month.
  - [ACTION] Cancel subscription? Move to /Pending_Approval

### Upcoming Deadlines
- Project Alpha final delivery: Jan 15 (8 days)
- Quarterly tax prep: Jan 31 (25 days)

---
*Generated by AI Employee v0.1*
```

---

## Security & Privacy

### 6.1 Credential Management

- **Never** store credentials in plain text or Obsidian vault
- Use environment variables: `export GMAIL_API_KEY="your-key"`
- Use secrets manager (macOS Keychain, Windows Credential Manager, 1Password CLI)
- Create `.env` file (add to `.gitignore` immediately)
- Rotate credentials monthly

#### Example .env Structure

```bash
# .env - NEVER commit this file
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret
BANK_API_TOKEN=your_token
WHATSAPP_SESSION_PATH=/secure/path/session
```

### 6.2 Sandboxing & Isolation

```python
# In any action script
DRY_RUN = os.getenv('DRY_RUN', 'true').lower() == 'true'

def send_email(to, subject, body):
    if DRY_RUN:
        logger.info(f'[DRY RUN] Would send email to {to}')
        return
    # Actual send logic here
```

### 6.3 Audit Logging

```json
{
  "timestamp": "2026-01-07T10:30:00Z",
  "action_type": "email_send",
  "actor": "qwen_code",
  "target": "client@example.com",
  "parameters": {"subject": "Invoice #123"},
  "approval_status": "approved",
  "approved_by": "human",
  "result": "success"
}
```

### 6.4 Permission Boundaries

| Action Category | Auto-Approve Threshold | Always Require Approval |
|----------------|----------------------|------------------------|
| Email replies | To known contacts | New contacts, bulk sends |
| Payments | < $50 recurring | All new payees, > $100 |
| Social media | Scheduled posts | Replies, DMs |
| File operations | Create, read | Delete, move outside vault |

---

## Error Handling & Recovery

### Error Categories

| Category | Examples | Recovery Strategy |
|----------|----------|------------------|
| Transient | Network timeout, API rate limit | Exponential backoff retry |
| Authentication | Expired token, revoked access | Alert human, pause operations |
| Logic | Qwen misinterprets message | Human review queue |
| Data | Corrupted file, missing field | Quarantine + alert |
| System | Orchestrator crash, disk full | Watchdog + auto-restart |

### Retry Logic

```python
# retry_handler.py
import time
from functools import wraps

def with_retry(max_attempts=3, base_delay=1, max_delay=60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except TransientError as e:
                    if attempt == max_attempts - 1:
                        raise
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    logger.warning(f'Attempt {attempt+1} failed, retrying in {delay}s')
                    time.sleep(delay)
        return wrapper
    return decorator
```

### Watchdog Process

```python
# watchdog.py - Monitor and restart critical processes
import subprocess
import time
from pathlib import Path

PROCESSES = {
    'orchestrator': 'python orchestrator.py',
    'gmail_watcher': 'python gmail_watcher.py',
    'file_watcher': 'python filesystem_watcher.py'
}

def check_and_restart():
    for name, cmd in PROCESSES.items():
        pid_file = Path(f'/tmp/{name}.pid')
        if not is_process_running(pid_file):
            logger.warning(f'{name} not running, restarting...')
            proc = subprocess.Popen(cmd.split())
            pid_file.write_text(str(proc.pid))
            notify_human(f'{name} was restarted')

while True:
    check_and_restart()
    time.sleep(60)
```

### Process Management with PM2

```bash
# Install PM2
npm install -g pm2

# Start your watcher and keep it alive forever
pm2 start gmail_watcher.py --interpreter python3

# Freeze this list to start on reboot
pm2 save
pm2 startup
```

---

## Example: End-to-End Invoice Flow

### Scenario
Client sends WhatsApp message asking for invoice. AI Employee should:
1. Detect the request
2. Generate the invoice
3. Send it via email
4. Log the transaction

### Step 1: Detection (WhatsApp Watcher)

```
# Detected message:
# From: Client A
# Text: "Hey, can you send me the invoice for January?"

# Watcher creates:
# /Vault/Needs_Action/WHATSAPP_client_a_2026-01-07.md
```

### Step 2: Reasoning (Qwen Code)

```markdown
# /Vault/Plans/PLAN_invoice_client_a.md
---
created: 2026-01-07T10:30:00Z
status: pending_approval
---

### Objective
Generate and send January invoice to Client A

### Steps
- [x] Identify client: Client A (client_a@email.com)
- [x] Calculate amount: $1,500 (from /Accounting/Rates.md)
- [ ] Generate invoice PDF
- [ ] Send via email (REQUIRES APPROVAL)
- [ ] Log transaction

### Approval Required
Email send requires human approval. See /Pending_Approval/
```

### Step 3: Approval (Human-in-the-Loop)

```markdown
# /Vault/Pending_Approval/EMAIL_invoice_client_a.md
---
action: send_email
to: client_a@email.com
subject: January 2026 Invoice - $1,500
attachment: /Vault/Invoices/2026-01_Client_A.pdf
---

Ready to send. Move to /Approved to proceed.
```

### Step 4: Action (Email MCP)

```javascript
// MCP call
await email_mcp.send_email({
  to: 'client_a@email.com',
  subject: 'January 2026 Invoice - $1,500',
  body: 'Please find attached your invoice for January 2026.',
  attachment: '/Vault/Invoices/2026-01_Client_A.pdf'
});

// Result logged to /Vault/Logs/2026-01-07.json
```

### Step 5: Completion

```markdown
# /Vault/Dashboard.md updated:
### Recent Activity
- [2026-01-07 10:45] Invoice sent to Client A ($1,500)

# Files moved:
# /Needs_Action/WHATSAPP_... -> /Done/
# /Plans/PLAN_invoice_... -> /Done/
# /Approved/EMAIL_... -> /Done/
```

---

## Operation Modes

| Operation Type | Example Task | Local Trigger |
|---------------|--------------|---------------|
| **Scheduled** | Daily Briefing at 8:00 AM | cron (Mac/Linux) or Task Scheduler (Win) |
| **Continuous** | Lead Capture from WhatsApp | Python watchdog monitoring /Inbox |
| **Project-Based** | Q1 Tax Prep | Manual drag-and-drop to /Active_Project |

---

## Learning Resources

### Prerequisites

| Topic | Resource | Time |
|-------|----------|------|
| Qwen Code Fundamentals | [Agent Factory Docs](https://agentfactory.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows) | 3 hours |
| Obsidian Fundamentals | [help.obsidian.md](https://help.obsidian.md) | 30 min |
| Python File I/O | [Real Python](https://realpython.com/read-write-files-python) | 1 hour |
| MCP Introduction | [modelcontextprotocol.io](https://modelcontextprotocol.io/introduction) | 1 hour |
| Agent Skills | [Claude Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) | 2 hours |

### Core Learning

| Topic | Resource | Type |
|-------|----------|------|
| Qwen + Obsidian Integration | [YouTube](https://youtube.com/watch?v=sCIS05Qt79Y) | Video |
| Building MCP Servers | [modelcontextprotocol.io/quickstart](https://modelcontextprotocol.io/quickstart) | Tutorial |
| Agent Teams | [YouTube](https://youtube.com/watch?v=0J2_YGuNrDo) | Video |
| Gmail API Setup | [Google Developers](https://developers.google.com/gmail/api/quickstart) | Docs |
| Playwright Automation | [playwright.dev](https://playwright.dev/python/docs/intro) | Docs |

### Deep Dives

- MCP Server Development: [github.com/anthropics/mcp-servers](https://github.com/anthropics/mcp-servers)
- Production Automation: "Automate the Boring Stuff with Python" (free online)
- Security Best Practices: OWASP API Security Top 10
- Agent Architecture: "Building LLM-Powered Applications" by Anthropic

---

## Troubleshooting FAQ

### Setup Issues

**Q: Qwen Code says "command not found"**

A: Ensure Qwen Code is installed globally and your PATH is configured. Run: `npm install -g @anthropic/claude-code`, then restart terminal.

**Q: Obsidian vault isn't being read by Qwen**

A: Check that you're running Qwen Code from the vault directory, or using the `--cwd` flag. Verify file permissions.

**Q: Gmail API returns 403 Forbidden**

A: Your OAuth consent screen may need verification, or you haven't enabled Gmail API in Google Cloud Console.

### Runtime Issues

**Q: Watcher scripts stop running overnight**

A: Use PM2 (Node.js) or supervisord (Python) to keep them alive. Implement the Watchdog pattern.

**Q: Qwen is making incorrect decisions**

A: Review your `Company_Handbook.md` rules. Add more specific examples. Lower autonomy thresholds.

**Q: MCP server won't connect**

A: Check that the server process is running (`ps aux | grep mcp`). Verify the path in `mcp.json` is absolute.

---

## Ethics & Responsible Automation

### When AI Should NOT Act Autonomously

- **Emotional contexts:** Condolence messages, conflict resolution, sensitive negotiations
- **Legal matters:** Contract signing, legal advice, regulatory filings
- **Medical decisions:** Health-related actions affecting you or others
- **Financial edge cases:** Unusual transactions, new recipients, large amounts
- **Irreversible actions:** Anything that cannot be easily undone

### Transparency Principles

- Disclose AI involvement when sending emails
- Maintain audit trails for all actions
- Allow opt-out for human-only communication
- Schedule weekly reviews of AI decisions

### Suggested Oversight Schedule

1. **Daily:** 2-minute dashboard check
2. **Weekly:** 15-minute action log review
3. **Monthly:** 1-hour comprehensive audit
4. **Quarterly:** Full security and access review

**Remember:** You are responsible for your AI Employee's actions. Regular oversight is essential.

---

## Research Meetings

Join us every Wednesday at 10:00 PM on Zoom:

- **First Meeting:** Wednesday, January 7th, 2026
- **Zoom Link:** https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1
- **Meeting ID:** 871 8870 7642
- **Passcode:** 744832

If Zoom is full, watch live or recordings at: https://www.youtube.com/@panaversity

---

## Submission Requirements

For hackathon submission:

- [ ] GitHub repository (public or private with judge access)
- [ ] README.md with setup instructions and architecture overview
- [ ] Demo video (5-10 minutes) showing key features
- [ ] Security disclosure: How credentials are handled
- [ ] Tier declaration: Bronze, Silver, or Gold
- [ ] Submit Form: https://forms.gle/JR9T1SJq5rmQyGkGA

### Judging Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Functionality | 30% | Does it work? Are core features complete? |
| Innovation | 25% | Creative solutions, novel integrations |
| Practicality | 20% | Would you actually use this daily? |
| Security | 15% | Proper credential handling, HITL safeguards |
| Documentation | 10% | Clear README, setup instructions, demo |

---

## Next Steps

Once you've built your local AI Employee, advance to cloud-based custom FTEs:

[Advanced Cloud FTE Architecture](https://docs.google.com/document/d/15GuwZwIOQy_g1XsIJjQsFNHCTQTWoXQhWGVMhiH0swc/edit?usp=sharing)

---

*Document Version: 1.0*  
*Last Updated: March 1, 2026*  
*Based on: Personal AI Employee Hackathon 0 Blueprint*

# 🤖 AI Employee - Bronze Tier

**Personal AI Employee Hackathon 0: Building Autonomous FTEs in 2026**

*Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.*

---

## Overview

This is the **Bronze Tier** implementation of a Personal AI Employee - a digital assistant that works 24/7 to manage your personal and business affairs using:

- **Qwen Code** as the reasoning engine
- **Obsidian** as the local knowledge base and dashboard
- **Python Watchers** to monitor for new tasks
- **Human-in-the-Loop** approval for sensitive actions

---

## Features (Bronze Tier)

✅ Obsidian vault with Dashboard, Company Handbook, and Business Goals  
✅ Filesystem Watcher - monitors drop folder for new files  
✅ Orchestrator - coordinates workflow between components  
✅ Agent Skills definition for Qwen Code  
✅ Basic folder structure for task management  
✅ Automatic plan generation for tasks  

---

## Quick Start

### Prerequisites

- Python 3.13 or higher
- Qwen Code installed
- Obsidian (optional, for viewing vault)

### Installation

1. **Clone or download this repository**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   # Copy the example file
   copy .env.example .env
   
   # Edit .env with your settings
   ```

4. **Verify the vault structure:**
   ```
   AI_Employee_Vault/
   ├── Dashboard.md
   ├── Company_Handbook.md
   ├── Business_Goals.md
   ├── SKILL.md
   ├── Inbox/
   ├── Needs_Action/
   ├── Plans/
   ├── Done/
   ├── Pending_Approval/
   ├── Approved/
   ├── Rejected/
   ├── Accounting/
   ├── Logs/
   ├── Briefings/
   └── Invoices/
   ```

---

## Usage

### Starting the Filesystem Watcher

The watcher monitors the `Inbox` folder for new files:

```bash
cd watchers
python filesystem_watcher.py ../AI_Employee_Vault
```

Or from the root directory:

```bash
python watchers/filesystem_watcher.py AI_Employee_Vault
```

**Drop files into:** `AI_Employee_Vault/Inbox/`

### Starting the Orchestrator

The orchestrator processes tasks and updates the Dashboard:

```bash
python orchestrator.py --vault AI_Employee_Vault --interval 60
```

**Options:**
- `--vault` or `-v`: Path to the Obsidian vault (default: `AI_Employee_Vault`)
- `--interval` or `-i`: Check interval in seconds (default: 60)

### Running Both (Recommended)

Open two terminal windows:

**Terminal 1 - Watcher:**
```bash
python watchers/filesystem_watcher.py AI_Employee_Vault
```

**Terminal 2 - Orchestrator:**
```bash
python orchestrator.py --vault AI_Employee_Vault
```

---

## How It Works

### Workflow

1. **Drop a file** into `AI_Employee_Vault/Inbox/`
2. **Filesystem Watcher** detects the new file
3. **Watcher creates** an action file in `Needs_Action/`
4. **Orchestrator** picks up the task
5. **Orchestrator creates** a plan in `Plans/`
6. **Qwen Code** (when integrated) processes the task
7. **Task moves** to `Done/` when complete
8. **Dashboard** updates with current stats

### Folder Structure

```
AI_Employee_Vault/
├── Dashboard.md           # Real-time summary
├── Company_Handbook.md    # Rules & guidelines
├── Business_Goals.md      # Objectives & metrics
├── SKILL.md              # Agent Skills definition
│
├── Inbox/                # Drop folder for new files
├── Needs_Action/         # Tasks waiting to be processed
├── Plans/                # Task plans with checkboxes
├── Done/                 # Completed tasks
│
├── Pending_Approval/     # Awaiting human decision
├── Approved/             # Approved actions
├── Rejected/             # Rejected actions
│
├── Accounting/           # Financial records
├── Logs/                 # Action logs
├── Briefings/            # CEO briefings
└── Invoices/             # Invoice files
```

---

## Testing the System

### Test 1: File Drop

1. **Start the watcher:**
   ```bash
   python watchers/filesystem_watcher.py AI_Employee_Vault
   ```

2. **Drop a test file:**
   ```bash
   echo "This is a test document" > AI_Employee_Vault/Inbox/test_document.txt
   ```

3. **Check the output:**
   - Watcher should log: "Processed new file: test_document.txt"
   - Check `Needs_Action/` for a new FILE_*.md file
   - Check `Files/` for a copy of the original file

### Test 2: Orchestrator

1. **Start the orchestrator:**
   ```bash
   python orchestrator.py --vault AI_Employee_Vault
   ```

2. **Check the output:**
   - Should log: "AI Employee Orchestrator (Bronze Tier)"
   - Should update Dashboard.md
   - Should create plans for pending tasks

### Test 3: Manual Task Processing

1. **Create a manual task:**
   ```markdown
   # AI_Employee_Vault/Needs_Action/MANUAL_test_2026-03-01.md
   ---
   type: manual_test
   priority: normal
   status: pending
   ---
   
   ### Test Task
   
   This is a manual test task.
   
   ### Suggested Actions
   
   - [ ] Read this task
   - [ ] Create a plan
   - [ ] Mark as complete
   ```

2. **Run the orchestrator** to process it

3. **Check** `Plans/` for the generated plan

---

## Configuration

### Environment Variables (.env)

| Variable | Default | Description |
|----------|---------|-------------|
| `VAULT_PATH` | `./AI_Employee_Vault` | Path to Obsidian vault |
| `WATCHER_CHECK_INTERVAL` | `30` | Watcher check interval (seconds) |
| `ORCHESTRATOR_CHECK_INTERVAL` | `60` | Orchestrator check interval (seconds) |
| `LOG_LEVEL` | `INFO` | Logging level |
| `DRY_RUN` | `true` | Prevent actual actions |

### Company Handbook

Edit `Company_Handbook.md` to customize:
- Payment approval thresholds
- Communication rules
- Response time SLAs
- Security boundaries

### Business Goals

Edit `Business_Goals.md` to set:
- Revenue targets
- Key metrics
- Active projects
- Growth objectives

---

## Logs

Logs are stored in `AI_Employee_Vault/Logs/`:

- `watcher_YYYY-MM-DD.log` - Filesystem watcher logs
- `orchestrator_YYYY-MM-DD.log` - Orchestrator logs

View logs in real-time:
```bash
# Windows
type AI_Employee_Vault\Logs\watcher_2026-03-01.log

# Linux/Mac
tail -f AI_Employee_Vault/Logs/watcher_2026-03-01.log
```

---

## Troubleshooting

### Watcher not detecting files

1. Check that the `Inbox` folder exists
2. Verify file permissions
3. Check watcher logs for errors
4. Try restarting the watcher

### Orchestrator not processing tasks

1. Check that `Needs_Action` folder has .md files
2. Verify vault path is correct
3. Check orchestrator logs for errors
4. Ensure Python has write access to vault

### Dashboard not updating

1. Check that `Dashboard.md` exists
2. Verify file is not locked by another process
3. Check orchestrator logs for errors

---

## Next Steps (Silver Tier)

To advance to Silver Tier, add:

- [ ] Gmail Watcher for email monitoring
- [ ] WhatsApp Watcher for message monitoring
- [ ] MCP Server for sending emails
- [ ] Human-in-the-loop approval workflow
- [ ] Scheduled tasks (cron/Task Scheduler)
- [ ] LinkedIn auto-posting

---

## Security Notes

⚠️ **Important Security Practices:**

1. **Never commit `.env`** to version control
2. **Never store credentials** in the vault
3. **Use DRY_RUN=true** during development
4. **Review all logs** regularly
5. **Rotate credentials** monthly

---

## Project Structure

```
Bronze-Tier/
├── AI_Employee_Vault/       # Obsidian vault
│   ├── Dashboard.md
│   ├── Company_Handbook.md
│   ├── Business_Goals.md
│   ├── SKILL.md
│   └── [folders...]
│
├── watchers/                # Watcher scripts
│   ├── base_watcher.py
│   └── filesystem_watcher.py
│
├── orchestrator.py          # Main orchestrator
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
└── README.md               # This file
```

---

## Contributing

This is a hackathon project. To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## Resources

- [Personal AI Employee Hackathon Blueprint](./Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.md)
- [Qwen Code Documentation](https://agentfactory.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows)
- [Obsidian Documentation](https://help.obsidian.md)
- [Watchdog Documentation](https://pypi.org/project/watchdog/)

---

## Support

For questions or issues:

- Join Wednesday Research Meetings (Zoom ID: 871 8870 7642, Passcode: 744832)
- Watch recordings at: https://www.youtube.com/@panaversity

---

## License

This project is part of the Personal AI Employee Hackathon 0.

---

*Version: 1.0 (Bronze Tier)*  
*Created: March 1, 2026*  
*Hackathon: Personal AI Employee Hackathon 0*

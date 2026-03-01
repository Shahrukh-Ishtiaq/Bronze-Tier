"""
Orchestrator - Main workflow controller for the AI Employee.

The orchestrator:
1. Monitors the Needs_Action folder for new tasks
2. Triggers Qwen Code to process pending items
3. Updates the Dashboard with current status
4. Manages the overall workflow

Bronze Tier Implementation
"""

import subprocess
import sys
import time
import logging
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional


class Orchestrator:
    """
    Main orchestrator for the AI Employee Bronze Tier.
    
    Coordinates between watchers, Qwen Code, and the vault.
    """
    
    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        Initialize the orchestrator.
        
        Args:
            vault_path: Path to the Obsidian vault root directory
            check_interval: How often to check for work (in seconds)
        """
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval
        
        # Folder paths
        self.inbox = self.vault_path / 'Inbox'
        self.needs_action = self.vault_path / 'Needs_Action'
        self.plans = self.vault_path / 'Plans'
        self.done = self.vault_path / 'Done'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.rejected = self.vault_path / 'Rejected'
        self.logs = self.vault_path / 'Logs'
        self.dashboard = self.vault_path / 'Dashboard.md'
        
        # Ensure all folders exist
        for folder in [self.inbox, self.needs_action, self.plans, 
                       self.done, self.pending_approval, self.approved,
                       self.rejected, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        self._setup_logging()
        
        # Track processed files
        self.processed_files: set = set()
    
    def _setup_logging(self):
        """Set up logging to file and console."""
        log_file = self.logs / f'orchestrator_{datetime.now().strftime("%Y-%m-%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('Orchestrator')
    
    def count_files(self, folder: Path) -> int:
        """
        Count markdown files in a folder.
        
        Args:
            folder: Path to the folder
            
        Returns:
            Number of .md files
        """
        if not folder.exists():
            return 0
        return len(list(folder.glob('*.md')))
    
    def get_pending_tasks(self) -> List[Path]:
        """
        Get list of pending task files.
        
        Returns:
            List of paths to pending action files
        """
        if not self.needs_action.exists():
            return []
        
        tasks = []
        for filepath in self.needs_action.glob('*.md'):
            if filepath not in self.processed_files:
                tasks.append(filepath)
        
        return tasks
    
    def update_dashboard(self):
        """
        Update the Dashboard.md with current statistics.
        """
        try:
            if not self.dashboard.exists():
                self.logger.warning('Dashboard.md not found')
                return
            
            # Count items in each folder
            inbox_count = self.count_files(self.inbox)
            needs_action_count = self.count_files(self.needs_action)
            pending_approval_count = self.count_files(self.pending_approval)
            approved_count = self.count_files(self.approved)
            done_count = self.count_files(self.done)
            
            # Read current dashboard
            content = self.dashboard.read_text(encoding='utf-8')
            
            # Update statistics
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Update last_updated in frontmatter
            if 'last_updated:' in content:
                content = content.replace(
                    content.split('last_updated:')[1].split('\n')[0],
                    f' {timestamp}'
                )
            
            # Update Quick Stats table
            content = self._update_table_value(
                content, 'Pending Tasks', str(needs_action_count)
            )
            content = self._update_table_value(
                content, 'Awaiting Approval', str(pending_approval_count)
            )
            content = self._update_table_value(
                content, 'Completed Today', str(done_count)
            )
            
            # Update Inbox Status table
            content = self._update_table_value(content, '/Inbox', str(inbox_count))
            content = self._update_table_value(
                content, '/Needs_Action', str(needs_action_count)
            )
            content = self._update_table_value(
                content, '/Pending_Approval', str(pending_approval_count)
            )
            
            # Write updated dashboard
            self.dashboard.write_text(content, encoding='utf-8')
            self.logger.info('Dashboard updated')
            
        except Exception as e:
            self.logger.error(f'Error updating dashboard: {e}', exc_info=True)
    
    def _update_table_value(self, content: str, key: str, value: str) -> str:
        """
        Update a value in a markdown table.
        
        Args:
            content: Full markdown content
            key: The key to find in the table
            value: The new value
            
        Returns:
            Updated content
        """
        lines = content.split('\n')
        new_lines = []
        
        for i, line in enumerate(lines):
            if f'| {key}' in line and '|' in line:
                # This is the row with our key
                parts = line.split('|')
                if len(parts) >= 3:
                    # Reconstruct the row with new value
                    new_line = f"| {key} | {value} |"
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        return '\n'.join(new_lines)
    
    def process_tasks(self):
        """
        Process all pending tasks in Needs_Action folder.
        
        This triggers Qwen Code to analyze and create plans.
        """
        tasks = self.get_pending_tasks()
        
        if not tasks:
            self.logger.debug('No pending tasks')
            return
        
        self.logger.info(f'Found {len(tasks)} pending task(s)')
        
        for task_file in tasks:
            try:
                self.logger.info(f'Processing: {task_file.name}')
                
                # Read the task file to understand what needs to be done
                task_content = task_file.read_text(encoding='utf-8')
                
                # Create a prompt for Qwen Code
                prompt = self._create_qwen_prompt(task_file, task_content)
                
                # Trigger Qwen Code to process the task
                self.trigger_qwen_code(prompt, task_file)
                
                # Mark as processed
                self.processed_files.add(task_file)
                
            except Exception as e:
                self.logger.error(f'Error processing task {task_file.name}: {e}', exc_info=True)
    
    def _create_qwen_prompt(self, task_file: Path, task_content: str) -> str:
        """
        Create a prompt for Qwen Code based on the task.
        
        Args:
            task_file: Path to the task file
            task_content: Content of the task file
            
        Returns:
            Formatted prompt for Qwen Code
        """
        return f"""
You are the AI Employee. Process the following task from the Needs_Action folder.

Task File: {task_file.name}

Task Content:
{task_content}

---

Instructions:
1. Read the Company_Handbook.md for rules and guidelines
2. Read the Business_Goals.md for context
3. Analyze the task and determine what actions are needed
4. Create a Plan.md file in the /Plans folder with checkboxes for each step
5. Update the Dashboard.md with current status
6. If the task requires approval, create a file in /Pending_Approval
7. If the task is complete, move the task file to /Done

Remember to follow the Rules of Engagement in the Company Handbook.
"""
    
    def trigger_qwen_code(self, prompt: str, task_file: Path):
        """
        Trigger Qwen Code to process a task.
        
        Args:
            prompt: The prompt to send to Qwen Code
            task_file: Path to the task file being processed
        """
        try:
            self.logger.info('Triggering Qwen Code...')
            
            # Create a temporary prompt file
            prompt_file = self.vault_path / 'temp_prompt.txt'
            prompt_file.write_text(prompt, encoding='utf-8')
            
            # Log that we're triggering Qwen
            # In a real implementation, this would call Qwen Code API or CLI
            self.logger.info(f'Prompt created for Qwen Code: {prompt_file}')
            
            # For Bronze Tier, we create a plan file automatically
            # In higher tiers, Qwen Code would do this
            self._create_auto_plan(task_file)
            
            # Clean up
            if prompt_file.exists():
                prompt_file.unlink()
            
        except Exception as e:
            self.logger.error(f'Error triggering Qwen Code: {e}', exc_info=True)
    
    def _create_auto_plan(self, task_file: Path):
        """
        Create an automatic plan for a task (Bronze Tier fallback).
        
        Args:
            task_file: Path to the task file
        """
        try:
            task_content = task_file.read_text(encoding='utf-8')
            
            # Extract task type from filename
            task_type = task_file.stem.split('_')[0] if '_' in task_file.stem else 'general'
            
            plan_filename = f"PLAN_{task_file.stem}.md"
            plan_path = self.plans / plan_filename
            
            plan_content = f"""---
created: {datetime.now().isoformat()}
task_source: {task_file.name}
status: pending
type: {task_type}
---

# Plan for {task_file.name}

## Objective
Process and complete the task from Needs_Action folder.

## Steps

- [ ] Read and understand the task requirements
- [ ] Check Company Handbook for relevant rules
- [ ] Identify required actions
- [ ] Execute actions (or request approval if needed)
- [ ] Update Dashboard with progress
- [ ] Move task file to /Done when complete

## Notes

*Add notes and observations here*

## Completion Checklist

- [ ] All actions completed
- [ ] Dashboard updated
- [ ] Logs written
- [ ] Task file moved to /Done

---
*Auto-generated by Orchestrator (Bronze Tier)*
"""
            
            plan_path.write_text(plan_content, encoding='utf-8')
            self.logger.info(f'Plan created: {plan_filename}')
            
            # Log the action
            self._log_action('plan_created', str(task_file), str(plan_path))
            
        except Exception as e:
            self.logger.error(f'Error creating plan: {e}', exc_info=True)
    
    def _log_action(self, action_type: str, source: str, result: str):
        """
        Log an action to the logs folder.
        
        Args:
            action_type: Type of action
            source: Source file/item
            result: Result of the action
        """
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action_type': action_type,
                'source': source,
                'result': result,
                'actor': 'orchestrator'
            }
            
            log_file = self.logs / f'{datetime.now().strftime("%Y-%m-%d")}.json'
            
            # Append to log file (simple format for Bronze Tier)
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"{log_entry}\n")
                
        except Exception as e:
            self.logger.error(f'Error logging action: {e}')
    
    def check_approved_actions(self):
        """
        Check for approved actions that need execution.
        
        In Bronze Tier, this just moves files to Done as a demo.
        """
        if not self.approved.exists():
            return
        
        for approved_file in self.approved.glob('*.md'):
            try:
                self.logger.info(f'Processing approved action: {approved_file.name}')
                
                # In higher tiers, this would execute the actual action
                # For Bronze Tier, we just move to Done
                dest = self.done / approved_file.name
                shutil.move(str(approved_file), str(dest))
                
                self.logger.info(f'Moved to Done: {dest.name}')
                self._log_action('approved_executed', str(approved_file), str(dest))
                
            except Exception as e:
                self.logger.error(f'Error processing approved action: {e}', exc_info=True)
    
    def run(self):
        """
        Main run loop for the orchestrator.
        """
        self.logger.info('=' * 50)
        self.logger.info('AI Employee Orchestrator (Bronze Tier)')
        self.logger.info('=' * 50)
        self.logger.info(f'Vault Path: {self.vault_path}')
        self.logger.info(f'Check Interval: {self.check_interval} seconds')
        self.logger.info('Starting orchestrator...')
        
        try:
            while True:
                # Update dashboard
                self.update_dashboard()
                
                # Process pending tasks
                self.process_tasks()
                
                # Check approved actions
                self.check_approved_actions()
                
                # Wait for next cycle
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info('Orchestrator stopped by user')
        except Exception as e:
            self.logger.error(f'Fatal error: {e}', exc_info=True)
            raise


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Employee Orchestrator')
    parser.add_argument(
        '--vault', '-v',
        type=str,
        default=None,
        help='Path to the Obsidian vault'
    )
    parser.add_argument(
        '--interval', '-i',
        type=int,
        default=60,
        help='Check interval in seconds (default: 60)'
    )
    
    args = parser.parse_args()
    
    # Default vault path
    if args.vault:
        vault_path = Path(args.vault)
    else:
        vault_path = Path(__file__).parent / 'AI_Employee_Vault'
    
    # Create and run orchestrator
    orchestrator = Orchestrator(str(vault_path), args.interval)
    orchestrator.run()


if __name__ == "__main__":
    main()

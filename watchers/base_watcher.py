"""
Base Watcher - Abstract base class for all watcher scripts.

All watchers (Gmail, WhatsApp, Filesystem, etc.) inherit from this class
and implement the check_for_updates() and create_action_file() methods.
"""

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Any, Optional


class BaseWatcher(ABC):
    """
    Abstract base class for all watcher scripts.
    
    Watchers monitor external sources (email, messaging apps, files)
    and create actionable markdown files in the Needs_Action folder
    for the AI Employee to process.
    """
    
    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        Initialize the watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root directory
            check_interval: How often to check for updates (in seconds)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        
        # Ensure the Needs_Action folder exists
        self.needs_action.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        self._setup_logging()
        
        # Track processed items to avoid duplicates
        self.processed_ids: set = set()
        
    def _setup_logging(self):
        """Set up logging to file and console."""
        log_dir = self.vault_path / 'Logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f'watcher_{datetime.now().strftime("%Y-%m-%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def check_for_updates(self) -> List[Any]:
        """
        Check for new items to process.
        
        Returns:
            List of new items (emails, messages, files, etc.)
        """
        pass
    
    @abstractmethod
    def create_action_file(self, item: Any) -> Optional[Path]:
        """
        Create a markdown action file for an item.
        
        Args:
            item: The item to create an action file for
            
        Returns:
            Path to the created file, or None if failed
        """
        pass
    
    def _generate_filename(self, prefix: str, unique_id: str) -> str:
        """
        Generate a standardized filename.
        
        Args:
            prefix: Type prefix (EMAIL, WHATSAPP, FILE, etc.)
            unique_id: Unique identifier for the item
            
        Returns:
            Formatted filename
        """
        timestamp = datetime.now().strftime("%Y-%m-%d")
        # Sanitize the unique_id for filesystem safety
        safe_id = "".join(c if c.isalnum() or c in '-_' else '_' for c in unique_id)
        return f"{prefix}_{safe_id}_{timestamp}.md"
    
    def _create_markdown_content(self, frontmatter: dict, content: str) -> str:
        """
        Create properly formatted markdown content with frontmatter.
        
        Args:
            frontmatter: Dictionary of frontmatter fields
            content: Main content body
            
        Returns:
            Formatted markdown string
        """
        fm_lines = ["---"]
        for key, value in frontmatter.items():
            fm_lines.append(f"{key}: {value}")
        fm_lines.append("---")
        fm_lines.append("")
        fm_lines.append(content)
        
        return "\n".join(fm_lines)
    
    def run(self):
        """
        Main run loop for the watcher.
        
        Continuously checks for updates and creates action files.
        Runs until interrupted (Ctrl+C).
        """
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval} seconds')
        
        try:
            while True:
                try:
                    items = self.check_for_updates()
                    if items:
                        self.logger.info(f'Found {len(items)} new item(s)')
                        for item in items:
                            filepath = self.create_action_file(item)
                            if filepath:
                                self.logger.info(f'Created action file: {filepath.name}')
                    else:
                        self.logger.debug('No new items')
                except Exception as e:
                    self.logger.error(f'Error processing items: {e}', exc_info=True)
                
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            self.logger.info(f'{self.__class__.__name__} stopped by user')
        except Exception as e:
            self.logger.error(f'Fatal error: {e}', exc_info=True)
            raise


if __name__ == "__main__":
    # This is an abstract class - should not be run directly
    print("BaseWatcher is an abstract class. Use a concrete implementation like FilesystemWatcher.")

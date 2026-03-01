"""
Filesystem Watcher - Monitors a drop folder for new files.

When a new file is detected, it creates a corresponding markdown action file
in the Needs_Action folder for the AI Employee to process.

This is the Bronze Tier watcher implementation.
"""

import shutil
import hashlib
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from base_watcher import BaseWatcher


class FileDropHandler(FileSystemEventHandler):
    """
    Handles file system events for the drop folder.
    
    When a new file is created, it triggers the FilesystemWatcher
    to create an action file.
    """
    
    def __init__(self, watcher: 'FilesystemWatcher'):
        """
        Initialize the handler.
        
        Args:
            watcher: The FilesystemWatcher instance to notify
        """
        self.watcher = watcher
    
    def on_created(self, event):
        """
        Handle file creation events.
        
        Args:
            event: The file system event
        """
        if event.is_directory:
            return
        
        self.watcher.process_new_file(Path(event.src_path))


class FilesystemWatcher(BaseWatcher):
    """
    Watches a drop folder for new files and creates action files.
    
    This is the primary watcher for Bronze Tier implementation.
    """
    
    def __init__(self, vault_path: str, drop_folder: Optional[str] = None, check_interval: int = 30):
        """
        Initialize the filesystem watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root directory
            drop_folder: Path to the drop folder (defaults to vault/Inbox)
            check_interval: How often to check for updates (in seconds)
        """
        super().__init__(vault_path, check_interval)
        
        # Set up drop folder
        if drop_folder:
            self.drop_folder = Path(drop_folder)
        else:
            self.drop_folder = self.vault_path / 'Inbox'
        
        self.drop_folder.mkdir(parents=True, exist_ok=True)
        
        # Track processed files by hash to avoid duplicates
        self.processed_files: Dict[str, str] = {}  # hash -> filename
        
        # Keywords for priority classification
        self.priority_keywords = ['urgent', 'asap', 'invoice', 'payment', 'contract', 'legal']
    
    def _get_file_hash(self, filepath: Path) -> str:
        """
        Calculate MD5 hash of a file for duplicate detection.
        
        Args:
            filepath: Path to the file
            
        Returns:
            MD5 hash string
        """
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def _classify_priority(self, filename: str) -> str:
        """
        Classify file priority based on filename keywords.
        
        Args:
            filename: The name of the file
            
        Returns:
            Priority level: 'high' or 'normal'
        """
        filename_lower = filename.lower()
        for keyword in self.priority_keywords:
            if keyword in filename_lower:
                return 'high'
        return 'normal'
    
    def _get_file_type(self, filepath: Path) -> str:
        """
        Determine file type based on extension.
        
        Args:
            filepath: Path to the file
            
        Returns:
            File type description
        """
        ext_map = {
            '.pdf': 'PDF Document',
            '.doc': 'Word Document',
            '.docx': 'Word Document',
            '.xls': 'Excel Spreadsheet',
            '.xlsx': 'Excel Spreadsheet',
            '.csv': 'CSV File',
            '.txt': 'Text File',
            '.md': 'Markdown File',
            '.jpg': 'Image',
            '.jpeg': 'Image',
            '.png': 'Image',
            '.gif': 'Image',
            '.zip': 'Archive',
            '.rar': 'Archive',
        }
        return ext_map.get(filepath.suffix.lower(), 'Unknown File')
    
    def process_new_file(self, filepath: Path):
        """
        Process a newly detected file.
        
        Args:
            filepath: Path to the new file
        """
        if not filepath.exists():
            return
        
        # Calculate hash for duplicate detection
        file_hash = self._get_file_hash(filepath)
        
        if file_hash in self.processed_files:
            self.logger.debug(f'File already processed: {filepath.name}')
            return
        
        # Create action file
        action_file = self.create_action_file({
            'filepath': filepath,
            'filename': filepath.name,
            'hash': file_hash
        })
        
        if action_file:
            self.processed_files[file_hash] = filepath.name
            self.logger.info(f'Processed new file: {filepath.name}')
    
    def check_for_updates(self) -> List[Dict[str, Any]]:
        """
        Check for new files in the drop folder.
        
        Returns:
            List of new file information dictionaries
        """
        new_files = []
        
        if not self.drop_folder.exists():
            return new_files
        
        for filepath in self.drop_folder.iterdir():
            if filepath.is_file():
                file_hash = self._get_file_hash(filepath)
                
                if file_hash not in self.processed_files:
                    new_files.append({
                        'filepath': filepath,
                        'filename': filepath.name,
                        'hash': file_hash
                    })
        
        return new_files
    
    def create_action_file(self, item: Dict[str, Any]) -> Optional[Path]:
        """
        Create a markdown action file for a new file drop.
        
        Args:
            item: Dictionary containing file information
            
        Returns:
            Path to the created action file, or None if failed
        """
        try:
            filepath = item['filepath']
            filename = item['filename']
            file_hash = item['hash']
            
            # Get file metadata
            stat = filepath.stat()
            file_size = stat.st_size
            created_time = datetime.fromtimestamp(stat.st_ctime).isoformat()
            modified_time = datetime.fromtimestamp(stat.st_mtime).isoformat()
            
            # Classify priority
            priority = self._classify_priority(filename)
            file_type = self._get_file_type(filepath)
            
            # Generate unique ID from hash (first 8 characters)
            unique_id = file_hash[:8]
            
            # Create frontmatter
            frontmatter = {
                'type': 'file_drop',
                'original_name': filename,
                'file_type': file_type,
                'size': file_size,
                'priority': priority,
                'status': 'pending',
                'received': datetime.now().isoformat(),
                'file_hash': file_hash
            }
            
            # Create content
            content = f'''### File Information

- **Original Name:** {filename}
- **File Type:** {file_type}
- **Size:** {self._format_size(file_size)}
- **Created:** {created_time}
- **Modified:** {modified_time}
- **Priority:** {priority.upper()}

### File Location

- **Drop Folder:** `{filepath}`
- **Action File:** `{self.needs_action / self._generate_filename('FILE', unique_id)}.md`

### Suggested Actions

- [ ] Review file contents
- [ ] Categorize and move to appropriate folder
- [ ] Take required action
- [ ] Move to /Done when complete

### Notes

*Add notes here after reviewing the file*

---
*Auto-generated by Filesystem Watcher*
'''
            
            # Generate filename
            action_filename = self._generate_filename('FILE', unique_id)
            action_filepath = self.needs_action / action_filename
            
            # Write the action file
            markdown_content = self._create_markdown_content(frontmatter, content)
            action_filepath.write_text(markdown_content, encoding='utf-8')
            
            # Copy the original file to vault for reference
            files_folder = self.vault_path / 'Files'
            files_folder.mkdir(parents=True, exist_ok=True)
            dest_path = files_folder / filename
            
            # Handle duplicate filenames
            counter = 1
            while dest_path.exists():
                stem = filepath.stem
                suffix = filepath.suffix
                dest_path = files_folder / f"{stem}_{counter}{suffix}"
                counter += 1
            
            shutil.copy2(filepath, dest_path)
            self.logger.info(f'Copied file to: {dest_path}')
            
            return action_filepath
            
        except Exception as e:
            self.logger.error(f'Error creating action file: {e}', exc_info=True)
            return None
    
    def _format_size(self, size_bytes: int) -> str:
        """
        Format file size in human-readable format.
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            Formatted size string
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def run_with_observer(self):
        """
        Run the watcher using watchdog observer (recommended for production).
        
        This provides real-time file monitoring instead of polling.
        """
        self.logger.info(f'Starting FilesystemWatcher with observer')
        self.logger.info(f'Drop folder: {self.drop_folder}')
        
        event_handler = FileDropHandler(self)
        observer = Observer()
        observer.schedule(event_handler, str(self.drop_folder), recursive=False)
        observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            self.logger.info('FilesystemWatcher stopped by user')
        observer.join()


if __name__ == "__main__":
    import sys
    import time
    
    # Default vault path
    vault_path = Path(__file__).parent.parent / 'AI_Employee_Vault'
    
    # Allow override via command line
    if len(sys.argv) > 1:
        vault_path = Path(sys.argv[1])
    
    print(f"Filesystem Watcher - Bronze Tier")
    print(f"Vault Path: {vault_path}")
    print(f"Drop Folder: {vault_path / 'Inbox'}")
    print(f"\nWatching for new files... (Press Ctrl+C to stop)")
    print(f"Drop files into: {vault_path / 'Inbox'}")
    print("-" * 50)
    
    watcher = FilesystemWatcher(str(vault_path))
    
    # Use observer-based watching for real-time detection
    watcher.run_with_observer()

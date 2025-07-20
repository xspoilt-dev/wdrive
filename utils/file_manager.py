# File Manager for wdrive
import os
import shutil
from datetime import datetime
from pathlib import Path


class FileManager:
    def __init__(self, upload_folder):
        self.upload_folder = Path(upload_folder)
        self.upload_folder.mkdir(parents=True, exist_ok=True)
    
    def get_files(self, search_query=""):
        """Get list of files in the upload folder with metadata."""
        files = []
        
        try:
            for file_path in self.upload_folder.iterdir():
                if file_path.is_file():
                    # Apply search filter
                    if search_query and search_query.lower() not in file_path.name.lower():
                        continue
                    
                    stat = file_path.stat()
                    file_info = {
                        'name': file_path.name,
                        'size': self._format_file_size(stat.st_size),
                        'size_bytes': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                        'type': self._get_file_type(file_path.name),
                        'extension': file_path.suffix.lower(),
                        'is_image': self._is_image(file_path.name),
                        'is_video': self._is_video(file_path.name),
                        'is_audio': self._is_audio(file_path.name),
                        'is_document': self._is_document(file_path.name),
                    }
                    files.append(file_info)
            
            # Sort files by modification time (newest first)
            files.sort(key=lambda x: x['modified'], reverse=True)
            
        except Exception as e:
            print(f"Error listing files: {str(e)}")
        
        return files
    
    def delete_file(self, filename):
        """Delete a file from the upload folder."""
        try:
            file_path = self.upload_folder / filename
            if file_path.exists() and file_path.is_file():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting file {filename}: {str(e)}")
            return False
    
    def rename_file(self, old_name, new_name):
        """Rename a file in the upload folder."""
        try:
            old_path = self.upload_folder / old_name
            new_path = self.upload_folder / new_name
            
            if old_path.exists() and not new_path.exists():
                old_path.rename(new_path)
                return True
            return False
        except Exception as e:
            print(f"Error renaming file {old_name} to {new_name}: {str(e)}")
            return False
    
    def get_file_path(self, filename):
        """Get the full path to a file."""
        return self.upload_folder / filename
    
    def _format_file_size(self, size_bytes):
        """Format file size in human readable format."""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def _get_file_type(self, filename):
        """Determine file type based on extension."""
        extension = Path(filename).suffix.lower()
        
        if extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp']:
            return 'Image'
        elif extension in ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']:
            return 'Video'
        elif extension in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma']:
            return 'Audio'
        elif extension in ['.pdf']:
            return 'PDF'
        elif extension in ['.doc', '.docx']:
            return 'Word Document'
        elif extension in ['.xls', '.xlsx']:
            return 'Excel Spreadsheet'
        elif extension in ['.ppt', '.pptx']:
            return 'PowerPoint'
        elif extension in ['.txt', '.md', '.rtf']:
            return 'Text Document'
        elif extension in ['.zip', '.rar', '.7z', '.tar', '.gz']:
            return 'Archive'
        elif extension in ['.exe', '.msi', '.dmg', '.pkg']:
            return 'Executable'
        else:
            return 'Unknown'
    
    def _is_image(self, filename):
        """Check if file is an image."""
        extension = Path(filename).suffix.lower()
        return extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp']
    
    def _is_video(self, filename):
        """Check if file is a video."""
        extension = Path(filename).suffix.lower()
        return extension in ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
    
    def _is_audio(self, filename):
        """Check if file is audio."""
        extension = Path(filename).suffix.lower()
        return extension in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma']
    
    def _is_document(self, filename):
        """Check if file is a document."""
        extension = Path(filename).suffix.lower()
        return extension in ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.xls', '.xlsx', '.ppt', '.pptx']


if __name__ == "__main__":
    # Test file manager
    fm = FileManager("shared")
    files = fm.get_files()
    print(f"Found {len(files)} files:")
    for file_info in files:
        print(f"- {file_info['name']} ({file_info['size']}) - {file_info['type']}")

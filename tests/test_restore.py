import os
import shutil
import tempfile
import pytest
from unittest.mock import patch
from pathlib import Path
from cleanenv.services.restore import restore_backup

@pytest.fixture
def mock_backup_env(monkeypatch):
    temp_dir = tempfile.mkdtemp()
    backup_root = Path(temp_dir) / ".cleanenv_backup"
    backup_folder = backup_root / "backups"
    
    # Mock the constants in the module directly where they are imported
    monkeypatch.setattr("cleanenv.services.restore.BACKUP_FOLDER", backup_folder)
    
    yield temp_dir, backup_folder
    
    shutil.rmtree(temp_dir)

def test_restore_backup_not_found():
    # Attempting to restore an id that isn't in metadata
    def mock_load_metadata():
        return {}
        
    with pytest.raises(ValueError, match="Backup not found"):
        with patch("cleanenv.services.restore.load_metadata", mock_load_metadata):
            restore_backup("missing_id")

def test_restore_backup_dir_missing(mock_backup_env):
    temp_dir, backup_folder = mock_backup_env
    
    original_path = os.path.join(temp_dir, "original", "node_modules")
    
    metadata = {
        "fake_id": {
            "original_path": original_path,
            "type": "node_modules"
        }
    }
    
    with patch("cleanenv.services.restore.load_metadata", return_value=metadata):
        # We did not create the backup directory "fake_id", so it's missing
        with pytest.raises(ValueError, match="Backup directory missing"):
            restore_backup("fake_id")

def test_restore_backup_folder_empty(mock_backup_env):
    temp_dir, backup_folder = mock_backup_env
    backup_id = "fake_id"
    original_path = os.path.join(temp_dir, "original", "node_modules")
    
    # Create the backup directory but nothing inside it
    backup_dir = backup_folder / backup_id
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    metadata = {
        backup_id: {
            "original_path": original_path,
            "type": "node_modules"
        }
    }
    
    with patch("cleanenv.services.restore.load_metadata", return_value=metadata):
        with pytest.raises(ValueError, match="Backup folder empty"):
            restore_backup(backup_id)

def test_restore_backup_success(mock_backup_env):
    temp_dir, backup_folder = mock_backup_env
    backup_id = "fake_id"
    
    # Original path logic
    original_base = os.path.join(temp_dir, "original")
    os.makedirs(original_base)
    original_path = os.path.join(original_base, "node_modules")
    
    # Create backup directory and content
    backup_dir = backup_folder / backup_id
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Create the backed up folder itself inside the backup_dir
    backed_up_folder = backup_dir / "node_modules"
    backed_up_folder.mkdir()
    
    # Also put a file inside to verify it transfers
    test_file = backed_up_folder / "test.txt"
    with open(test_file, "w") as f:
        f.write("hello world")
    
    metadata = {
        backup_id: {
            "original_path": original_path,
            "type": "node_modules"
        }
    }
    
    saved_metadata = {}
    
    def mock_save_metadata(data):
        nonlocal saved_metadata
        saved_metadata = data
        
    with patch("cleanenv.services.restore.load_metadata", return_value=metadata):
        with patch("cleanenv.services.restore.save_metadata", mock_save_metadata):
            restored_path = restore_backup(backup_id)
            
            # Check it returned the correct original path
            assert str(restored_path) == str(original_path)
            
            # Verify the folder was actually moved
            assert os.path.exists(original_path)
            assert os.path.exists(os.path.join(original_path, "test.txt"))
            
            # Verify backup_dir is cleaned up
            assert not backup_dir.exists()
            
            # Verify metadata was popped
            assert backup_id not in saved_metadata

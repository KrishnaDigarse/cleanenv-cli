import os
import shutil
import json
import time
from pathlib import Path

BACKUP_ROOT = Path.home() / ".cleanenv_backup"
BACKUP_FOLDER = BACKUP_ROOT / "backups"
METADATA_FILE = BACKUP_ROOT / "metadata.json"


def initialize_backup_system():
    """Ensure backup folders and metadata file exist"""

    BACKUP_FOLDER.mkdir(parents=True, exist_ok=True)

    if not METADATA_FILE.exists():
        with open(METADATA_FILE, "w") as f:
            json.dump({}, f)


def load_metadata():
    with open(METADATA_FILE) as f:
        return json.load(f)


def save_metadata(data):
    with open(METADATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def backup_folder(path):
    """
    Move folder to backup location and record metadata
    """

    initialize_backup_system()

    backup_id = f"backup_{int(time.time())}"

    backup_dir = BACKUP_FOLDER / backup_id
    backup_dir.mkdir()

    folder_name = os.path.basename(path)
    destination = backup_dir / folder_name

    shutil.move(path, destination)

    metadata = load_metadata()

    metadata[backup_id] = {
        "original_path": path,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "type": folder_name,
    }

    save_metadata(metadata)

    return backup_id, destination
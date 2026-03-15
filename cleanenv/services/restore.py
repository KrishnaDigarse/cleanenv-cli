import shutil
from pathlib import Path
import json

from cleanenv.services.backup import BACKUP_FOLDER, METADATA_FILE


def load_metadata():
    with open(METADATA_FILE) as f:
        return json.load(f)


def restore_backup(backup_id):
    metadata = load_metadata()

    if backup_id not in metadata:
        raise ValueError("Backup not found")

    info = metadata[backup_id]

    original_path = Path(info["original_path"])
    backup_dir = BACKUP_FOLDER / backup_id

    # find the folder inside backup directory
    items = list(backup_dir.iterdir())

    if not items:
        raise ValueError("Backup folder empty")

    folder = items[0]

    shutil.move(str(folder), str(original_path))

    return original_path
import shutil
from pathlib import Path

from cleanenv.services.backup import BACKUP_FOLDER, load_metadata, save_metadata


def restore_backup(backup_id):
    metadata = load_metadata()

    if backup_id not in metadata:
        raise ValueError("Backup not found")

    info = metadata[backup_id]

    original_path = Path(info["original_path"])
    backup_dir = BACKUP_FOLDER / backup_id

    # find the folder inside backup directory
    if not backup_dir.exists():
        raise ValueError("Backup directory missing")

    items = list(backup_dir.iterdir())

    if not items:
        raise ValueError("Backup folder empty")

    folder = items[0]

    shutil.move(str(folder), str(original_path))
    shutil.rmtree(str(backup_dir), ignore_errors=True)

    metadata.pop(backup_id, None)
    save_metadata(metadata)

    return original_path
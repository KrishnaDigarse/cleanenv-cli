import os
from cleanenv.core.projects import is_project_root

TARGET_DIRS = {"node_modules", "venv", ".venv", "__pycache__", ".pytest_cache"}

SKIP_DIRS = {
    "Windows",
    "Program Files",
    "Program Files (x86)",
    "$Recycle.Bin",
    "System Volume Information",
    ".Trash",
    ".Trashes"
}

def is_venv(path):
    """Check if the directory is a valid Python virtual environment."""
    return os.path.isfile(os.path.join(path, "pyvenv.cfg")) or \
           os.path.isdir(os.path.join(path, "Scripts")) or \
           os.path.isdir(os.path.join(path, "bin"))

def scan_directory(root):
    results = []
    stack = [root]

    while stack:
        current = stack.pop()

        try:
            with os.scandir(current) as entries:
                for entry in entries:

                    if not entry.is_dir(follow_symlinks=False):
                        continue

                    # Skip large system directories
                    if entry.name in SKIP_DIRS:
                        continue

                    # Detect dependency folders
                    if entry.name in TARGET_DIRS:
                        if entry.name in {"venv", ".venv"} and not is_venv(entry.path):
                            # Not a real venv, treat as regular directory
                            stack.append(entry.path)
                            continue

                        results.append(entry.path)

                        # Stop recursion inside dependency folders
                        continue

                    # Detect project roots
                    if is_project_root(entry.path):
                        stack.append(entry.path)
                        continue

                    stack.append(entry.path)

        except PermissionError:
            pass

    return results
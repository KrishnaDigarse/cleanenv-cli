import os

PROJECT_MARKERS = {
    ".git",
    "package.json",
    "pyproject.toml",
    "requirements.txt",
}


def is_project_root(path):
    """Check if folder is a project root"""

    try:
        files = os.listdir(path)
    except PermissionError:
        return False

    return any(marker in files for marker in PROJECT_MARKERS)
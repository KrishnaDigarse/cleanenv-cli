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

def find_projects(root):
    """Find project directories"""

    projects = []
    stack = [root]

    while stack:
        current = stack.pop()

        try:
            entries = os.scandir(current)
        except PermissionError:
            continue

        if is_project_root(current):
            projects.append(current)
            continue

        for entry in entries:
            if entry.is_dir(follow_symlinks=False):
                stack.append(entry.path)

    return projects
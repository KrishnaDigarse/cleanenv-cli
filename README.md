# CleanEnv 🧹

CleanEnv is a fast and safe CLI utility built to clean up your development environments by safely archiving bulky dependency folders like `node_modules` and Python virtual environments (`venv`, `.venv`, `__pycache__`). 

Instead of permanently deleting folders right away, CleanEnv moves them to a secure, timestamped backup location so they can easily be restored if needed.

## Features
- **Cross-Platform:** Works seamlessly on Windows, macOS, and Linux.
- **Safe:** Moves files to a local backup instead of permanently deleting them.
- **Smart Detection:** Automatically verifies if a `venv` is actually a python virtual environment, and ignores large system directories to speed up scanning.
- **Restore:** Accidental deletion? Simply run the restore command to place the files exactly where they were.
- **Dependency Saving:** Automatically runs `pip freeze > requirements.txt` before backing up a Python virtual environment to make it easier to rebuild later.

## Installation

CleanEnv can be installed globally directly from the source code using `pip` or `pipx`.

```bash
# Clone the repository
git clone https://github.com/KrishnaDigarse/cleanenv-cli.git
cd cleanenv-cli

# Install globally using pip
pip install .

# Or install without polluting your global packages using pipx
pipx install .
```

To install it for local development (editable mode):
```bash
pip install -e .
```

## Usage

Once installed, the `cleanenv` command will be available globally in your terminal. 

### 1. Scan for Clutter
Preview how much space you can reclaim in a specific directory without actually deleting anything.
```bash
cleanenv scan /path/to/your/projects
```

### 2. Clean Environments
Clean the environments in a target directory. The folders will be moved to your local `~/.cleanenv_backup/` directory.
```bash
cleanenv clean /path/to/your/projects
```

### 3. Restore Backups
If you accidentally cleaned a folder that you still need, you can list all available backups and restore them.

View a list of available backups:
```bash
cleanenv restore
```

Restore a specific backup by its index number (e.g., restore the 2nd item in the list):
```bash
cleanenv restore 2
```

## Testing

CleanEnv has a comprehensive test suite covering the core modules (`size`, `projects`, `scanner`) and services (`requirements`, `restore`). It also includes CLI tests to verify terminal output and interactions.

To run the tests, first install the developer dependencies:

```bash
pip install -e .[dev]
```

Run the `pytest` suite:

```bash
pytest tests/
```

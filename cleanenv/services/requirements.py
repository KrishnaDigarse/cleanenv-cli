import os
import subprocess

def generate_requirements(venv_path):
    project_dir = os.path.dirname(venv_path)
    req_file = os.path.join(project_dir, "requirements.txt")

    if os.path.exists(req_file):
        return

    is_windows = os.name == 'nt'
    pip_dir = "Scripts" if is_windows else "bin"
    pip_exe = "pip.exe" if is_windows else "pip"
    pip_path = os.path.join(venv_path, pip_dir, pip_exe)

    try:
        if os.path.exists(pip_path):
            with open(req_file, "w") as f:
                subprocess.run([pip_path, "freeze"], stdout=f, check=True)
        else:
            print(f"Warning: pip executable not found at {pip_path}")
    except Exception as e:
        print(f"Warning: Failed to generate requirements.txt - {e}")
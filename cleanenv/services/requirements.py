import os
import subprocess

def generate_requirements(venv_path):
    project_dir = os.path.dirname(venv_path)
    req_file = os.path.join(project_dir, "requirements.txt")

    if os.path.exists(req_file):
        return

    pip_path = os.path.join(venv_path, "Scripts", "pip.exe")

    try:
        with open(req_file, "w") as f:
            subprocess.run([pip_path, "freeze"], stdout=f)

    except:
        pass
import os
import tempfile
import pytest
from cleanenv.core.projects import is_project_root, PROJECT_MARKERS

def test_is_project_root_with_git():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.makedirs(os.path.join(temp_dir, ".git"))
        assert is_project_root(temp_dir) is True

def test_is_project_root_with_package_json():
    with tempfile.TemporaryDirectory() as temp_dir:
        with open(os.path.join(temp_dir, "package.json"), "w") as f:
            f.write("{}")
        assert is_project_root(temp_dir) is True

def test_is_project_root_with_pyproject_toml():
    with tempfile.TemporaryDirectory() as temp_dir:
        with open(os.path.join(temp_dir, "pyproject.toml"), "w") as f:
            f.write("")
        assert is_project_root(temp_dir) is True

def test_not_project_root():
    with tempfile.TemporaryDirectory() as temp_dir:
        with open(os.path.join(temp_dir, "random_file.txt"), "w") as f:
            f.write("hello")
        assert is_project_root(temp_dir) is False

def test_empty_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        assert is_project_root(temp_dir) is False

def test_permission_error(monkeypatch):
    def mock_listdir(path):
        raise PermissionError("Access Denied")
    
    monkeypatch.setattr(os, "listdir", mock_listdir)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Should gracefully handle PermissionError and return False
        assert is_project_root(temp_dir) is False

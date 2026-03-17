import os
import subprocess
import tempfile
from unittest.mock import patch, mock_open
from cleanenv.services.requirements import generate_requirements

def test_generate_requirements_already_exists():
    with tempfile.TemporaryDirectory() as temp_dir:
        venv_path = os.path.join(temp_dir, "venv")
        os.makedirs(venv_path)
        
        req_file = os.path.join(temp_dir, "requirements.txt")
        with open(req_file, "w") as f:
            f.write("flask==2.0.1")
            
        with patch("subprocess.run") as mock_run:
            generate_requirements(venv_path)
            # Should not call subprocess because file already exists
            mock_run.assert_not_called()

def test_generate_requirements_success(monkeypatch):
    with tempfile.TemporaryDirectory() as temp_dir:
        venv_path = os.path.join(temp_dir, "venv")
        os.makedirs(venv_path)
        req_file = os.path.join(temp_dir, "requirements.txt")
        
        # Mock pip executable existence
        original_exists = os.path.exists
        def mock_exists(path):
            if "pip" in path or "pip.exe" in path:
                return True
            return original_exists(path)
            
        monkeypatch.setattr(os.path, "exists", mock_exists)
        
        with patch("subprocess.run") as mock_run:
            generate_requirements(venv_path)
            # Should have called subprocess to generate requirements
            mock_run.assert_called_once()
            
            # Check arguments
            args, kwargs = mock_run.call_args
            assert "freeze" in args[0]
            assert "stdout" in kwargs

def test_generate_requirements_no_pip(monkeypatch):
    with tempfile.TemporaryDirectory() as temp_dir:
        venv_path = os.path.join(temp_dir, "venv")
        os.makedirs(venv_path)
        
        # Mock pip not existing
        original_exists = os.path.exists
        def mock_exists(path):
            if "pip" in path or "pip.exe" in path:
                return False
            return original_exists(path)
            
        monkeypatch.setattr(os.path, "exists", mock_exists)
        
        with patch("subprocess.run") as mock_run:
            generate_requirements(venv_path)
            # Should not call subprocess because pip was not found
            mock_run.assert_not_called()

def test_generate_requirements_exception(monkeypatch):
    with tempfile.TemporaryDirectory() as temp_dir:
        venv_path = os.path.join(temp_dir, "venv")
        os.makedirs(venv_path)
        
        # Mock pip executable existence
        original_exists = os.path.exists
        def mock_exists(path):
            if "pip" in path or "pip.exe" in path:
                return True
            return original_exists(path)
            
        monkeypatch.setattr(os.path, "exists", mock_exists)
        
        with patch("subprocess.run", side_effect=Exception("mocked error")) as mock_run:
            # Should handle exception gracefully
            generate_requirements(venv_path)
            mock_run.assert_called_once()

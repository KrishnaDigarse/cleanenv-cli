import os
import tempfile
import pytest
from cleanenv.core.scanner import scan_directory, is_venv

def test_is_venv_with_pyvenv_cfg():
    with tempfile.TemporaryDirectory() as temp_dir:
        with open(os.path.join(temp_dir, "pyvenv.cfg"), "w") as f:
            f.write("home = /usr/bin")
        assert is_venv(temp_dir) is True

def test_is_venv_with_scripts_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.makedirs(os.path.join(temp_dir, "Scripts"))
        assert is_venv(temp_dir) is True

def test_is_venv_with_bin_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.makedirs(os.path.join(temp_dir, "bin"))
        assert is_venv(temp_dir) is True

def test_not_venv():
    with tempfile.TemporaryDirectory() as temp_dir:
        with open(os.path.join(temp_dir, "random_file.txt"), "w") as f:
            f.write("hello")
        assert is_venv(temp_dir) is False

def test_scan_directory_finds_node_modules():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a mock project
        project_dir = os.path.join(temp_dir, "my_project")
        os.makedirs(project_dir)
        with open(os.path.join(project_dir, "package.json"), "w") as f:
            f.write("{}")
            
        # Create node_modules inside the project
        node_modules = os.path.join(project_dir, "node_modules")
        os.makedirs(node_modules)
        
        results = scan_directory(temp_dir)
        assert len(results) == 1
        assert results[0] == node_modules

def test_scan_directory_finds_venv():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a mock venv
        venv_dir = os.path.join(temp_dir, ".venv")
        os.makedirs(venv_dir)
        with open(os.path.join(venv_dir, "pyvenv.cfg"), "w") as f:
            f.write("home = /usr/bin")
            
        results = scan_directory(temp_dir)
        assert len(results) == 1
        assert results[0] == venv_dir

def test_scan_directory_skips_fake_venv():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a directory named ".venv" but not a real venv
        fake_venv = os.path.join(temp_dir, ".venv")
        os.makedirs(fake_venv)
        os.makedirs(os.path.join(fake_venv, "some_folder"))
        
        results = scan_directory(temp_dir)
        assert len(results) == 0

def test_scan_directory_skips_system_dirs():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a skipped directory like "Windows"
        win_dir = os.path.join(temp_dir, "Windows")
        os.makedirs(win_dir)
        # Put a node_modules inside it
        os.makedirs(os.path.join(win_dir, "node_modules"))
        
        results = scan_directory(temp_dir)
        # Should be empty because it shouldn't scan inside "Windows"
        assert len(results) == 0

def test_scan_directory_skips_own_dir(monkeypatch):
    with tempfile.TemporaryDirectory() as temp_dir:
        # We need to mock os.path.abspath and __file__ context inside scanner.py
        # But an easier way is to just call it where temp_dir IS the own_dir
        
        own_dir = temp_dir
        
        def mock_dirname(*args, **kwargs):
            return ""

        def mock_abspath(path):
            if "__file__" in path or path == "":
                return own_dir
            return os.path.join(own_dir, path) if not os.path.isabs(path) else path
            
        # Patching __file__ is hard, so we'll patch the abspath to return temp_dir for own_dir
        # Actually scanner uses os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        import cleanenv.core.scanner as scanner
        
        original_own_dir = scanner.OWN_DIR
        scanner.OWN_DIR = os.path.normcase(os.path.abspath(temp_dir))
        
        # Create something that would normally be found
        os.makedirs(os.path.join(temp_dir, "node_modules"))
        
        try:
            results = scan_directory(temp_dir)
            assert len(results) == 0 # Should skip since it matches own_dir
        finally:
            scanner.OWN_DIR = original_own_dir

import os
import tempfile
import pytest
from typer.testing import CliRunner
from unittest.mock import patch
from cleanenv.cli import app

runner = CliRunner()

def test_app_no_command():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "CleanEnv:" in result.stdout
    assert "scan" in result.stdout
    assert "clean" in result.stdout
    assert "restore" in result.stdout

def test_scan_no_results():
    with patch("cleanenv.commands.scan.scan_directory", return_value=[]):
        result = runner.invoke(app, ["scan", "."])
        assert result.exit_code == 0
        assert "No environments found." in result.stdout

def test_scan_with_results():
    with patch("cleanenv.commands.scan.scan_directory", return_value=["/fake/node_modules", "/fake/venv"]):
        with patch("cleanenv.commands.scan.get_directory_size", return_value=1024):
            result = runner.invoke(app, ["scan", "."])
            assert result.exit_code == 0
            assert "CleanEnv Results" in result.stdout
            assert "/fake/node_modules" in result.stdout
            assert "/fake/venv" in result.stdout
            assert "Total reclaimable" in result.stdout

def test_clean_no_results():
    with patch("cleanenv.commands.clean.scan_directory", return_value=[]):
        result = runner.invoke(app, ["clean", "."])
        assert result.exit_code == 0
        assert "Nothing to clean" in result.stdout

def test_clean_with_results():
    with patch("cleanenv.commands.clean.scan_directory", return_value=["/fake/node_modules"]):
        with patch("cleanenv.commands.clean.backup_folder", return_value=("backup_id_123", "/fake/backup")):
            result = runner.invoke(app, ["clean", "."])
            assert result.exit_code == 0
            assert "Cleaning environments" in result.stdout
            assert "Moved" in result.stdout
            assert "/fake/node_modules" in result.stdout

def test_restore_success():
    mock_metadata = {
        "backup_id_123": {
            "type": "node_modules",
            "original_path": "/fake/node_modules"
        }
    }
    with patch("cleanenv.commands.restore.load_metadata", return_value=mock_metadata):
        with patch("cleanenv.commands.restore.restore_backup", return_value="/fake/node_modules"):
            result = runner.invoke(app, ["restore", "1"])
            assert result.exit_code == 0
            assert "Restored to" in result.stdout
            assert "/fake/node_modules" in result.stdout

def test_restore_failure():
    mock_metadata = {
        "backup_id_123": {
            "type": "node_modules",
            "original_path": "/fake/node_modules"
        }
    }
    with patch("cleanenv.commands.restore.load_metadata", return_value=mock_metadata):
        with patch("cleanenv.commands.restore.restore_backup", side_effect=ValueError("Backup not found")):
            result = runner.invoke(app, ["restore", "1"])
            assert result.exit_code == 0
            assert "Failed to restore backup" in result.stdout

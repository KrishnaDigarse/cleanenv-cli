import os
import tempfile
import pytest
from cleanenv.core.size import get_directory_size, human_readable

def test_human_readable_bytes():
    assert human_readable(500) == "500.00 B"
    assert human_readable(1023) == "1023.00 B"

def test_human_readable_kb():
    assert human_readable(1024) == "1.00 KB"
    assert human_readable(1536) == "1.50 KB"

def test_human_readable_mb():
    assert human_readable(1024 * 1024) == "1.00 MB"
    assert human_readable(1024 * 1024 * 2.5) == "2.50 MB"

def test_human_readable_gb_tb():
    assert human_readable(1024**3) == "1.00 GB"
    assert human_readable(1024**4) == "1.00 TB"

def test_get_directory_size():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create some files with known sizes
        file1 = os.path.join(temp_dir, "file1.txt")
        file2 = os.path.join(temp_dir, "file2.txt")
        
        with open(file1, "wb") as f:
            f.write(b"0" * 100)  # 100 bytes
            
        with open(file2, "wb") as f:
            f.write(b"1" * 200)  # 200 bytes
            
        # Create a subfolder
        sub_dir = os.path.join(temp_dir, "sub")
        os.makedirs(sub_dir)
        file3 = os.path.join(sub_dir, "file3.txt")
        
        with open(file3, "wb") as f:
            f.write(b"2" * 50)   # 50 bytes

        size = get_directory_size(temp_dir)
        assert size == 350

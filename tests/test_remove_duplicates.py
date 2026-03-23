import os
import hashlib
import tempfile
import shutil
import pytest
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from remove_duplicates import calculate_file_hash, find_duplicate_files, remove_duplicate_files


class TestCalculateFileHash:
    def test_same_content_same_hash(self, tmp_path):
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("hello world")
        file2.write_text("hello world")
        
        hash1 = calculate_file_hash(str(file1))
        hash2 = calculate_file_hash(str(file2))
        
        assert hash1 == hash2
    
    def test_different_content_different_hash(self, tmp_path):
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("hello world")
        file2.write_text("goodbye world")
        
        hash1 = calculate_file_hash(str(file1))
        hash2 = calculate_file_hash(str(file2))
        
        assert hash1 != hash2
    
    def test_empty_file(self, tmp_path):
        file1 = tmp_path / "empty1.txt"
        file2 = tmp_path / "empty2.txt"
        file1.write_text("")
        file2.write_text("")
        
        hash1 = calculate_file_hash(str(file1))
        hash2 = calculate_file_hash(str(file2))
        
        assert hash1 == hash2


class TestFindDuplicateFiles:
    def test_no_duplicates(self, tmp_path):
        (tmp_path / "file1.txt").write_text("content1")
        (tmp_path / "file2.txt").write_text("content2")
        
        duplicates = find_duplicate_files(str(tmp_path))
        
        assert len(duplicates) == 2
    
    def test_with_duplicates(self, tmp_path):
        (tmp_path / "file1.txt").write_text("same content")
        (tmp_path / "file2.txt").write_text("same content")
        
        duplicates = find_duplicate_files(str(tmp_path))
        
        assert len(duplicates) == 1
        for hash_val, files in duplicates.items():
            assert len(files) == 2
    
    def test_nested_directories(self, tmp_path):
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (tmp_path / "file1.txt").write_text("content1")
        (subdir / "file2.txt").write_text("content1")
        
        duplicates = find_duplicate_files(str(tmp_path))
        
        assert len(duplicates) == 1


class TestDryRun:
    def test_dry_run_does_not_delete_files(self, tmp_path, capsys):
        file1 = tmp_path / "original.txt"
        file2 = tmp_path / "duplicate.txt"
        file1.write_text("same content")
        file2.write_text("same content")
        
        duplicates = {"abc123": [str(file1), str(file2)]}
        remove_duplicate_files(duplicates, confirmed=False, dry_run=True)
        
        assert file1.exists()
        assert file2.exists()
    
    def test_dry_run_shows_files_to_delete(self, tmp_path, capsys):
        file1 = tmp_path / "original.txt"
        file2 = tmp_path / "duplicate.txt"
        file1.write_text("same content")
        file2.write_text("same content")
        
        duplicates = {"abc123": [str(file1), str(file2)]}
        remove_duplicate_files(duplicates, confirmed=False, dry_run=True)
        
        captured = capsys.readouterr()
        assert "[DRY RUN]" in captured.out
        assert str(file2) in captured.out
    
    def test_dry_run_shows_summary(self, tmp_path, capsys):
        file1 = tmp_path / "original.txt"
        file2 = tmp_path / "duplicate.txt"
        file1.write_text("same content")
        file2.write_text("same content")
        
        duplicates = {"abc123": [str(file1), str(file2)]}
        remove_duplicate_files(duplicates, confirmed=False, dry_run=True)
        
        captured = capsys.readouterr()
        assert "would be deleted" in captured.out
    
    def test_dry_run_no_duplicates(self, tmp_path, capsys):
        duplicates = {}
        remove_duplicate_files(duplicates, confirmed=False, dry_run=True)
        
        captured = capsys.readouterr()
        assert "No duplicate files found" in captured.out

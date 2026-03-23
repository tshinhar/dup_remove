import os
import pytest
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from file_org import EXT_DICT, org_by_extension, org_files


class TestEXT_DICT:
    def test_no_duplicate_keys(self):
        keys = list(EXT_DICT.keys())
        assert len(keys) == len(set(keys)), "EXT_DICT has duplicate keys"
    
    def test_bat_in_scripts_not_images(self):
        assert EXT_DICT.get('.bat') == 'scripts'
    
    def test_common_extensions_mapped(self):
        common = ['.jpg', '.png', '.mp3', '.mp4', '.py', '.js']
        for ext in common:
            assert ext in EXT_DICT


class TestOrgByExtension:
    def test_creates_directory(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "test.txt").write_text("content")
        
        org_by_extension(["test.txt"], exclude_list=None, smart=False, dir_path=str(tmp_path))
        
        assert (tmp_path / "txt").exists()
    
    def test_smart_organize_uses_dict(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "test.jpg").write_text("content")
        
        org_by_extension(["test.jpg"], exclude_list=None, smart=True, dir_path=str(tmp_path))
        
        assert (tmp_path / "images").exists()
    
    def test_exclude_list(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "keep.txt").write_text("keep")
        (tmp_path / "skip.txt").write_text("skip")
        
        org_by_extension(["keep.txt", "skip.txt"], exclude_list=["skip.txt"], smart=False, dir_path=str(tmp_path))
        
        assert (tmp_path / "txt").exists()
        assert (tmp_path / "txt" / "keep.txt").exists()
        assert (tmp_path / "skip.txt").exists()
    
    def test_skips_directories(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file.txt").write_text("content")
        
        org_by_extension(["subdir"], exclude_list=None, smart=False, dir_path=str(tmp_path))
        
        assert subdir.exists()


class TestOrgFiles:
    def test_single_thread(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "test.txt").write_text("content")
        
        org_files(str(tmp_path), exclude_list=None, smart=False, threads=1)
        
        assert (tmp_path / "txt").exists()
    
    def test_handles_empty_directory(self, tmp_path):
        result = org_files(str(tmp_path), exclude_list=None, smart=False, threads=1)
        
        assert result is True
    
    def test_multithread_execution(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        for i in range(10):
            (tmp_path / f"test{i}.txt").write_text(f"content{i}")
        
        org_files(str(tmp_path), exclude_list=None, smart=False, threads=4)
        
        assert (tmp_path / "txt").exists()


class TestDryRun:
    def test_dry_run_does_not_move_files(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "test.txt").write_text("content")
        
        org_by_extension(["test.txt"], exclude_list=None, smart=False, dir_path=str(tmp_path), dry_run=True)
        
        assert (tmp_path / "test.txt").exists()
        assert not (tmp_path / "txt").exists()
    
    def test_dry_run_shows_preview(self, tmp_path, monkeypatch, capsys):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "test.txt").write_text("content")
        
        org_by_extension(["test.txt"], exclude_list=None, smart=False, dir_path=str(tmp_path), dry_run=True)
        
        captured = capsys.readouterr()
        assert "[DRY RUN]" in captured.out
        assert "test.txt" in captured.out
    
    def test_dry_run_smart_organize(self, tmp_path, monkeypatch, capsys):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "test.jpg").write_text("content")
        
        org_by_extension(["test.jpg"], exclude_list=None, smart=True, dir_path=str(tmp_path), dry_run=True)
        
        captured = capsys.readouterr()
        assert "[DRY RUN]" in captured.out
        assert "images" in captured.out
    
    def test_dry_run_shows_dirs_to_create(self, tmp_path, monkeypatch, capsys):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "test.txt").write_text("content")
        
        org_by_extension(["test.txt"], exclude_list=None, smart=False, dir_path=str(tmp_path), dry_run=True)
        
        captured = capsys.readouterr()
        assert "Would create directories" in captured.out
    
    def test_dry_run_excludes_git(self, tmp_path, monkeypatch, capsys):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "test.txt").write_text("content")
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        (git_dir / "config").write_text("git config")
        
        org_by_extension(["test.txt", ".git"], exclude_list=None, smart=False, dir_path=str(tmp_path), dry_run=True)
        
        captured = capsys.readouterr()
        assert ".git" not in captured.out or "Would move" not in captured.out.split(".git")[0] if ".git" in captured.out else True

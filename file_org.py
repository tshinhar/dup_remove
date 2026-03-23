# -*- coding: utf8 -*
import os
import shutil
import threading

EXT_DICT = {
        '.doc': 'documents',
        '.ppt': 'documents',
        '.pptx': 'documents',
        '.pdf': 'documents',
        '.xls': 'documents',
        '.xlsx': 'documents',
        '.jpeg': 'images',
        '.jpg': 'images',
        '.gif': 'images',
        '.png': 'images',
        '.svg': 'images',
        '.bmp': 'images',
        '.webp': 'images',
        '.mp3': 'music',
        '.ogg': 'music',
        '.wav': 'music',
        '.wma': 'music',
        '.flac': 'music',
        '.m4a': 'music',
        '.bat': 'scripts',
        '.sh': 'scripts',
        '.c': 'code',
        '.h': 'code',
        '.cpp': 'code',
        '.cc': 'code',
        '.js': 'code',
        '.ts': 'code',
        '.html': 'code',
        '.css': 'code',
        '.scss': 'code',
        '.pyc': 'code',
        '.py': 'code',
        '.cs': 'code',
        '.mp4': 'movies',
        '.mkv': 'movies',
        '.avi': 'movies',
        '.mov': 'movies',
        '.zip': 'archives',
        '.tar': 'archives',
        '.gz': 'archives',
        '.rar': 'archives',
        '.7z': 'archives',
        }

DEFAULT_EXCLUDE = ['.git', '__pycache__', 'node_modules', '.DS_Store']


def org_files(dir_path, exclude_list=None, smart=False, threads=1, dry_run=False):
        original_dir = os.getcwd()
        try:
                os.chdir(dir_path)
                files_list = os.listdir(dir_path)
        finally:
                os.chdir(original_dir)
        
        effective_exclude = list(DEFAULT_EXCLUDE)
        if exclude_list:
                effective_exclude.extend(exclude_list)
        
        if threads < 2:
                return org_by_extension(files_list, effective_exclude, smart, dir_path, dry_run)
        if not files_list:
                return None
        
        k, m = divmod(len(files_list), threads)
        sublists = (files_list[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(threads))
        threads_list = []
        for sublist in sublists:
                t = threading.Thread(target=org_by_extension, args=(sublist, effective_exclude, smart, dir_path, dry_run))
                t.start()
                threads_list.append(t)
        
        for t in threads_list:
                t.join()


def org_by_extension(file_paths, exclude_list=None, smart=False, dir_path=".", dry_run=False):
        """Organize the files based on their extension"""
        original_dir = os.getcwd()
        files_to_move = []
        dirs_to_create = set()
        
        try:
                os.chdir(dir_path)
                for file in file_paths:
                        if exclude_list and file in exclude_list:
                                continue
                        if not os.path.isfile(file):
                                continue
                        _, file_ext = os.path.splitext(file)
                        if not file_ext:
                                continue
                        dir_name = file_ext[1:]
                        if file_ext.lower() in EXT_DICT and smart:
                                dir_name = EXT_DICT[file_ext.lower()]
                        files_to_move.append((file, dir_name))
                        if not os.path.exists(dir_name):
                                dirs_to_create.add(dir_name)
        
                if dry_run:
                        if dirs_to_create:
                                print(f"[DRY RUN] Would create directories: {', '.join(sorted(dirs_to_create))}")
                        print(f"[DRY RUN] Would move {len(files_to_move)} file(s):")
                        for file, dir_name in files_to_move:
                                try:
                                        size = os.path.getsize(file)
                                        print(f"  {file} -> {dir_name}/ ({size} bytes)")
                                except OSError:
                                        print(f"  {file} -> {dir_name}/")
                        return True
                
                for file, dir_name in files_to_move:
                        if dir_name not in dirs_to_create:
                                continue
                        try:
                                os.makedirs(dir_name)
                        except FileExistsError:
                                pass
                        dirs_to_create.discard(dir_name)
                
                for file, dir_name in files_to_move:
                        print(f"moving {file} to {dir_name}")
                        shutil.move(file, dir_name+"/")
        finally:
                os.chdir(original_dir)
        return True

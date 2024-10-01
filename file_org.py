# -*- coding: utf8 -*
import os,shutil
import threading

EXT_DICT = {
        '.doc': 'documents',
        '.doc': 'documents',
        '.ppt': 'documents',
        '.pptx': 'documents',
        '.jpeg': 'images',
        '.jpg': 'images',
        '.gif': 'images',
        '.png': 'images',
        '.svg': 'images',
        '.bat': 'images',
        '.bmp': 'images',
        '.mp3': 'music',
        '.ogg': 'music',
        '.wav': 'music',
        '.wma': 'music',
        '.flac': 'music',
        '.m4a': 'music',
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
        '.mp4': 'movies'
        }

def org_files(dir_path, exclude_list=None, smart=False, threads=1):
        files_list = os.listdir(dir_path)
        if threads < 2:
                return org_by_extension(files_list, exclude_list, smart)
        if not files_list:
                return None
        k, m = divmod(len(files_list), threads)
        sublists = (files_list[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(threads))
        for sublist in sublists:
                threading.Thread(target=org_by_extension(sublist, exclude_list, smart)).start()


def org_by_extension(file_paths, exclude_list=None, smart=False):
        """orginize the files based on their extension"""
        for file in file_paths:
                if file in exclude_list:
                        continue
                _, file_ext = os.path.splitext(file)
                dir_name = file_ext.remove(".")
                if file_ext in EXT_DICT and smart is True:
                            dir_name = EXT_DICT[file_ext]
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
                print(f"moving {file} to {dir_name}")
                shutil.move(file, dir_name+"/")
                return True

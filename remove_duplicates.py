import os
import hashlib

def calculate_file_hash(file_path):
    """Calculates the hash value of a file's content."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicate_files(root_folder):
    """Traverses through the root folder and identifies duplicate files."""
    print(f"Looking for duplicate files under {root_folder}...")
    duplicates = {}
    for folder_path, _, file_names in os.walk(root_folder):
        for file_name in file_names:
            file_path = os.path.join(folder_path, file_name)
            file_hash = calculate_file_hash(file_path)
            if file_hash in duplicates:
                duplicates[file_hash].append(file_path)
            else:
                duplicates[file_hash] = [file_path]
    return duplicates

def remove_duplicate_files(duplicates, confirmed=False, dry_run=False):
    """Removes duplicate files from the file system."""
    total_files_to_delete = 0
    total_size_to_free = 0
    
    for file_paths in duplicates.values():
        if len(file_paths) > 1:
            original = file_paths[0]
            to_delete = file_paths[1:]
            total_files_to_delete += len(to_delete)
            
            for file_path in to_delete:
                try:
                    total_size_to_free += os.path.getsize(file_path)
                except OSError:
                    pass
            
            if dry_run:
                print(f"[DRY RUN] Would delete {len(to_delete)} duplicate(s) of:")
                print(f"  Original: {original}")
                for fp in to_delete:
                    try:
                        size = os.path.getsize(fp)
                        print(f"  Would delete: {fp} ({size} bytes)")
                    except OSError:
                        print(f"  Would delete: {fp}")
                print()
            else:
                print(f"Duplicate files found:\n{file_paths}\n")
                for file_path in to_delete:
                    delete_flag = confirmed
                    if not confirmed:
                        confirmation = input("Delete?")
                        if confirmation.lower() in ["yes", "y", "ok"]:
                            delete_flag = True
                    if delete_flag:
                        os.remove(file_path)
                        print(f"{file_path} has been deleted.\n")
                    else:
                        print("Duplicate file was not deleted")
    
    if dry_run and total_files_to_delete > 0:
        print(f"\n[DRY RUN] Summary: {total_files_to_delete} file(s) would be deleted, freeing ~{total_size_to_free} bytes")
    elif dry_run:
        print("\n[DRY RUN] No duplicate files found.")

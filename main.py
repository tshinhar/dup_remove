import argparse
from remove_duplicates import find_duplicate_files, remove_duplicate_files
from file_org import org_files

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="fily: file managment utility")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument(
        "-y", "--yes", action="store_true", help="pre-confirm files removal"
    )
    parser.add_argument(
        "-r", "--remove", action="store_true", help="remove duplicate files in target directory"
    )
    parser.add_argument(
        "-o", "--organize", action="store_true", help="organize files in target directory"
    )
    parser.add_argument(
        "-s", "--smart", action="store_true", help="enable smart organization"
    )
    parser.add_argument(
        "-n", "--threads", type=int, default=1, help="set number of threads for organization"
    )
    parser.add_argument(
        "-d", "--dry-run", action="store_true", help="preview actions without executing them"
    )
    parser.add_argument("root_path", nargs="+", help="Path to the root directory")
    args = parser.parse_args()

    for path in args.root_path:
        arg_lst = args._get_args()
        if args.remove or not args._get_args():
            duplicates = find_duplicate_files(path)
            remove_duplicate_files(duplicates, args.yes, args.dry_run)
        if args.organize:
            org_files(path, smart=args.smart, threads=args.threads, dry_run=args.dry_run)
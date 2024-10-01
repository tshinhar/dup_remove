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
        "-o", "--orgenize", action="store_true", help="orgenize files in target directory"
    )
    parser.add_argument(
        "-s", "--smart", action="store_true", help="enable smart orginazation"
    )
    parser.add_argument(
        "-n", "--threads", action="store_true", help="enable smart orginazation"
    )
    parser.add_argument("root_path", nargs="+", help="Path to the root directory")
    # Parse the command-line arguments
    args = parser.parse_args()

    for path in args.root_path:
        if args.remove:
            duplicates = find_duplicate_files(path)
            remove_duplicate_files(duplicates, args.yes)
        if args.orgenize:
            threads = 1
            if args.threads:
                threads = 2
            org_files(path, smart=args.smart, threads=threads)
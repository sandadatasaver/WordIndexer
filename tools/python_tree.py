import os
import argparse

def generate_tree(directory, ignore_folders, prefix="", is_root=True):
    try:
        entries = sorted(os.listdir(directory))
    except PermissionError:
        return []
    
    dirs = [e for e in entries if os.path.isdir(os.path.join(directory, e))]
    files = [e for e in entries if os.path.isfile(os.path.join(directory, e))]
    
    all_entries = [(d, True) for d in dirs] + [(f, False) for f in files]
    lines = []

    for i, (entry, is_dir) in enumerate(all_entries):
        is_last = (i == len(all_entries) - 1)
        connector = "└── " if is_last else "├── "
        display_name = entry + "/" if is_dir else entry

        lines.append(f"{prefix}{connector}{display_name}")

        # Only recurse if it's a directory AND not in ignore list
        if is_dir and entry not in ignore_folders:
            extension = "    " if is_last else "│   "
            lines.extend(generate_tree(
                os.path.join(directory, entry),
                ignore_folders,
                prefix + extension,
                is_root=False
            ))

    return lines


def main():
    parser = argparse.ArgumentParser(description="Generate directory tree")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to scan")
    parser.add_argument("-o", "--output", default="tree.txt", help="Output file")
    parser.add_argument("-i", "--ignore", nargs="*", default=["venv", "__pycache__", ".git"],
                        help="Folders to show but not expand")
    
    args = parser.parse_args()
    
    root = os.path.abspath(args.directory)
    tree_lines = [os.path.basename(root) + "/"]
    tree_lines.extend(generate_tree(root, args.ignore))
    output = "\n".join(tree_lines)
    
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(output)
    
    print(output)
    print(f"\nSaved to: {args.output}")


if __name__ == "__main__":
    main()
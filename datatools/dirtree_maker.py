import os

# make tree view
def print_tree():
    """Prompt for a directory path and print its tree structure."""
    start_dir = input("Enter directory path (default: current directory): ").strip() or "."
    if not os.path.exists(start_dir):
        print(f"Error: The path '{start_dir}' does not exist.")
        return
    def _print_tree(path, prefix=""):
        try:
            entries = sorted(os.listdir(path))
        except PermissionError:
            print(prefix + "└── [Permission Denied]")
            return
        for i, name in enumerate(entries):
            full_path = os.path.join(path, name)
            connector = "└── " if i == len(entries) - 1 else "├── "
            print(prefix + connector + name)
            if os.path.isdir(full_path):
                extension = "    " if i == len(entries) - 1 else "│   "
                _print_tree(full_path, prefix + extension)
    print(f"\nDirectory tree for: {os.path.abspath(start_dir)}\n")
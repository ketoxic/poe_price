import os

ALLOWED_EXT = {".py", ".json", ".txt"}
EXCLUDE_DIR = {
    ".idea", ".venv", "__pycache__", ".git",
    ".pytest_cache", "node_modules"
}

def print_tree(path=".", prefix=""):
    items = []
    for name in os.listdir(path):
        full = os.path.join(path, name)

        if os.path.isdir(full):
            if name in EXCLUDE_DIR:
                continue
            items.append(name)

        elif os.path.isfile(full):
            if os.path.splitext(name)[1] in ALLOWED_EXT:
                items.append(name)

    for i, name in enumerate(items):
        full = os.path.join(path, name)
        last = i == len(items) - 1
        print(prefix + ("└── " if last else "├── ") + name)

        if os.path.isdir(full):
            print_tree(full, prefix + ("    " if last else "│   "))

print_tree()

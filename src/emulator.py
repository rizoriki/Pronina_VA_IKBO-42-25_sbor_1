"""OS shell emulator. Variant 24, Stages 1-3."""
import argparse
import base64
import json
import os
import re
import sys


class VFSNode:
    """Represents a node in the Virtual File System."""

    def __init__(self, name, is_dir=False, content=None):
        self.name = name
        self.is_dir = is_dir
        self.content = content
        self.children = {} if is_dir else None


def build_vfs_node(data):
    """Recursively build VFSNode from dictionary."""
    if not isinstance(data, dict):
        return None
    name = data.get("name", "root")
    is_dir = data.get("is_dir", False)
    node = VFSNode(name, is_dir=is_dir)
    if is_dir:
        for child in data.get("children", []):
            child_node = build_vfs_node(child)
            if child_node:
                node.children[child_node.name] = child_node
    else:
        if data.get("is_binary", False):
            node.content = base64.b64decode(
                data.get("content", "")
            )
        else:
            node.content = data.get("content", "")
    return node


def load_vfs(filepath):
    """Load VFS tree from JSON file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"VFS file not found: {filepath}"
        )
    try:
        with open(
            filepath, "r", encoding="utf-8"
        ) as file:
            data = json.load(file)
        return build_vfs_node(data)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON format in VFS: {filepath}"
        ) from exc


class Emulator:
    """Main emulator class."""

    def __init__(self, vfs_path=None):
        self.vfs_name = "default_vfs"
        self.current_dir = "/"
        self.vfs_root = VFSNode("root", is_dir=True)
        if vfs_path:
            try:
                self.vfs_root = load_vfs(vfs_path)
                self.vfs_name = os.path.basename(vfs_path)
                print(
                    f"[DEBUG] VFS loaded from {vfs_path}"
                )
            except (
                FileNotFoundError, ValueError
            ) as err:
                print(f"[ERROR] {err}")
                sys.exit(1)

    def expand_vars(self, text):
        """Expand $VAR and ${VAR} in text."""
        def repl(match):
            name = match.group(1) or match.group(2)
            return os.environ.get(name, match.group(0))
        pattern = r'\$\{([^}]+)\}|\$([A-Za-z_]\w*)'
        return re.sub(pattern, repl, text)

    def execute(self, line):
        """Execute a single command line."""
        line = self.expand_vars(line).strip()
        if not line or line.startswith('#'):
            return
        parts = line.split()
        cmd = parts[0]
        args = parts[1:]
        if cmd == 'exit':
            print("Exiting emulator.")
            sys.exit(0)
        if cmd in ('ls', 'cd'):
            print(f"Executing stub: {cmd} with args {args}")
        else:
            print(f"[ERROR] Unknown command: {cmd}")

    def run_script(self, path):
        """Run commands from a script file."""
        if not os.path.exists(path):
            print(f"[ERROR] Script not found: {path}")
            return
        with open(path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                print(f"[{self.vfs_name}]$ {line}")
                try:
                    self.execute(line)
                except Exception as err:
                    print(
                        f"[ERROR] Line {line_num}: {err}"
                    )

    def run_repl(self):
        """Interactive REPL loop."""
        print(f"Emulator started. VFS: {self.vfs_name}")
        while True:
            try:
                prompt = f"[{self.vfs_name} {self.current_dir}]$ "
                line = input(prompt)
                self.execute(line)
            except (EOFError, KeyboardInterrupt):
                print("\nExiting emulator.")
                break


def main():
    """Entry point with argparse."""
    parser = argparse.ArgumentParser(
        description="OS Shell Emulator"
    )
    parser.add_argument(
        '--vfs', type=str,
        help="Path to VFS JSON file"
    )
    parser.add_argument(
        '--script', type=str,
        help="Path to startup script"
    )
    args = parser.parse_args()

    print(f"[DEBUG] vfs={args.vfs}, script={args.script}")
    emulator = Emulator(vfs_path=args.vfs)

    if args.script:
        emulator.run_script(args.script)
    else:
        emulator.run_repl()


if __name__ == "__main__":
    main()

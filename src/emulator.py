"""OS shell emulator. Variant 24, Stages 1-3."""
import argparse
import os
import re
import sys


class Emulator:
    """Main emulator class."""

    def __init__(self):
        self.vfs_name = "default_vfs"
        self.current_dir = "/"

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
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                print(f"[{self.vfs_name}]$ {line}")
                self.execute(line)

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

    emulator = Emulator()
    if args.vfs:
        emulator.vfs_name = os.path.basename(args.vfs)

    if args.script:
        emulator.run_script(args.script)
    else:
        emulator.run_repl()


if __name__ == "__main__":
    main()

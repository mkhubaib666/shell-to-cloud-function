from src.handlers.base_handler import CommandHandler


class EchoHandler(CommandHandler):
    def to_code(self):
        message = " ".join(self.args)
        resolved_message = self._resolve_vars(message).replace("'", "\\'")
        return f"print(f'{resolved_message}')"

    def get_imports(self):
        # os is needed for resolving env vars
        return ["import os"]


class SubprocessHandler(CommandHandler):
    """Generic handler for commands that will be run in a subprocess."""

    def get_imports(self):
        return ["import subprocess"]

    def to_code(self):
        cmd_parts = [f'"{p}"' for p in self.parts]
        return f"subprocess.run([{', '.join(cmd_parts)}], check=True)"


def register():
    """Registers the handlers in this file."""
    return {
        "echo": EchoHandler,
        "ls": SubprocessHandler,
        "cp": SubprocessHandler,
        "mv": SubprocessHandler,
        "rm": SubprocessHandler,
        "mkdir": SubprocessHandler,
    }

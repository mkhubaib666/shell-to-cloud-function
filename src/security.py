import bashlex

DANGEROUS_COMMANDS = {
    "rm": {
        "flags": ["-rf", "-fr"],
        "level": "CRITICAL",
        "warning": "Potentially destructive recursive force delete.",
    },
    "dd": {
        "flags": [],
        "level": "CRITICAL",
        "warning": "Direct disk write command, can cause irreversible data loss.",
    },
    "mkfs": {
        "flags": [],
        "level": "CRITICAL",
        "warning": "Command to create a new file system, erases data.",
    },
    "> /dev/sd": {
        "flags": [],
        "level": "CRITICAL",
        "warning": "Direct redirection to a disk device, can wipe partitions.",
    },
}


class SecurityAnalyzer:
    def __init__(self, config):
        self.fail_level = config.get("fail_on_level", "CRITICAL")
        self.interactive = config.get("interactive_prompt", True)

    def scan(self, script_content):
        """Scans script for dangerous commands and returns True if safe to proceed."""
        warnings = []
        try:
            nodes = bashlex.parse(script_content)
            for node in nodes:
                if node.kind != "command":
                    continue
                cmd_name = node.parts[0].word
                if cmd_name in DANGEROUS_COMMANDS:
                    rule = DANGEROUS_COMMANDS[cmd_name]
                    parts_str = " ".join(p.word for p in node.parts)
                    # Check if any of the rule's flags are present
                    if not rule["flags"] or any(f in parts_str for f in rule["flags"]):
                        warnings.append(
                            f"[{rule['level']}] Found command '{cmd_name}': {rule['warning']}"
                        )

        except Exception:
            pass  # Ignore parsing errors during security scan

        if not warnings:
            print("Security scan passed.")
            return True

        print("Security scan found potential issues:")
        for warning in warnings:
            print(f"  - {warning}")

        if self.interactive:
            proceed = input("Do you wish to continue? (y/N): ")
            return proceed.lower() == "y"

        return False

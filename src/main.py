import argparse
import os
import yaml
from orchestrator import Orchestrator


def load_config():
    """Loads config.yaml if it exists."""
    config_path = "config.yaml"
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    return {}


def main():
    """CLI entry point."""
    config = load_config()
    defaults = config.get("defaults", {})

    parser = argparse.ArgumentParser(
        description="Convert shell scripts to serverless projects."
    )
    parser.add_argument(
        "shell_script", help="Path to the shell script to convert."
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Name of the output directory for the generated project.",
    )
    parser.add_argument(
        "--language",
        choices=["python", "nodejs"],
        default=defaults.get("language", "python"),
        help="Target language for the cloud function.",
    )
    parser.add_argument(
        "--provider",
        choices=["aws", "azure", "gcp"],
        default=defaults.get("provider", "aws"),
        help="Target cloud provider.",
    )

    args = parser.parse_args()

    if not os.path.exists(args.shell_script):
        print(f"Error: Shell script not found at {args.shell_script}")
        return

    with open(args.shell_script, "r") as f:
        script_content = f.read()

    orchestrator = Orchestrator(
        script_content, args.language, args.provider, args.output_dir, config
    )
    orchestrator.process()


if __name__ == "__main__":
    main()
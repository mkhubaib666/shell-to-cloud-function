import bashlex
import os
import importlib.util
from generator import ProjectGenerator
from security import SecurityAnalyzer
from context import ConversionContext


class Orchestrator:
    """Coordinates the parsing, analysis, conversion, and generation."""

    def __init__(self, script_content, language, provider, output_dir, config):
        self.script_content = script_content
        self.language = language
        self.provider = provider
        self.output_dir = output_dir
        self.config = config
        self.security_analyzer = SecurityAnalyzer(config.get("security", {}))
        self.handler_map = {}

    def _load_plugins(self):
        """Loads handlers from core and custom plugin directories."""
        print("Loading conversion plugins")
        plugin_dirs = [os.path.join("src", "plugins", "core")]
        custom_plugins_dir = self.config.get("defaults", {}).get(
            "plugins_dir"
        )
        if custom_plugins_dir and os.path.isdir(custom_plugins_dir):
            plugin_dirs.append(custom_plugins_dir)

        for directory in plugin_dirs:
            for filename in os.listdir(directory):
                if filename.endswith(f"_{self.language}.py"):
                    filepath = os.path.join(directory, filename)
                    module_name = f"plugins.{filename[:-3]}"
                    spec = importlib.util.spec_from_file_location(
                        module_name, filepath
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    if hasattr(module, "register"):
                        self.handler_map.update(module.register())

    def process(self):
        """Executes the end-to-end conversion process."""
        print("Running security scan")
        if not self.security_analyzer.scan(self.script_content):
            return 

        self._load_plugins()

        print("Converting script to target language")
        try:
            parsed_nodes = bashlex.parse(self.script_content)
        except Exception as e:
            print(f"Error parsing shell script: {e}")
            return

        context = ConversionContext()
        for node in parsed_nodes:
            if node.kind != "command":
                context.add_code_line(
                    f"# Skipping non-command node: {node}", is_comment=True
                )
                continue

            command_name = node.parts[0].word
            # Find a specific handler (e.g., 'aws s3 cp') or a generic one ('aws')
            handler_key = self._find_handler_key(node)
            handler_class = self.handler_map.get(handler_key)

            if handler_class:
                handler = handler_class(node, context)
                handler.handle()
            else:
                context.add_code_line(
                    f"# Unsupported command: {command_name}", is_comment=True
                )

        print(" Generating project files")
        generator = ProjectGenerator(
            self.output_dir, self.language, self.provider
        )
        generator.generate(context.get_imports(), context.get_code())

        print(f"\nSuccessfully generated project in: output/{self.output_dir}")

    def _find_handler_key(self, node):
        """Finds the most specific handler key for a command."""
        parts = [p.word for p in node.parts]
        # Check for multi-word keys like "aws s3 cp"
        for i in range(len(parts), 0, -1):
            key = " ".join(parts[:i])
            if key in self.handler_map:
                return key
        return None
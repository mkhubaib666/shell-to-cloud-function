import re


class CommandHandler:
    """Abstract base class for all command handlers."""

    def __init__(self, node, context):
        self.node = node
        self.context = context
        self.parts = [p.word for p in node.parts]
        self.command = self.parts[0]
        self.args = self.parts[1:]
        self.redirect_out = None

        if node.redirects:
            for r in node.redirects:
                if r.type == ">":
                    self.redirect_out = r.output.word

    def handle(self):
        """
        Main method to be called. It gets imports and code,
        and adds them to the context.
        """
        for imp in self.get_imports():
            self.context.add_import(imp)
        self.context.add_code_line(self.to_code())

    def to_code(self):
        """Converts the command to a line of target language code."""
        raise NotImplementedError

    def get_imports(self):
        """Returns a list of required imports for this command."""
        return []

    def _resolve_vars(self, text, lang="python"):
        """Resolves shell variables like $VAR or ${VAR}."""
        if lang == "python":
            return re.sub(r"\$(\w+)|\${(\w+)}", r"os.environ.get('\1\2', '')", text)
        # Add nodejs logic here if needed
        return text

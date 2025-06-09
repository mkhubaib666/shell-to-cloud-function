class ConversionContext:
    """Holds the state of the conversion process."""

    def __init__(self):
        self.imports = set()
        self.code_lines = []
        self.variables = {}

    def add_import(self, import_statement):
        self.imports.add(import_statement)

    def add_code_line(self, line, is_comment=False):
        # Simple way to handle comments vs code
        prefix = "# " if is_comment else ""
        self.code_lines.append(f"{prefix}{line}")

    def get_imports(self):
        return sorted(list(self.imports))

    def get_code(self):
        return "\n".join(self.code_lines)

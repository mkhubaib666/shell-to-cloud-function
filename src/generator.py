import os
import shutil


class ProjectGenerator:
    """
    Generates the complete project directory structure and files,
    including IaC templates and local testing configs.
    """

    def __init__(self, output_dir_name, language, provider):
        self.output_dir_name = output_dir_name
        self.output_path = os.path.join("output", output_dir_name)
        self.language = language
        self.provider = provider
        self.template_path = os.path.join("src", "templates")

    def generate(self, imports, code_body):
        """
        Creates the project directory and all necessary files.
        """
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path)
        os.makedirs(os.path.join(self.output_path, "tests"))

        self._generate_function_file(imports, code_body)
        self._generate_dependencies_file()
        self._generate_gitignore()
        self._generate_provider_specific_files()
        self._generate_test_files()

    def _generate_function_file(self, imports, code_body):
        lang_path = os.path.join(self.template_path, self.language)
        template_file = (
            f"{self.provider}_function.{'py' if self.language == 'python' else 'js'}"
        )

        with open(os.path.join(lang_path, template_file), "r") as f:
            template = f.read()

        indent = "    " if self.language == "python" else "  "
        indented_body = "\n".join([f"{indent}{line}" for line in code_body.split("\n")])

        full_code = template.replace("#IMPORTS#", "\n".join(imports)).replace(
            "#CODE_BODY#", indented_body
        )

        output_filename = "main.py" if self.language == "python" else "index.js"
        with open(os.path.join(self.output_path, output_filename), "w") as f:
            f.write(full_code)

    def _generate_dependencies_file(self):
        if self.language == "python":
            deps_path = os.path.join(self.template_path, "python", "requirements.txt")
            shutil.copy(deps_path, self.output_path)
        elif self.language == "nodejs":
            deps_path = os.path.join(self.template_path, "nodejs", "package.json")
            shutil.copy(deps_path, self.output_path)

    def _generate_gitignore(self):
        gitignore_path = os.path.join(self.template_path, "common", ".gitignore")
        shutil.copy(gitignore_path, self.output_path)

    def _generate_provider_specific_files(self):
        """Generates files like template.yaml, local.settings.json, etc."""
        provider_template_path = os.path.join(
            self.template_path, self.language, self.provider
        )
        if not os.path.exists(provider_template_path):
            return

        for filename in os.listdir(provider_template_path):
            src = os.path.join(provider_template_path, filename)
            dest = os.path.join(self.output_path, filename)
            shutil.copy(src, dest)

    def _generate_test_files(self):
        """Generates a basic test file."""
        test_template_path = os.path.join(
            self.template_path, self.language, "test_template.txt"
        )
        if os.path.exists(test_template_path):
            dest_filename = (
                "test_handler.py"
                if self.language == "python"
                else "test_handler.test.js"
            )
            dest_path = os.path.join(self.output_path, "tests", dest_filename)
            shutil.copy(test_template_path, dest_path)

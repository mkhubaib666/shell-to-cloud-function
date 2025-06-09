# Shell to Cloud Function Converter (v4.0)

An intelligent, secure, and extensible framework for migrating shell scripts to production-ready serverless projects on AWS, Azure, and GCP.

**Repository:** `https://github.com/mkhubaib666/shell-to-cloud-function-converter`

---

## What Makes This Version Different?

This is not just a code translator; it's a migration accelerator built on professional software principles.

-   ✅ **Semantic Conversion:** Understands commands like `aws s3 cp` and converts them to efficient, native SDK calls (`boto3`) instead of slow `subprocess` calls.
-   ✅ **Plugin Architecture:** Need to support a custom command or a new tool? Just drop a handler file into a directory. No need to modify the core tool.
-   ✅ **Security-First:** An integrated security scanner warns you about dangerous commands (`rm -rf`, `dd`) *before* conversion, preventing costly mistakes.
-   ✅ **Configuration Driven:** Manage complex projects and team settings using a central `config.yaml` file.

---

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mkhubaib666/shell-to-cloud-function-converter.git
    cd shell-to-cloud-function-converter
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure (Optional):**
    Rename `config.yaml.example` to `config.yaml` and customize your default settings.

## Usage

The core command remains simple. CLI flags will always override settings in `config.yaml`.

```bash
python src/main.py <path_to_shell_script> --output-dir <project_name>
```

## Extending the Converter with Plugins

To add support for a new command, you don't need to edit the source.

1.  Create a directory for your custom plugins (e.g., `my_plugins`).
2.  In your `config.yaml`, set `plugins_dir: my_plugins`.
3.  Create a Python file in that directory (e.g., `my_tool_handler.py`).
4.  Inside, create a handler class inheriting from `CommandHandler` and a `register()` function.

## License

This project is licensed under the MIT License.
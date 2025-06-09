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
-   ✅ **Ready for CI/CD:** The tool itself is built with CI/CD, and the projects it generates are structured for automated testing and deployment.

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

### Example: Intelligent Conversion

Consider this script, `samples/s3_upload.sh`:
```sh
#!/bin/bash
# Create a report
echo "{\"status\": \"completed\", \"user\": \"$USER\"}" > /tmp/report.json

# Upload the report to S3 using the AWS CLI
aws s3 cp /tmp/report.json s3://my-app-reports-bucket/daily/report.json
```

**Run the converter:**
```bash
python src/main.py samples/s3_upload.sh --provider aws --output-dir my-s3-uploader
```

**Result:** Instead of a slow `subprocess` call, the generated Python code will contain:
```python
# ... boilerplate ...
import boto3
# ...
s3_client = boto3.client('s3')
s3_client.upload_file('/tmp/report.json', 'my-app-reports-bucket', 'daily/report.json')
# ...
```

## Development & Deployment Lifecycle

The workflow for testing and deploying the *generated* projects remains the same as in v3.0. Please refer to the detailed steps in the previous README versions for local emulation (SAM, Azure Functions Tools) and cloud deployment.

## Extending the Converter with Plugins

To add support for a new command, you don't need to edit the source.

1.  Create a directory for your custom plugins (e.g., `my_plugins`).
2.  In your `config.yaml`, set `plugins_dir: my_plugins`.
3.  Create a Python file in that directory (e.g., `my_tool_handler.py`).
4.  Inside, create a handler class inheriting from `CommandHandler` and a `register()` function.

**Example `my_plugins/my_tool_handler.py`:**
```python
from src.handlers.base_handler import CommandHandler

class MyToolHandler(CommandHandler):
    def to_code(self):
        return f"my_custom_library.run('{self.args[0]}')"
    def get_imports(self):
        return ["import my_custom_library"]

def register():
    return {"my-tool": MyToolHandler}
```
The converter will now automatically recognize and convert the `my-tool` command.

## License

This project is licensed under the MIT License.

from src.handlers.base_handler import CommandHandler


class AwsS3CpHandler(CommandHandler):
    """
    Intelligently handles `aws s3 cp` commands by converting them
    to boto3 SDK calls.
    """

    def get_imports(self):
        return ["import boto3"]

    def to_code(self):
        # Expects `aws s3 cp <source> <destination>`
        if len(self.parts) != 4:
            return "# Malformed 'aws s3 cp' command. Falling back to subprocess."
            # In a real scenario, you might fall back to SubprocessHandler
            # return f"subprocess.run({self.parts}, check=True)"

        source = self.parts[2]
        dest = self.parts[3]

        code = "s3_client = boto3.client('s3')"

        if source.startswith("s3://"):  # Download
            bucket, key = self._parse_s3_uri(source)
            return f"{code}\n" f"s3_client.download_file('{bucket}', '{key}', '{dest}')"
        elif dest.startswith("s3://"):  # Upload
            bucket, key = self._parse_s3_uri(dest)
            return f"{code}\n" f"s3_client.upload_file('{source}', '{bucket}', '{key}')"
        else:
            return "# 'aws s3 cp' requires one S3 URI. Falling back."

    def _parse_s3_uri(self, uri):
        path_parts = uri.replace("s3://", "").split("/", 1)
        bucket = path_parts[0]
        key = path_parts[1] if len(path_parts) > 1 else ""
        return bucket, key


def register():
    """Registers the AWS-specific handlers."""
    return {"aws s3 cp": AwsS3CpHandler}

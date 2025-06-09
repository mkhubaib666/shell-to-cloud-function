#!/bin/bash

# A script that uses a cloud-specific CLI command.
echo "Generating report for user: $USER"

# Create a dummy report file
echo "{\"status\": \"completed\", \"timestamp\": $(date +%s)}" > /tmp/report.json

# Upload the report to S3 using the AWS CLI
# The converter should be smart enough to handle this.
aws s3 cp /tmp/report.json s3://my-app-reports-bucket/daily/report.json

echo "Report uploaded."

# This is a dangerous command that the security scanner should flag.
rm -rf /tmp/report.json
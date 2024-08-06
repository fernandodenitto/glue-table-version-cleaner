# Glue Crawler Cleaner Lambda

## Overview

The Glue Crawler Cleaner Lambda automates the cleanup of outdated table versions in AWS Glue, preventing storage bloat and versioning issues. The function runs on a schedule, ensuring your Glue Data Catalog stays optimized and efficient.

## Problem

AWS Glue accumulates multiple versions of tables over time, leading to increased storage costs and potential version management issues. Manually cleaning up these versions is cumbersome and error-prone.

## Solution

This Lambda function addresses the problem by:
1. **Fetching Databases**: Retrieves all databases and tables from AWS Glue.
2. **Processing Tables**: Deletes older table versions while managing execution time.
3. **Batch Deletion**: Handles version deletions in batches to comply with API limits and track errors.

## How to Use

1. **Deploy**: Upload the function code to an S3 bucket and use the YAML configuration to deploy via AWS CloudFormation.
2. **Configure**: Set the desired schedule and update placeholders in the YAML file.
3. **Monitor**: Check CloudWatch logs for function execution and issues.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

[Your Name] - [Your Contact Information]

## Acknowledgements

- AWS Documentation
- boto3 Python SDK

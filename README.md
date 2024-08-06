# Glue Crawler Cleaner Lambda

## Overview

The Glue Crawler Cleaner Lambda function automates the cleanup of older table versions in AWS Glue, helping to manage storage efficiently and avoid versioning issues.

## Situation

AWS Glue accumulates multiple versions of tables over time, leading to increased storage costs and potential management issues. Manual cleanup is inefficient and prone to error.

## Task

Develop a solution to automatically remove outdated table versions in AWS Glue to:
1. Reduce storage costs.
2. Prevent version management issues.
3. Automate the cleanup process.

## Action

1. **Deploy Lambda Function**: Implemented an AWS Lambda function that runs on a schedule.
2. **Fetch Data**: The function retrieves all databases and tables from AWS Glue.
3. **Process and Clean**: It identifies and deletes older table versions, ensuring it does not exceed API rate limits.
4. **Batch Processing**: Handles deletions in batches and logs results, including errors.

## Result

The Lambda function effectively cleans up old table versions, reducing storage costs and preventing clutter in the Glue Data Catalog. It runs on a regular schedule, automating what was previously a manual and error-prone task.

## How to Use

### Method 1: Deploy Using YAML Configuration

1. **Upload Code**: Upload the Lambda function code (`glue_crawler_cleaner.py`) to an S3 bucket.
2. **Deploy via CloudFormation**: Use the provided YAML configuration (`lambda_function.yaml`) to deploy the Lambda function, IAM role, EventBridge rule, and permissions using AWS CloudFormation.
   - Note: The YAML file demonstrates the required permissions and configuration but is not strictly necessary for deployment. You can manually create these resources in the AWS Management Console if preferred.

### Method 2: Deploy Using AWS Management Console

1. **Create Lambda Function**:
   - Go to the AWS Lambda console.
   - Click "Create function" and choose "Author from scratch."
   - Enter a function name (e.g., `GlueCrawlerCleanerFunction`).
   - Choose Python 3.8 as the runtime.
   - Upload the Lambda function code (`glue_crawler_cleaner.py`) as a .zip file or specify the S3 bucket location.
   - Create or select an existing execution role with the necessary permissions (AWS Glue and CloudWatch Logs).

2. **Create EventBridge Rule**:
   - Go to the Amazon EventBridge console.
   - Click "Create rule."
   - Set the schedule using a cron expression or rate expression (e.g., `rate(1 day)`).
   - Add the Lambda function as the target.

3. **Grant Lambda Permission to EventBridge**:
   - Go to the AWS Lambda console.
   - Select the Lambda function you created.
   - Under the "Configuration" tab, choose "Permissions."
   - Add a resource-based policy to allow EventBridge to invoke the function.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

[Your Name] - [Your Contact Information]

## Acknowledgements

- AWS Documentation
- boto3 Python SDK

# AWS Glue Table Version Cleanup Lambda

## Description

This project provides a solution for efficiently managing AWS Glue table versions using an AWS Lambda function. Over time, AWS Glue can accumulate a large number of table versions, which may exceed service quotas and cause issues with data access and crawler operations. This Lambda function addresses this problem by periodically deleting older table versions in bulk, ensuring smooth operation and avoiding crawler failures.

## Problem

AWS Glue creates a new version of a table every time a transformation occurs. If the number of table versions exceeds certain thresholds, it can lead to crawler failures and issues accessing data through Athena or other DBMS/Data Warehouse solutions.

### Service Quotas

Here are some relevant service quotas for AWS Glue table versions:

| Service Quota                            | Scope               | Default Limit | Adjustable | Description                                               |
|------------------------------------------|---------------------|---------------|------------|-----------------------------------------------------------|
| Max concurrent job runs per account      | Each supported Region | 2,000         | Yes        | The maximum number of concurrent job runs in your account. |
| Max concurrent job runs per job          | Each supported Region | 4,000         | Yes        | The maximum number of concurrent job runs for a job.     |
| Max table versions per account           | Each supported Region | 1,000,000     | Yes        | The maximum number of table versions in your account.    |
| Max table versions per table             | Each supported Region | 100,000       | Yes        | The maximum number of table versions per table.         |
| Max tables per account                   | Each supported Region | 1,000,000     | Yes        | The maximum number of tables in your account.           |
| Max tables per database                  | Each supported Region | 200,000       | Yes        | The maximum number of tables per database.              |

For more details, refer to the [AWS Glue Service Quotas documentation](https://docs.aws.amazon.com/glue/latest/dg/limits.html).

## Solution

To resolve the problem of accumulating AWS Glue table versions, the provided Lambda function performs the following tasks:

1. **Fetch Databases and Tables:** The Lambda function iterates over all databases and tables using pagination to handle large datasets.
2. **Delete Old Versions:** It retrieves all table versions and deletes older versions in batches to manage the number of versions effectively.
3. **Timeout Handling:** The function checks the remaining execution time and exits 20 seconds before the timeout to ensure smooth operation and avoid abrupt terminations.
4. **Periodic Execution:** The Lambda function is set up to run periodically via an EventBridge rule to maintain optimal table version counts.

### IAM Permissions

The IAM role used by the Lambda function must have the following permissions:

- `glue:GetDatabases`
- `glue:GetTables`
- `glue:GetTableVersions`
- `glue:BatchDeleteTableVersion`

### Example IAM Policy

Here is an example IAM policy that includes the necessary permissions:

```yaml
# Example IAM Policy for AWS Glue
Policies:
  - PolicyName: GlueTableVersionCleanupPolicy
    PolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Effect: Allow
          Action:
            - glue:GetDatabases
            - glue:GetTables
            - glue:GetTableVersions
            - glue:BatchDeleteTableVersion
          Resource: '*'
```
## How to Use

### Method 1: Deploy Using YAML Configuration

1. **Create IAM Role**: Use the provided YAML to create an IAM role with the necessary permissions for the Lambda function. This YAML defines the policies required to access and modify AWS Glue resources.
   
   **Note**: This YAML is primarily for showing the permissions needed and is not strictly required for deployment.

2. **Deploy Lambda Function**: Use the provided YAML to deploy the Lambda function, including its code, environment variables, and configuration.

3. **Set Up EventBridge Rule**: Create an EventBridge rule to schedule the Lambda function to run periodically (e.g., every 7 days). This ensures the function is executed automatically to clean up old table versions.

### Method 2: Deploy Using AWS Management Console

1. **Create IAM Role**: 
   - Go to the AWS IAM console and create a new role.
   - Attach the following policies to the role:
     - `glue:GetTableVersions`
     - `glue:BatchDeleteTableVersion`
     - `glue:GetDatabases`
     - `glue:GetTables`
   - Save the role and note its ARN for later use.

2. **Deploy Lambda Function**:
   - Go to the AWS Lambda console and create a new Lambda function.
   - Choose "Author from scratch" and configure the function with the following settings:
     - **Runtime**: Python 3.x
     - **Role**: Select the IAM role created in the previous step.
     - **Code**: Copy and paste the provided Python code into the inline editor or upload a ZIP file if preferred.
   - Set environment variables and adjust the function settings as needed.

3. **Set Up EventBridge Rule**:
   - Go to the Amazon EventBridge console.
   - Create a new rule with a schedule expression (e.g., `rate(7 days)`) to trigger the Lambda function.
   - Choose "Lambda function" as the target and select the function created.
## Design and Optimization

The Lambda function has been designed to be simple yet efficient, aiming to manage AWS Glue table version cleanup in a practical and cost-effective manner. The function deletes between 150,000 and 250,000 versions per execution, depending on the data volume and number of versions to remove. This approach was chosen to ensure high efficiency without the need for additional resources like DynamoDB or Glue, keeping costs low.

### Advantages of the Current Implementation

- **Simplicity:** The Lambda function is easy to deploy and does not require complex configurations.
- **Cost-Efficiency:** It does not use additional resources like DynamoDB or Glue, thus reducing overall costs.
- **Efficiency:** The current approach is highly effective for big data systems and real-time ETL, minimizing the risk of crawler blocks due to reaching service quota limits.

### Improvement Opportunities

Although the current implementation is very effective, there are opportunities for further enhancement:

- **Recursive Lambda:** Implementing a recursive Lambda function could enable the management of all old versions more comprehensively. This solution might require more complex state and timeout management.
- **AWS Step Functions:** Using AWS Step Functions to orchestrate the cleanup process in multiple steps could provide a more robust and scalable solution. Step Functions can handle longer and more complex executions, allowing for more thorough and continuous version cleanup.

These improvements could increase the Lambda function's ability to handle even larger quantities of versions but may also introduce additional costs and complexity. However, the current version strikes an optimal balance between simplicity and performance and is suitable for most common use cases.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

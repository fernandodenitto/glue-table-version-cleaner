import boto3
from botocore.exceptions import ClientError

TIMEOUT_THRESHOLD_MS = 20000  # 20 seconds

class GlueCrawlerCleanerHandler:

    def __init__(self, glue_client=None):
        self.glue_client = glue_client or boto3.client('glue')
        self.total_deleted_versions = 0

    def handle_request(self, event, context):
        databases = self.fetch_all_databases()

        for database in databases:
            # Check remaining time before processing each database
            if context.get_remaining_time_in_millis() <= TIMEOUT_THRESHOLD_MS:
                return f"Timeout approaching. Exiting. Total deleted versions: {self.total_deleted_versions}"

            db_name = database['Name']
            tables = self.fetch_all_tables(db_name)

            # Sort tables alphabetically by name
            tables.sort(key=lambda t: t['Name'])

            for table in tables:
                # Check remaining time before processing each table
                if context.get_remaining_time_in_millis() <= TIMEOUT_THRESHOLD_MS:
                    return f"Timeout approaching. Exiting. Total deleted versions: {self.total_deleted_versions}"

                table_name = table['Name']
                self.delete_older_versions_in_batch(db_name, table_name)

                # Check remaining time after processing each table to ensure enough time for the next operation
                if context.get_remaining_time_in_millis() <= TIMEOUT_THRESHOLD_MS:
                    return f"Timeout approaching. Exiting. Total deleted versions: {self.total_deleted_versions}"

        return f"Successfully deleted older table versions. Total deleted versions: {self.total_deleted_versions}"

    # API VERSION WITH PAGINATION
    def fetch_all_databases(self):
        all_databases = []
        next_token = None

        while True:
            kwargs = {}
            if next_token:
                kwargs['NextToken'] = next_token

            response = self.glue_client.get_databases(**kwargs)
            all_databases.extend(response['DatabaseList'])
            next_token = response.get('NextToken')

            if not next_token:
                break

        return all_databases

    def fetch_all_tables(self, database_name):
        all_tables = []
        next_token = None

        while True:
            kwargs = {
                'DatabaseName': database_name
            }
            if next_token:
                kwargs['NextToken'] = next_token

            response = self.glue_client.get_tables(**kwargs)
            all_tables.extend(response['TableList'])
            next_token = response.get('NextToken')

            if not next_token:
                break

        return all_tables

    def fetch_all_table_versions(self, database_name, table_name):
        all_table_versions = []
        next_token = None

        while True:
            kwargs = {
                'DatabaseName': database_name,
                'TableName': table_name
            }
            if next_token:
                kwargs['NextToken'] = next_token

            response = self.glue_client.get_table_versions(**kwargs)
            all_table_versions.extend(response['TableVersions'])
            next_token = response.get('NextToken')

            if not next_token:
                break

        return all_table_versions

    def delete_older_versions_in_batch(self, database_name, table_name):
        versions = self.fetch_all_table_versions(database_name, table_name)

        if len(versions) <= 1:
            print(f"DATABASE {database_name}: No older versions to delete for table {table_name}")
            return

        older_version_ids = [v['VersionId'] for v in versions[1:]]

        print(f"DATABASE {database_name}: Trying to delete {len(older_version_ids)} older versions of table {table_name}")

        batch_size = 100
        total_successfully_deleted = 0

        for i in range(0, len(older_version_ids), batch_size):
            batch = older_version_ids[i:i + batch_size]

            try:
                response = self.glue_client.batch_delete_table_version(
                    DatabaseName=database_name,
                    TableName=table_name,
                    VersionIds=batch
                )

                errors = response.get('Errors', [])
                successfully_deleted = len(batch) - len(errors)

                for error in errors:
                    print(f"DATABASE {database_name}: Failed to delete version {error['VersionId']} from table {table_name} due to {error['ErrorDetail']['ErrorMessage']}")

                self.total_deleted_versions += successfully_deleted
                total_successfully_deleted += successfully_deleted

            except ClientError as e:
                print(f"DATABASE {database_name}: Failed to delete older versions from table {table_name} due to {e}")

        print(f"DATABASE {database_name}: Total successfully deleted older versions of table {table_name}: {total_successfully_deleted}")

# Example usage
# handler = GlueCrawlerCleanerHandler()
# handler.handle_request({}, context)
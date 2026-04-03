import os
from datetime import datetime
import boto3
import botocore

class BackupScript:
    def __init__(self, bucket_name, prefix, suffix, region):
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.suffix = suffix
        self.region = region
        self.s3 = boto3.client('s3', region_name=region)

    def get_backup_files(self):
        try:
            response = self.s3.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=self.prefix,
                Delimiter='/'
            )
            return [f'/{obj.key}' for obj in response.get('Contents', [])]
        except botocore.exceptions.NoCredentialsError:
            print("Credentials not available for AWS")
            exit(1)
        except Exception as e:
            print(f"Failed to get AWS credentials: {e}")
            exit(1)

    def get_backup_files_count(self):
        files = self.get_backup_files()
        return len(files)

    def delete_backup_files(self, days):
        files = self.get_backup_files()
        files = sorted(files, reverse=True)
        cutoff_date = datetime.now() - datetime.timedelta(days=days)
        files_to_delete = [file for file in files if datetime.strptime(file.split('/')[2], '%Y%m%d') < cutoff_date]
        files_to_delete = ','.join(files_to_delete)
        try:
            self.s3.delete_objects(
                Bucket=self.bucket_name,
                Delete={'Objects': [{'Key': file} for file in files_to_delete.split(',')]}
            )
            print(f"Deleted {len(files_to_delete.split(','))} files")
        except Exception as e:
            print(f"Failed to delete backup files: {e}")

if __name__ == "__main__":
    script = BackupScript(bucket_name=os.environ.get('BUCKET_NAME'), prefix=os.environ.get('PREFIX'), suffix=os.environ.get('SUFFIX'), region=os.environ.get('AWS_REGION'))
    script.delete_backup_files(7)
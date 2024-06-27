from dotenv import load_dotenv #for .env variables like the API key
import boto3 # For Amazon S3 uploading
from botocore.exceptions import NoCredentialsError
import os
from pathlib import Path

load_dotenv() 

# Get some context from the the previous story output
def getLast20Words(context):
    context_words = context.split()
    last_20_words = context_words[-20:]
    context = ' '.join(last_20_words)
    return context

# AWS Upload Setup
def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', 
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"), 
        aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"))

    try:
        s3.upload_file(local_file, bucket, s3_file)
    except FileNotFoundError:
        raise FileNotFoundError
    except NoCredentialsError:
        raise NoCredentialsError
    
# Check if file exists in S3 and move it to archive if it does
def check_and_archive_s3_file(bucket, s3_file, archive_folder="archive/"):
    s3_client = boto3.client('s3')

    try:
        s3_client.head_object(Bucket=bucket, Key=s3_file)
        # If the object exists, move it to the archive folder
        copy_source = {'Bucket': bucket, 'Key': s3_file}
        archive_key = f"{archive_folder}{s3_file}"
        s3_client.copy(copy_source, bucket, archive_key)
        s3_client.delete_object(Bucket=bucket, Key=s3_file)
        print(f"Moved existing file to archive: {archive_key}")
    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            # The object does not exist, so no action needed
            print(f"No existing file to move to archive.")
        else:
            raise
    
def deleteTempMp3(loopCount):
    i = 0
    while i < int(loopCount):
        try:
            os.remove(Path(__file__).parent / f'temp_{i}.mp3')
        except FileNotFoundError:
            print(f'temp_output_{i}.mp3 not found.')
        except Exception as e:
            print(f'Error deleting temp_output{i}.mp3: {e}')
        i += 1
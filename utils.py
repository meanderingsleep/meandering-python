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
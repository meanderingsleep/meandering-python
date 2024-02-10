from dotenv import load_dotenv #for .env variables like the API key
import boto3 # For Amazon S3 uploading
import os

load_dotenv() 

# Get some context from the the previous story output
def getLast20Words(context):
    context_words = context.split()
    last_20_words = context_words[-20:]
    context = ' '.join(last_20_words)
    return context

# AWS Upload Setup
def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=os.environ.get("ACCESS_KEY"), aws_secret_access_key=os.environ.get("SECRET_KEY"))

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
    except FileNotFoundError:
        print("Local file not found")
        raise FileNotFoundError
    except NoCredentialsError:
        print("Credentials not available")
        raise NoCredentialsError
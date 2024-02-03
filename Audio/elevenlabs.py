from dotenv import load_dotenv #for .env variables like the API key
import os
from openai import OpenAI
import io
from pathlib import Path
from freeplay import Freeplay 
from freeplay.provider_config import ProviderConfig, OpenAIConfig
import requests
import boto3 # For Amazon S3 uploading
from botocore.exceptions import NoCredentialsError  # Import NoCredentialsError


load_dotenv() 

ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/zcAOhNBS3c14rBihAFp1"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": os.environ.get("XI_API_KEY")
}

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

freeplay_chat = Freeplay(
    provider_config=ProviderConfig(openai=OpenAIConfig(os.environ['OPENAI_API_KEY'])),
    freeplay_api_key=os.environ['FREEPLAY_API_KEY'],
    api_base=f'https://{os.environ["FREEPLAY_CUSTOMER_NAME"]}.freeplay.ai/api')

freeplay_environment = os.environ.get("FREEPLAY_ENVIRONMENT")

chat_completion = freeplay_chat.get_completion(
    project_id=os.environ['FREEPLAY_PROJECT_ID'],
    template_name="story",
    variables={},
    tag=freeplay_environment)

data = {
  "text": chat_completion.content,
  "model_id": "eleven_monolingual_v1",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.5
  }
}

response = requests.post(url, json=data, headers=headers)
with open('output1.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

uploaded = upload_to_aws('output1.mp3', 'sleeplesslv', 'output1.mp3')
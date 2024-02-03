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

# Freeplay prompting configuration
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

# Eleven Labs settings
# data = {
#   "text": chat_completion.content,
#   "model_id": "eleven_monolingual_v1",
#   "voice_settings": {
#     "stability": 0.5,
#     "similarity_boost": 0.5
#   }
# }

# OpenAI instead of ElevenLabs text to speech (I ran out of credits for Eleven Labs)
response = client.audio.speech.create(
  model="tts-1-hd", # Added "hd" because its apparently better
  voice="onyx", # Onyx is the sleepiest voice in my opinion
  input=chat_completion.content
)

response.write_to_file(Path(__file__).parent / "output.mp3")

# Request from Eleven Labs and write it to output.mp3
# response = requests.post(url, json=data, headers=headers)
# with open('output.mp3', 'wb') as f:
#     for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
#         if chunk:
#             f.write(chunk)

# AWS Upload Setup
def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=os.environ.get("ACCESS_KEY"),
                      aws_secret_access_key=os.environ.get("SECRET_KEY"))

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

uploaded = upload_to_aws('output.mp3', 'sleeplesslv', 'output.mp3') # Upload to the sleepless AWS S3 bucket
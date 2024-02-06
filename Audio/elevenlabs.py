from dotenv import load_dotenv #for .env variables like the API key
import os
from openai import OpenAI
import io
from pathlib import Path
from freeplay import Freeplay 
from freeplay.provider_config import ProviderConfig, OpenAIConfig
import requests
import boto3 # For Amazon S3 uploading
from botocore.exceptions import NoCredentialsError

load_dotenv() 

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/zcAOhNBS3c14rBihAFp1" # Elevenlabs voice url

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

story = freeplay_chat.get_completion(
    project_id=os.environ['FREEPLAY_PROJECT_ID'],
    template_name="initialize_story",
    variables={},
    tag=freeplay_environment)

def getLast20Words(context):
    context_words = context.split()  # Split the string into a list of words
    last_20_words = context_words[-20:]  # Get the last 20 words
    context = ' '.join(last_20_words)  # Join the words back into a string
    return context

context = getLast20Words(story.content)

i = 1
while i < 7: # 7 chunks of text and audio at 3500 tokens of text each
    if (i != 1):
        story = freeplay_chat.get_completion(
            project_id=os.environ['FREEPLAY_PROJECT_ID'],
            template_name="continue_story",
            variables={"context":context},
            tag=freeplay_environment)
        context = getLast20Words(story.content)
    
    # OpenAI instead of ElevenLabs text to speech (I ran out of credits for Eleven Labs)
    response = client.audio.speech.create(
        model="tts-1-hd", # Added "hd" because its apparently better
        voice="onyx", # Onyx is the sleepiest voice in my opinion
        input=story.content
    )

    response.write_to_file(Path(__file__).parent / f"output{i}.mp3")

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

    uploaded = upload_to_aws(f'output{i}.mp3', 'sleeplesslv', f'output{i}.mp3') # Upload to the sleepless AWS S3 bucket
    i = i + 1
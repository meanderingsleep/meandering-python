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
from pydub import AudioSegment


load_dotenv() 

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Freeplay prompting configuration
freeplay_chat = Freeplay(
    provider_config=ProviderConfig(openai=OpenAIConfig(os.environ['OPENAI_API_KEY'])),
    freeplay_api_key=os.environ['FREEPLAY_API_KEY'],
    api_base=f'https://{os.environ["FREEPLAY_CUSTOMER_NAME"]}.freeplay.ai/api')

freeplay_environment = os.environ.get("FREEPLAY_ENVIRONMENT")

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
        
# The initial story chunk
story = freeplay_chat.get_completion(
    project_id=os.environ['FREEPLAY_PROJECT_ID'],
    template_name="initialize_story",
    variables={},
    tag=freeplay_environment)

# Get some context from the the previous story output
def getLast20Words(context):
    context_words = context.split()
    last_20_words = context_words[-20:]
    context = ' '.join(last_20_words)
    return context

context = getLast20Words(story.content)
merged = AudioSegment.empty()

# Generate 7 total chunks of text/audio
i = 1
while i <= 50: 
    if (i != 1):
        story = freeplay_chat.get_completion(
            project_id=os.environ['FREEPLAY_PROJECT_ID'],
            template_name="continue_story",
            variables={"context":context},
            tag=freeplay_environment)
        context = getLast20Words(story.content)
    
    # Generate OpenAI instead of ElevenLabs text to speech 
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="onyx",
        input=story.content
    )

    # Write out the current chunk as an wav
    response.write_to_file(Path(__file__).parent / f"output{i}.wav")

    output = AudioSegment.from_file(f'output{i}.wav')
    merged =  merged + output

    i = i + 1

merged.export("final_output.wav", format="wav")
uploaded = upload_to_aws('final_output.wav') # Upload the final file to the AWS S3 bucket
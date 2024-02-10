from dotenv import load_dotenv #for .env variables like the API key
import os
from openai import OpenAI
import io
from pathlib import Path
from freeplay import Freeplay 
from freeplay.provider_config import ProviderConfig, OpenAIConfig
import requests
from botocore.exceptions import NoCredentialsError
from pydub import AudioSegment
from ffmpeg import FFmpeg
import utils
import sys

load_dotenv() 

# make sure the correct number of arguments were passed in.
try:
    len(sys.argv) == 2
    loopCount = sys.argv[1]
    print("Looping " + sys.argv[1] + " times.")
except:
    print("Usage: " + sys.argv[0] + " loopCount")
    sys.exit()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Freeplay prompting configuration
freeplay_chat = Freeplay(
    provider_config=ProviderConfig(openai=OpenAIConfig(os.environ['OPENAI_API_KEY'])),
    freeplay_api_key=os.environ['FREEPLAY_API_KEY'],
    api_base=f'https://{os.environ["FREEPLAY_CUSTOMER_NAME"]}.freeplay.ai/api')

freeplay_environment = os.environ.get("FREEPLAY_ENVIRONMENT")

# The initial story chunk
story = freeplay_chat.get_completion(
    project_id=os.environ['FREEPLAY_PROJECT_ID'],
    template_name="initialize_story",
    variables={},
    tag=freeplay_environment)

context = utils.getLast20Words(story.content)
merged = AudioSegment.empty()

# Generate chunks of text/audio
i = 0
while i < int(loopCount): 
    # Generate OpenAI instead of ElevenLabs text to speech 
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="onyx",
        input=story.content
    )

    # Write out the current chunk as an wav
    response.write_to_file(Path(__file__).parent / f"temp_output{i}.wav")

    merged += AudioSegment.from_file(f'temp_output{i}.wav')

    if (i): # skip this section first time through the loop. this should be dealt with differnetly
        story = freeplay_chat.get_completion(
            project_id=os.environ['FREEPLAY_PROJECT_ID'],
            template_name="continue_story",
            variables={"context":context},
            tag=freeplay_environment)
        context = getLast20Words(story.content)   

    i += 1

outputFileName = "final_output.wav"
merged.export(outputFileName, format="wav")
uploaded = utils.upload_to_aws(outputFileName, 'sleeplesslv', outputFileName) # Upload the final file to the AWS S3 bucket

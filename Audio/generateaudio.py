from dotenv import load_dotenv
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
from datetime import date

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

merged = AudioSegment.empty()
context=""
i = 0

# Generate chunks of text/audio
while i < int(loopCount): 
    story = freeplay_chat.get_completion(
        project_id=os.environ['FREEPLAY_PROJECT_ID'],
        template_name="initialize_story",
        variables={"context":context},
        tag=freeplay_environment
    )

    context = utils.getLast20Words(story.content)

    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="onyx",
        input=story.content
    )

    response.write_to_file(Path(__file__).parent / f"temp_output{i}.mp3")
    merged += AudioSegment.from_file(f'temp_output{i}.mp3')
    i += 1

# Export final file to cloud and cleanup temp files
finalOutputFilename = f"sleepless-{date.today()}.mp3"
finalOutputPath = Path(__file__).parent / finalOutputFilename
merged.export(finalOutputPath, format="mp3", bitrate="192k")
uploaded = utils.upload_to_aws(finalOutputPath, 'sleeplesslv', finalOutputFilename)
utils.deleteTempMp3(loopCount)
os.remove(finalOutputPath)
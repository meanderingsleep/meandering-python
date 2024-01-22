from dotenv import load_dotenv #for .env variables like the API key
import os
from openai import OpenAI
import io
from pathlib import Path
from freeplay import Freeplay
from freeplay.provider_config import ProviderConfig, OpenAIConfig

load_dotenv() 

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

freeplay_chat = Freeplay(
    provider_config=ProviderConfig(openai=OpenAIConfig(os.environ['OPENAI_API_KEY'])),
    freeplay_api_key=os.environ['FREEPLAY_API_KEY'],
    api_base=f'https://{os.environ["FREEPLAY_CUSTOMER_NAME"]}.freeplay.ai/api')

chat_completion = freeplay_chat.get_completion(
    project_id=os.environ['FREEPLAY_PROJECT_ID'],
    template_name="story",
    variables={},
    tag=os.environ.get("FREEPLAY_ENVIRONMENT"))

# convert the text to audio
response = client.audio.speech.create(
  model="tts-1-hd", # Added "hd" because its apparently better
  voice="onyx", # Onyx is the sleepiest voice in my opinion
  input=chat_completion.content
)

response.write_to_file(Path(__file__).parent / "sleepless.mp3")
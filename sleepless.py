from dotenv import load_dotenv #for .env variables like the API key
import os
from openai import OpenAI
import io
from pathlib import Path

load_dotenv() 

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

prompt_text = open("prompt.txt").read()

# get the content that we want to convert to audio
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt_text,
        }
    ],
    model="gpt-4-1106-preview",
)

# create a text file so we can check the story it wrote
bedtime_story = "bedtime_story.txt"
with open(bedtime_story, 'w') as file:
    file.write(chat_completion.choices[0].message.content)

# convert the text to audio
response = client.audio.speech.create(
  model="tts-1-hd", # Added "hd" because its apparently better
  voice="onyx", # Onyx is the sleepiest voice in my opinion
  input=chat_completion.choices[0].message.content
)

response.write_to_file(Path(__file__).parent / "sleepless.mp3")
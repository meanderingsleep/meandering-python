from pathlib import Path
from pydub import AudioSegment
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generateopenai(voiceType, storyContent, i, promptType):
    response = client.audio.speech.create(
                model="tts-1-hd",
                voice=voiceType,
                input=storyContent
            )
    return response
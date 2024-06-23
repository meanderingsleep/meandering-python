import os
from pathlib import Path
import requests
from pydub import AudioSegment
import gendriver

# Male british voice ID: 
# Female british voice ID: 

def generateelevenlabs():

    tts_url = f'https://api.elevenlabs.io/v1/text-to-speech/{gendriver.args.voiceType}'
    CHUNK_SIZE = 1024
    headers = {
    "Accept": "application/json",
    "xi-api-key": os.environ['XI_API_KEY']
    }

    data = {
        "text": gendriver.story.content,
        "model_id": "eleven_turbo_v2",
        "voice_settings": {
            "stability": 0.9,
            "similarity_boost": 0.9,
            "style": 0.0,
            "use_speaker_boost": True
            }
    }
    # Merge audio after creation
    response = requests.post(tts_url, headers=headers, json=data, stream=True)
    if response.ok:
        with open(f"temp_output_{gendriver.i}.mp3", "wb") as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
            gendriver.merged += AudioSegment.from_file(Path(__file__).parent.parent / f'/home/ec2-user/sleepless/Audio/temp_output_{gendriver.i}.mp3')
    else:
        print(response.text)
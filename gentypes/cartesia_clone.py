import requests
import json
import subprocess
import os

# ---
# Create a custom voice using local mp3 
# ---

url = "https://api.cartesia.ai/voices/clone/clip"
audio_file_path = "logan.mp3"
with open(audio_file_path, "rb") as file:
    files = {
        "clip": file,
        "enhance": (None, "true")
    }

    headers = {
        "Cartesia-Version": "2024-06-10",
        "X-API-Key": os.environ.get("CARTESIA_API_KEY")
    }

    response = requests.post(url, files=files, headers=headers)

# ---
# Create the voice using the new embedding 
# --- 

# Problem
# type of response is app.Embedding
# need it to be Voice.embedding

embedding_data = json.loads(response.text)

embedding = embedding_data.get('embedding')

url = "https://api.cartesia.ai/voices"

payload = {
    "name": "Logan",
    "description": "Me.",
    "embedding": embedding
}
headers = {
    "Cartesia-Version": "2024-06-10",
    "X-API-Key": os.environ["CARTESIA_API_KEY"],
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

voice = json.loads(response.text)
id = voice.get("id")

url = "https://api.cartesia.ai/tts/bytes"

headers = {
    "Cartesia-Version": "2024-06-10",
    "X-API-Key": os.environ["CARTESIA_API_KEY"],
    "Content-Type": "application/json"
}
data = {
    "transcript": "Welcome to Cartesia Sonic!",
    "model_id": "sonic-english",
    "voice": {
        "mode": "id",
        "id": id
    },
    "output_format": {
        "container": "raw",
        "encoding": "pcm_f32le",
        "sample_rate": 44100
    }
}

response = requests.post(url, headers=headers, json=data, stream=True)

if response.status_code == 200:

    ffmpeg_command = [
        "ffmpeg",
        "-f", "f32le",
        "-i", "pipe:",
        "sonic.wav"
    ]
    
    process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)
    
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            process.stdin.write(chunk)
    
    process.stdin.close()
    process.wait()
    
    print("Audio file 'sonic.wav' has been created.")
else:
    print(f"Error: {response.status_code}")
    print(response.text)


import requests
import subprocess

url = "https://api.cartesia.ai/tts/bytes"

headers = {
    "Cartesia-Version": "2024-06-10",
    "X-API-Key": "73fc7125-3416-4b04-82a5-0d4b3d5457c5",
    "Content-Type": "application/json"
}
data = {
    "transcript": "Welcome to Cartesia Sonic!",
    "model_id": "sonic-english",
    "voice": {
        "mode": "id",
        "id": "a0e99841-438c-4a64-b679-ae501e7d6091"
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
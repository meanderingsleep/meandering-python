import requests

url = "https://api.cartesia.ai/tts/bytes"

payload = {
    "model_id": "sonic-english",
    "transcript": "Felix is such a retarded pussy.",
    "duration": 123,
    "voice": {
        "mode": "id",
        "id": "a88c785b-6266-404a-b02e-993df876a403"
    },
    "output_format": {
        "container": "wav",  # Set to wav
        "encoding": "pcm_s16le",
        "sample_rate": 8000
    },
    "language": "en"
}
headers = {
    "Cartesia-Version": "2024-06-10",
    "X-API-Key": "f6e95745-ea2b-463c-aebe-0e4a1fef5c55",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

if response.status_code == 200:
    with open("output.wav", "wb") as f:
        f.write(response.content)
    print("Audio saved as output.wav")
else:
    print("Failed to get audio:", response.text)

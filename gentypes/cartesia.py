# import os
# import io
# from pathlib import Path
# from pydub import AudioSegment
# from cartesia.tts import CartesiaTTS
# from io import BytesIO
# import numpy as np
# import wave
# import sounddevice as sd
# import gendriver

# def generatecartesia(content):
#     voice = 'be7d6af6-3bd8-4953-84ae-adda8113ea69'
#     transcript = content

#     # config
#     api_key = os.environ.get("CARTESIA_API_KEY")
#     assert api_key is not None
#     gen_cfg = dict(model_id="upbeat-moon", data_rtype='array', output_format='pcm')

#     # create client
#     client = CartesiaTTS(api_key=api_key)
#     voice = client.get_voice_embedding(voice_id="")

#     output = client.generate(transcript=transcript, voice=voice, stream=False, **gen_cfg)

#     # generate audio
#     buffer = output["audio"]
#     rate = output["sampling_rate"]
#     filename = "output_audio.wav"

#     sd.play(buffer, rate, blocking=True) # Verify output is working

#     # Save the audio data to a file
#     with wave.open(filename, 'wb') as wf:
#         wf.setnchannels(1)  # Assuming mono audio
#         wf.setsampwidth(2)  # PCM uses 2 bytes
#         wf.setframerate(rate)
#         wf.writeframes(buffer)
    
#     return filename

#     # audio_data = output["audio"]
#     # rate = output["sampling_rate"]

#     # # Save audio data to a temporary file
#     # with wave.open("temp_audio.wav", "wb") as wav_file:
#     #     wav_file.setnchannels(1)
#     #     wav_file.setsampwidth(2)  # Assuming 16-bit samples
#     #     wav_file.setframerate(rate)
#     #     wav_file.writeframes(np.array(audio_data).tobytes())

#     # return "temp_audio.wav"
# Driver file for generating openai, elevenlabs, or cartesia's TTS.

from dotenv import load_dotenv
import os
from pathlib import Path
from freeplay import Freeplay
from freeplay.provider_config import ProviderConfig, OpenAIConfig
from pydub import AudioSegment
import utils
import argparse
from gentypes import cartesia
from gentypes import elevenlabs
from gentypes import openai
import io

load_dotenv()

def main():
    # Command line arguments
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('loopCount', type=int, help='Number of loops')
    parser.add_argument('promptType', type=str, help='Type of prompt')
    parser.add_argument('voiceType', type=str, help='Type of voice')
    parser.add_argument('gender', type=str, help='Gender')
    parser.add_argument('provider', type=str, help='Provider')
    parser.add_argument('day', type=str, help='Day')

    args = parser.parse_args()

    print(f"Loops: {args.loopCount}")
    print(f"Prompt: {args.promptType}")
    print(f"Voice: {args.voiceType}")
    print(f"Gender: {args.gender}")
    print(f"Provider: {args.provider}")
    print(f"Day: {args.day}")

    # Freeplay prompting configuration
    freeplay_chat = Freeplay(
        provider_config=ProviderConfig(openai=OpenAIConfig(os.environ['OPENAI_API_KEY'])),
        freeplay_api_key=os.environ['FREEPLAY_API_KEY'],
        api_base=f'https://{os.environ["FREEPLAY_CUSTOMER_NAME"]}.freeplay.ai/api')

    freeplay_environment = os.environ.get("FREEPLAY_ENVIRONMENT")

    # Creating the empty context and merged file
    merged = AudioSegment.empty()
    context=""
    i = 0

    # Generate chunks of text/audio
    while i < int(args.loopCount):
        if (i == 0 and args.promptType == "meandering"):
            story = freeplay_chat.get_completion(
                project_id=os.environ['FREEPLAY_PROJECT_ID'],
                template_name="meandering_starter",
                variables={},
                tag=freeplay_environment
            )
        else:
            story = freeplay_chat.get_completion(
                project_id=os.environ['FREEPLAY_PROJECT_ID'],
                template_name=args.promptType,
                variables={"context":context},
                tag=freeplay_environment
            )

        context = utils.getLast20Words(story.content)

        if (args.provider == 'openai'):
            response = openai.generateopenai(args.voiceType, story.content, i, args.promptType)

        elif (args.provider == 'elevenlabs'):
            response = elevenlabs.generatelevenlabs()

        elif (args.provider == 'cartesia'):
            response = cartesia.generatecartesia(story.content)

        response.write_to_file(f'temp_{i}.mp3')
        audio_segment = AudioSegment.from_file(f'temp_{i}.mp3')
        merged += audio_segment
        silence = AudioSegment.silent(duration=750)
        merged += silence

        i += 1

    # Export to S3
    finalOutputFilename = f"{args.day}_{args.promptType}_{args.gender}.mp3"
    finalOutputPath = Path(__file__).parent / finalOutputFilename
    bucket_name = os.environ.get("AWS_S3_BUCKET")

    # Check and archive existing file if it exists
    utils.check_and_archive_s3_file(bucket_name, finalOutputFilename)

    merged.export(finalOutputPath, format="mp3", bitrate="192k")
    uploaded = utils.upload_to_aws(finalOutputPath, bucket_name, finalOutputFilename)

    # Remove the final audio file and temp files
    utils.deleteTempMp3(args.loopCount)
    os.remove(finalOutputPath)

if __name__ == "__main__":
    main()
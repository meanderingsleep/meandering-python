from datetime import datetime
import os
import utils

now = datetime.now()
day_of_week = now.strftime("%A")

# Classic female
uploaded_classic_female = utils.upload_to_aws(f'{day_of_week}_classic_female.mp3', 
    os.environ.get("AWS_S3_BUCKET"), 
    'classic_female.mp3')

if uploaded_classic_female:
    print("Classic female uploaded")
else:
    print("Failed to upload classic female")

# Classic male
uploaded_classic_male = utils.upload_to_aws(f'{day_of_week}_classic_male.mp3', 
    os.environ.get("AWS_S3_BUCKET"), 
    'classic_male.mp3')

if uploaded_classic_male:
    print("Classic male uploaded")
else:
    print("Failed to upload classic male")

# Weather male
uploaded_weather_male = utils.upload_to_aws(f'{day_of_week}_weather_male.mp3', 
    os.environ.get("AWS_S3_BUCKET"), 
    'weather_male.mp3')

if uploaded_weather_male:
    print("Weather male uploaded")
else:
    print("Failed to upload weather male")

# Weather female
uploaded_weather_female = utils.upload_to_aws(f'{day_of_week}_weather_female.mp3', 
    os.environ.get("AWS_S3_BUCKET"), 
    'weather_female.mp3')

if uploaded_weather_female:
    print("Weather female uploaded")
else:
    print("Failed to upload weather female")
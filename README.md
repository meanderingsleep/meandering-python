# sleepless

Requirements:
- python3
- python3 -m pip install -r requirements.txt (generate requirements.txt via pipreqs)
- ffmpeg install near bottom of - https://github.com/jiaaro/pydub#installation

Tests:
run "python3 audiotests.py" to make sure tests pass.

# Usage

Template: python generateaudio.py LOOPCOUNT PROMPTNAME VOICE GENDER PROVIDER DAY
ElevenLabs example: python gendriver.py 25 initialize_weather_story ThT5KcBeYPX3keUQqHPh female elevenlabs thursday
OpenAI example: python gendriver.py 25 initialize_story onyx male openai monday

# Amazon Linux EC2 instance setup

- SETUP base environment
- sudo yum install git -y
- sudo yum install python3.11.x86_64
- sudo yum install python3.11-pip.noarch
- wget -O ffmpeg.tar.xz https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz
- tar xf ffmpeg.tar.xz
- rm ffmpeg.tar.xz
- sudo mv ffmpeg-git-20240213-amd64-static/ffmpeg /usr/bin
- sudo mv ffmpeg-git-20240213-amd64-static/ffprobe /usr/bin

- SETUP sleepless code repository
- ssh-keygen
- install new public key in github
- git clone git@github.com:jvaleski/sleepless.git

- SETUP api keys in the env
- follow .envexample on github
- python3.11 -m pip install -r requirements.txt

- SETUP cron
- sudo yum install cronie
- sudo systemctl start crond
- sudo systemctl enable crond
- sudo systemctl status crond

- Crontab Example: (NOTE: You need to absolute path each file in the gen scripts and in the cron job)
- python3.11 /home/ec2-user/sleepless/Audio/generateaudio.py 2 > /usr/tmp/generateaudio.log 2>&1


# sleepless

Requirements:
- python 3.11.6 (3.11.6+ might work)
- python3[.11] -m pip install -r requirements.txt (generate requirements.txt via pipreqs)
- ffmpeg install near bottom of - https://github.com/jiaaro/pydub#installation

Tests:
run "python3[.11] audiotests.py" to make sure tests pass.

# Amazon Linux EC2 instance setup

- SETUP base environment
- sudo passwd ec2-user (this might not be required)
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

- Add the following to crontab and adjust timing depending on needs
- python3.11 /home/ec2-user/sleepless/Audio/generateaudio.py 2 > /usr/tmp/generateaudio.log 2>&1
- Also edit generateaudio.py to include the absolute path of the temp audio mp3 paths.

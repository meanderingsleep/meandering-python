# sleepless

Requirements:
- python 3.11.7 (3+ might work)
- pip install -r requirements.txt
- ffmpeg install near bottom of - https://github.com/jiaaro/pydub#installation

Tests:
run "python audiotests.py" to make sure tests pass.

# Amazon Linux EC2 instance shell setup

- sudo passwd ec2-user
- yum install git -y
- git clone https://github.com/pyenv/pyenv.git ~/.pyenv
- echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
- echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
- echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
- yum install gcc zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel
- source ~/.bashrc
- pyenv install 3.11.7
- pyenv global 3.11.7
- wget -O ffmpeg.tar.xz https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz
- change into the installation director and move the bins
- sudo mv ffmpeg /usr/bin
- sudo mv ffprobe /usr/bin


- ssh-keygen -t ed25519 -C "your_email@example.com"
- install new public key in github
- git clone git@github.com:jvaleski/sleepless.git

- setup api keys in the env
- follow .envexample on github

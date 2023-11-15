# A Dockerfile is a text document that contains all the commands
# a user could call on the command line to assemble an image.
# Our Debian with python is now installed.
# Imagine we have folders /sys, /tmp, /bin etc. there
# like we would install this system on our laptop.

FROM python:3.10
RUN apt update
RUN apt install curl -y
RUN su -c "pip install --upgrade pip"
RUN apt install software-properties-common -y

# Customization
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" -- \
    -t https://github.com/denysdovhan/spaceship-prompt \
    -a 'SPACESHIP_PROMPT_ADD_NEWLINE="false"' \
    -a 'SPACESHIP_PROMPT_SEPARATE_LINE="false"' \
    -p git \
    -p ssh-agent \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions



#LightHouse
RUN su -c "curl -s https://deb.nodesource.com/setup_16.x | bash"
RUN su -c "apt install nodejs -y"
RUN su -c "apt install npm -y"
RUN su -c "apt install net-tools -y"
RUN su -c "npm install -g lighthouse"
RUN su -c "apt install chromium -y"
RUN su -c "pip3 install git+https://github.com/Cornatul/lighthouse-python.git#egg=lighthouse"


WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . .


#Custom Stuff
RUN su -c "pip3 install gnews"
RUN su -c "pip3 install hypercorn"
RUN su -c "pip3 install uvicorn"
RUN su -c "python3 -m nltk.downloader -d /usr/local/share/nltk_data punkt"
RUN su -c "python3 -m nltk.downloader -d /usr/local/share/nltk_data stopwords"
RUN su -c "python3 -m nltk.downloader -d /usr/local/share/nltk_data vader_lexicon"
RUN su -c "python3 -m spacy download en_core_web_md"
RUN su -c "python3 -m textblob.download_corpora"

ADD . /app/

LABEL maintainer="Stefan <stefan@lzomedia.com>"
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

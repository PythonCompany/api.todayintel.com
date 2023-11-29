FROM python:3.10
LABEL maintainer="Stefan <stefan@lzomedia.com>"
RUN apt update
RUN apt install curl -y
RUN apt install nodejs -y
RUN apt install npm -y
RUN npm install -y lighthouse -g
RUN apt install mlocate -y
RUN apt install net-tools -y

# NVM Install
#SHELL ["/bin/bash", "--login", "-c"]
#RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash

RUN pip install --upgrade pip
RUN apt install software-properties-common -y
RUN apt install openjdk-17-jdk -y
RUN java --version
WORKDIR /app
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

RUN su -c "apt install chromium -y"
RUN su -c "pip3 install git+https://github.com/Cornatul/lighthouse-python.git#egg=lighthouse"




COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . .


# Install some other packages and download the models
RUN su -c "pip3 install uvicorn"
RUN su -c "pip3 install gnews"
RUN su -c "python3 -m nltk.downloader -d /usr/local/share/nltk_data wordnet"
RUN su -c "python3 -m nltk.downloader -d /usr/local/share/nltk_data punkt"
RUN su -c "python3 -m nltk.downloader -d /usr/local/share/nltk_data stopwords"
RUN su -c "python3 -m nltk.downloader -d /usr/local/share/nltk_data vader_lexicon"
RUN su -c "python3 -m spacy download en_core_web_md"
RUN su -c "python3 -m textblob.download_corpora"


RUN updatedb

ADD . /app/


EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]

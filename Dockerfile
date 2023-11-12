FROM python:3.10
RUN apt update
RUN apt install curl -y
WORKDIR /app/
ADD requirements.txt /app/
ADD . /app/
RUN su -c "curl -s https://deb.nodesource.com/setup_16.x | bash"
RUN su -c "apt install nodejs -y"
RUN su -c "apt install npm -y"
RUN su -c "npm install -g lighthouse"
RUN su -c "apt install chromium -y"
RUN su -c "pip3 install git+https://github.com/Cornatul/lighthouse-python.git#egg=lighthouse"
RUN su -c "pip3 install html5lib"
RUN su -c "pip3 install selenium"
RUN su -c "pip3 install python-dotenv"
RUN su -c "pip3 install tomd"
RUN su -c "pip3 install pandoc"
RUN su -c "pip3 install pytrends"
RUN su -c "pip3 install tweepy"
RUN su -c "pip3 install python-decouple"
RUN su -c "pip3 install pypandoc"
RUN su -c "pip3 install prompt_toolkit"
RUN su -c "pip3 install rich"
RUN su -c "pip3 install hypercorn"
RUN su -c "pip3 install google-search-results"
RUN su -c "pip3 install socials"
RUN su -c "pip3 install feedfinder2"
RUN su -c "pip3 install pika"
RUN su -c "pip3 install pyseoanalyzer"
RUN su -c "pip3 install email-validator"
RUN su -c "pip3 install markdownify"
RUN su -c "pip3 install newspaper3k"
RUN su -c "pip3 install fastapi"
RUN su -c "pip3 install feedparser"
RUN su -c "pip3 install pydantic"
RUN su -c "pip3 install pysocks"
RUN su -c "pip3 install requests"
RUN su -c "pip3 install GoogleNews"
RUN su -c "pip3 install vaderSentiment"
RUN su -c "pip3 install spacy"

RUN su -c "pip3 install nltk"
RUN su -c "pip3 install textblob"
RUN su -c "python3 -m nltk.downloader -d /usr/local/share/nltk_data punkt"
RUN su -c "python3 -m nltk.downloader -d /usr/local/share/nltk_data stopwords"
RUN su -c "python3 -m nltk.downloader -d /usr/local/share/nltk_data vader_lexicon"
RUN su -c "python3 -m spacy download en_core_web_md"
RUN su -c "python3 -m textblob.download_corpora"

EXPOSE 8000
CMD [ "python", "./rabbitmq.py"]
CMD ["hypercorn", "main:app", "-b", "0.0.0.0:8000", "--reload"]

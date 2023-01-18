FROM python:3.10
RUN apt update
WORKDIR /app/
ADD requirements.txt /app/
ADD . /app/
RUN su -c "pip3 install hypercorn"
RUN su -c "pip3 install email-validator"
RUN su -c "pip3 install markdownify"
RUN su -c "pip3 install newspaper3k"
RUN su -c "pip3 install fastapi"
RUN su -c "pip3 install feedparser"
RUN su -c "pip3 install pydantic"
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
CMD ["hypercorn", "main:app", "-b", "0.0.0.0:8000", "--reload"]

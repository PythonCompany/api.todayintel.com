import newspaper
import feedparser
import spacy
import datetime as dt
from markdownify import markdownify as md

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from newspaper import Config
from pydantic import BaseModel
from GoogleNews import GoogleNews
from newspaper import Article
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.stem.porter import *
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse

stemmer = PorterStemmer()
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()

nlp = spacy.load("en_core_web_md")

now = dt.date.today()
now = now.strftime('%m-%d-%Y')
yesterday = dt.date.today() - dt.timedelta(days=1)
yesterday = yesterday.strftime('%m-%d-%Y')


from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest

from TextSummarizer import *


tags_metadata = [
    {
        "name": "trending-terms",
        "description": "This will show you the trending terms in the newspapers across the world",
    },
    {
        "name": "google-news",
        "description": "This will print you the past 7 days news for a keyword and a certain language ",
    },
    {
        "name": "feed-reader",
        "description": "This will extract the latest entries from a feed",
    },
    {
        "name": "article",
        "description": "This will extract the article from a feed and provide you with some nlp tasks",
    },
    {
        "name": "summarize",
        "description": "This this will summarize a piece of text",
    },
]


app = FastAPI(
    title="NLP App",
    description="This is a NLP app that allows you the user to perform simple nlp tasks",
    version="1.0",
    terms_of_service="https://nlpapi.org/terms/",
    contact={
        "name": "Stefan I",
        "url": "https://lzomedia.com/",
        "email": "stefan@LzoMedia.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


class PostAction(BaseModel):
    query: str
class FeedReader(BaseModel):
    link: str
class GoogleNewsAction(BaseModel):
    keyword: str
    language: str
class TwitterAction(BaseModel):
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str
class SummarizeAction(BaseModel):
    text: str



@app.get("/")
async def root():
    return {"data": {
        "response": "Welcome to the NLP Api - for documentation please visit /docs ",
    }}


@app.get("/trending-terms")
async def root():
    return {"data": {
        "response": newspaper.hot(),
    }}


#Todo Improve this
@app.post("/google-news")
async def root(google: GoogleNewsAction):
    googlenews = GoogleNews(lang=""+google.language+"", period='7d')
    googlenews.search(google.keyword)
    return {"data": {
        "keyword": google.keyword,
        "response": googlenews.results(),
    }}


"""Article Extract"""


@app.post("/feed-reader")
async def root(feed: FeedReader):
    response = feedparser.parse(feed.link)
    return {"data": {
        "feed-link": feed.link,
        "response": {
            "title": response.feed.get('title', ''),
            "entries": response.entries
        },

    }}

@app.post("/article")
async def root(feed: FeedReader):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/50.0.2661.102 Safari/537.36 '
    config = Config()
    config.browser_user_agent = user_agent
    crawler = Article(feed.link,config=config, keep_article_html=True)
    crawler.download()
    crawler.parse()
    crawler.nlp()
    doc = nlp(crawler.text)
    sentiment = SentimentIntensityAnalyzer()
    entities = [(e.text, e.start_char, e.end_char, e.label_) for e in doc.ents]

    data = {
        "data": {
            "title": crawler.title,
            "date": crawler.publish_date,
            "text": crawler.text,
            "markdown": md(crawler.article_html, newline_style="BACKSLASH"),
            "html": crawler.article_html,
            "summary": crawler.summary,
            "keywords": crawler.keywords,
            "authors": crawler.authors,
            "banner": crawler.top_image,
            "images": crawler.images,
            "entities": entities,
            "videos": crawler.movies,
            "sentiment": sentiment.polarity_scores(crawler.text)
        },
    }
    return data



@app.post("/summarize")
async def root(summarize: SummarizeAction):
    # Counting number of words in original article
    original_words = summarize.text.split()
    original_words = summarize.text.split()
    original_words = [w for w in original_words if w.isalnum()]
    num_words_in_original_text = len(original_words)

    # Converting received text into sapcy Doc object
    text = nlp(summarize.text)

    # Extracting all sentences from the text in a list
    sentences = list(text.sents)
    total_sentences = len(sentences)

    # Generating Frequency Matrix
    freq_matrix = frequency_matrix(sentences)

    # Generating Term Frequency Matrix
    tf_matrixx = tf_matrix(freq_matrix)

    # Getting number of sentences containing a particular word
    num_sent_per_words = sentences_per_words(freq_matrix)

    # Generating ID Frequency Matrix
    idf_matrixx = idf_matrix(freq_matrix, num_sent_per_words, total_sentences)

    # Generating Tf-Idf Matrix
    tf_idf_matrixx = tf_idf_matrix(tf_matrixx, idf_matrixx)

    # Generating Sentence score for each sentence
    sentence_scores = score_sentences(tf_idf_matrixx)

    # Setting threshold to average value (You are free to play with ther values)
    threshold = average_score(sentence_scores)

    # Getting summary
    summary = create_summary(sentences, sentence_scores, 1.3 * threshold)
    return {"data": {
        "response": summary,
    }}



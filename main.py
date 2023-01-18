import datetime as dt
import newspaper
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from newspaper import Config
import feedparser
from pydantic import BaseModel
from GoogleNews import GoogleNews
from newspaper import Article
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import T5Tokenizer, T5ForConditionalGeneration
from nltk.stem.porter import *

stemmer = PorterStemmer()
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()

nlp = spacy.load("en_core_web_md")

now = dt.date.today()
now = now.strftime('%m-%d-%Y')
yesterday = dt.date.today() - dt.timedelta(days=1)
yesterday = yesterday.strftime('%m-%d-%Y')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


class PostAction(BaseModel):
    query: str


class TwitterAction(BaseModel):
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str


class TranslateAction(BaseModel):
    text: str
    lang: str


description = """
NLP API
## Trending
You can **get the latest trending news**.
"""


@app.get("/api/v1/trending-websites")
async def root():
    return {"data": {
        "response": newspaper.popular_urls(),
    }}


@app.post("/api/v1/translate")
async def root(post: TranslateAction):
    # Translation section
    tokenizer = T5Tokenizer.from_pretrained("t5-small")
    model = T5ForConditionalGeneration.from_pretrained("t5-small")
    input_ids = tokenizer("translate English to German: " + post.text, return_tensors="pt").input_ids
    outputs = model.generate(input_ids)
    return {"data": {
        "response": tokenizer.decode(outputs[0], skip_special_tokens=True),
    }}


@app.get("/api/v1/trending-terms")
async def root():
    return {"data": {
        "response": newspaper.hot(),
    }}


@app.post("/api/v1/google-news")
async def root(post: PostAction):
    googlenews = GoogleNews(lang='en', period='7d')
    googlenews.search(post.query)
    return {"data": {
        "query": post.query,
        "response": googlenews.results(),
    }}


"""Article Extract"""


@app.post("/api/v1/feed-reader")
async def root(post: PostAction):
    response = feedparser.parse(post.query)
    return {"data": {
        "query": post.query,
        "response": {
            "title": response.feed.get('title', ''),
            "entries": response.entries
        },

    }}


@app.post("/api/v1/article-extract")
async def root(post: PostAction):
    user_agent = 'Chrome/50.0.2661.102 Safari/537.36 '
    config = Config()
    config.browser_user_agent = user_agent
    crawler = Article(post.query, keep_article_html=True, config=config)
    crawler.download()
    crawler.parse()
    crawler.nlp()

    data = {
        "title": crawler.title,
        "text": crawler.text,
        "html": crawler.article_html,
        "summary": crawler.summary,
        "keywords": crawler.keywords,
        "authors": crawler.authors,
        "videos": crawler.movies,
        "images": crawler.images
    }
    return {"data": data}


@app.post("/api/v1/article-sentiment")
async def root(post: PostAction):
    nlp = spacy.load("en_core_web_md")
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/50.0.2661.102 Safari/537.36 '
    config = Config()
    config.browser_user_agent = user_agent
    crawler = Article(post.query, keep_article_html=True, config=config)
    crawler.download()
    crawler.parse()
    crawler.nlp()
    doc = nlp(crawler.text)
    sentiment = SentimentIntensityAnalyzer()
    entities = [(e.text, e.start_char, e.end_char, e.label_) for e in doc.ents]
    data = {
        "title": crawler.title,
        "date": crawler.publish_date,
        "text": crawler.text,
        "html": crawler.article_html,
        "summary": crawler.summary,
        "keywords": crawler.keywords,
        "authors": crawler.authors,
        "images": crawler.images,
        "entities": entities,
        "videos": crawler.movies,
        "sentiment": sentiment.polarity_scores(crawler.text)
    }
    return {"data": data}


# @todo implement this
@app.post("/api/v1/share/twitter")
async def root(post: TwitterAction):
    response = feedparser.parse(post.consumer_secret)
    return {"data": {
        "query": post.consumer_secret,
        "response": {
            "title": response.feed.get('title', ''),
            "entries": response.entries
        },

    }}

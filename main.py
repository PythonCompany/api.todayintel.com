import newspaper
import feedparser
import spacy
import socials
from pytrends.request import TrendReq

from spacy_html_tokenizer import create_html_tokenizer

pytrends = TrendReq(hl='en-GB', tz=360)

import datetime as dt
from markdownify import markdownify as md


from selenium import webdriver


from feedfinder2 import find_feeds
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from newspaper import Config
from pydantic import BaseModel
from GoogleNews import GoogleNews
from newspaper import Article
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.stem.porter import *
from seoanalyzer import analyze
from lighthouse import LighthouseRunner
from classes.Bard import Chatbot

stemmer = PorterStemmer()
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()
from spacy import displacy

nlp = spacy.load("en_core_web_md")



now = dt.date.today()
now = now.strftime('%m-%d-%Y')
yesterday = dt.date.today() - dt.timedelta(days=1)
yesterday = yesterday.strftime('%m-%d-%Y')

from classes.TextSummarizer import *
from decouple import config

import tweepy
from decouple import config

# Twitter trends

tags_metadata = [
    {
        "name": "Get Trending Terms",
        "description": "This will show you the trending terms in the newspapers across the world",
    },
    {
        "name": "Find Google News ",
        "description": "This will find google news for a certain topic in the past x days news for a keyword and a "
                       "certain language ",
    },
    {
        "name": "Feed reader",
        "description": "This will extract the latest entries from a feed",
    },
    {
        "name": "Feed Finder",
        "description": "This will try to find the feeds associated with a domain",
    },
    {
        "name": "Get article",
        "description": "This will extract the full article from a link and provide you with some nlp information",
    },
    {
        "name": "Summarize Text",
        "description": "This this will summarize a piece of text",
    },
    {
        "name": "Seo analyze",
        "description": "This this will analyze a website using seo analyzer",
    },
    {
        "name": "Get Lighthouse Analysis",
        "description": "This will generate a Lighthouse report regarding your website",
    },
]

app = FastAPI(
    title="NLP App",
    description="This is a NLP app that allows you the user to perform simple nlp tasks",
    version="1.1",
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


class BardAuth(BaseModel):
    session_id: str
    message: str




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
    newspaper_hot_trends = newspaper.hot()
    trends = pytrends.realtime_trending_searches(pn='GB')

    return {

        "data": {
            "newspaper": newspaper_hot_trends,
            "google": trends["title"].tolist(),
        }
    }


@app.post("/google-news")
async def root(google: GoogleNewsAction):
    googlenews = GoogleNews(lang="" + google.language + "", period='7d')
    googlenews.search(google.keyword)

    return {"data": {
        "keyword": google.keyword,
        "response": googlenews.results(),
    }}


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


@app.post("/feed-finder")
async def root(feed: FeedReader):
    response = find_feeds(feed.link)
    return {"data": {
        "feed-link": feed.link,
        "response": response,

    }}


@app.post("/article")
async def root(feed: FeedReader):

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/50.0.2661.102 Safari/537.36 '
    config = Config()
    config.browser_user_agent = user_agent
    crawler = Article(feed.link, config=config, keep_article_html=True)
    crawler.download()
    crawler.parse()
    crawler.nlp()

    nlp.add_pipe('dbpedia_spotlight')
    doc = nlp(crawler.text)

    sentiment = SentimentIntensityAnalyzer()
    entities = [(e.text, e.start_char, e.end_char, e.label_) for e in doc.ents]

    social = socials.extract(feed.link).get_matches_per_platform()

    data = {
        "data": {
            "title": crawler.title,
            "date": crawler.publish_date,
            "text": crawler.text,
            "markdown": md(crawler.article_html, newline_style="BACKSLASH", strip=['a'], heading_style="ATX"),
            "html": crawler.article_html,
            "summary": crawler.summary,
            "keywords": crawler.keywords,
            "authors": crawler.authors,
            "banner": crawler.top_image,
            "images": crawler.images,
            "entities": entities,
            "videos": crawler.movies,
            "social": social,
            "spacy": displacy.render(doc, style="ent"),
            "sentiment": sentiment.polarity_scores(crawler.text),
        },
    }
    return data


@app.post("/summarize")
async def root(summarize: SummarizeAction):
    # Counting number of words in original article
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


@app.post("/seo-analyze")
async def root(feed: FeedReader):
    output = analyze(feed.link, follow_links=False, analyze_headings=True, analyze_extra_tags=True)
    return {"data": {
        "response": output,

    }}


@app.post("/lighthouse")
async def root(feed: FeedReader):
    report = LighthouseRunner(feed.link, form_factor='desktop', quiet=False).report

    return {"data": {
        "response": report,
    }}

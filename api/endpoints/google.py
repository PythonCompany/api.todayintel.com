import json
import base64
import newspaper
import datetime as dt
import sqlite3
import functools
import re
from datetime import datetime
from fastapi import APIRouter, Path, Query, Depends
from pydantic import BaseModel
from cachetools import TTLCache
from pytrends.request import TrendReq
from gnews import GNews
from GoogleNews import GoogleNews

pytrends = TrendReq(hl='en-GB', tz=360)

router = APIRouter()

now = dt.date.today()
now = now.strftime('%m-%d-%Y')
yesterday = dt.date.today() - dt.timedelta(days=1)
yesterday = yesterday.strftime('%m-%d-%Y')

# Assuming you have a SQLite database file named 'keywords.db'
conn = sqlite3.connect('keywords.db')
cursor = conn.cursor()

# Create a table to store keywords and their appearance count if it doesn't exist already
cursor.execute('''
    CREATE TABLE IF NOT EXISTS keywords (
        keyword TEXT PRIMARY KEY,
        appearances INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

class GoogleAction(BaseModel):
    topic: str = Query(None, alias="item-query",
                       title="The topic to extract the news from: WORLD, NATION, BUSINESS, TECHNOLOGY, "
                             "ENTERTAINMENT, SPORTS, SCIENCE, HEALTH."),


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(MyJSONEncoder, self).default(obj)

trending_terms_cache = TTLCache(maxsize=5000, ttl=6 * 60 * 60)

@router.get("/google/trending")
async def root(cache: TTLCache = Depends(lambda: trending_terms_cache)):
    # Check if the data is already in the cache
    if "keywords" in cache:
        return {"data": cache["keywords"]}

    # If not in cache, fetch and calculate the keywords
    newspaper_hot_trends = newspaper.hot()
    trends = pytrends.realtime_trending_searches(pn='GB')['entityNames']
    merged_trends = []
    merged_trends.extend(newspaper_hot_trends)
    merged_trends.extend(trends)

    original_dict = {
        "data": merged_trends,
        "newspaper": newspaper_hot_trends,
        "google": trends
    }
    unique_data_list = []

    for item in original_dict["data"]:
        if isinstance(item, list):
            unique_data_list.extend(set(item))
        else:
            unique_data_list.append(item)

    keywords = list(set(unique_data_list))

    # Increment appearance count in the database and update cache
    current_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for keyword in keywords:
        cursor.execute('''
            INSERT OR IGNORE INTO keywords (keyword, created_at, updated_at) VALUES (?, ?, ?)
        ''', (keyword, current_time, current_time))
        cursor.execute('''
            UPDATE keywords SET appearances = appearances + 1, updated_at = ? WHERE keyword = ?
        ''', (current_time, keyword))
    conn.commit()

    # Retrieve updated keywords and appearances from the database
    cursor.execute('''
        SELECT keyword, appearances, created_at, updated_at FROM keywords
    ''')
    keyword_info = cursor.fetchall()
    # Prepare response with keywords, their appearances, created_at, and updated_at
    response_data = [{"keyword": info[0], "appearances": info[1], "created_at": info[2], "updated_at": info[3]} for info in keyword_info]

    cache["keywords"] = response_data

    return {"data": response_data}

# Start the cache for the Google News API
google_news_cache = TTLCache(maxsize=1000, ttl=6 * 60 * 60)

_ENCODED_URL_PREFIX = "https://news.google.com/rss/articles/"
_ENCODED_URL_PREFIX_WITH_CONSENT = "https://consent.google.com/m?continue=https://news.google.com/rss/articles/"
_ENCODED_URL_RE = re.compile(fr"^{re.escape(_ENCODED_URL_PREFIX_WITH_CONSENT)}(?P<encoded_url>[^?]+)")
_ENCODED_URL_RE = re.compile(fr"^{re.escape(_ENCODED_URL_PREFIX)}(?P<encoded_url>[^?]+)")
_DECODED_URL_RE = re.compile(rb'^\x08\x13".+?(?P<primary_url>http[^\xd2]+)\xd2\x01')

@functools.lru_cache(2048)
def _decode_google_news_url(url: str) -> str:
    match = _ENCODED_URL_RE.match(url)
    encoded_text = match.groupdict()["encoded_url"]  # type: ignore
    encoded_text += "==="  # Fix incorrect padding. Ref: https://stackoverflow.com/a/49459036/
    decoded_text = base64.urlsafe_b64decode(encoded_text)

    match = _DECODED_URL_RE.match(decoded_text)
    primary_url = match.groupdict()["primary_url"]  # type: ignore
    primary_url = primary_url.decode()
    return primary_url

def decode_google_news_url(url: str) -> str:
    return _decode_google_news_url(url) if url.startswith(_ENCODED_URL_PREFIX) else url

@router.post("/google/news/search")
async def root(google: GoogleAction):
    keyword = google.topic
    cached_result = google_news_cache.get(keyword)
    if cached_result:
        return {"data": cached_result}

    google_news = GNews()
    google_news.period = '1d'
    google_news.max_results = 30
    google_news.country = 'GB'
    results_dict = google_news.get_news(keyword)

    # Apply the clean_url function to each entry
    for entry in results_dict:
        entry["url"] = decode_google_news_url(entry.get("url", ""))

    google_news_cache[keyword] = results_dict
    return {"data": results_dict}

google_topic_cache = TTLCache(maxsize=1000, ttl=6 * 60 * 60)

# Topics available: WORLD, NATION, BUSINESS, TECHNOLOGY, ENTERTAINMENT, SPORTS, SCIENCE, HEALTH.
@router.post("/google/news/topic")
async def root(google: GoogleAction):
    cached_result = google_topic_cache.get(google.topic)
    if cached_result:
        return {"data": cached_result}
    google_news = GNews()
    google_news.period = '1d'
    google_news.max_results = 30
    google_news.country = 'United Kingdom'
    results_dict = google_news.get_news_by_topic(google.topic)
    for entry in results_dict:
        entry["url"] = decode_google_news_url(entry.get("url", ""))
    google_topic_cache[google.topic] = results_dict

    return {"data": results_dict}

import json
import newspaper
from fastapi import APIRouter, Path, Query, Depends
from pydantic import BaseModel
from cachetools import TTLCache
from pytrends.request import TrendReq
from gnews import GNews


pytrends = TrendReq(hl='en-GB', tz=360)

router = APIRouter()

google_topic_cache = TTLCache(maxsize=1000, ttl=6 * 60 * 60)


class GoogleAction(BaseModel):
    topic: str = Query(None, alias="item-query",
                       title="The topic to extract the news from: WORLD, NATION, BUSINESS, TECHNOLOGY, "
                             "ENTERTAINMENT, SPORTS, SCIENCE, HEALTH."),


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(MyJSONEncoder, self).default(obj)


trending_terms_cache = TTLCache(maxsize=1000, ttl=6 * 60 * 60)


@router.get("/trending-terms")
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

    # Store the keywords in the cache
    cache["keywords"] = keywords

    return {"data": keywords}


google_news_cache = TTLCache(maxsize=1000, ttl=6 * 60 * 60)


@router.post("/google-news-word")
async def root(google: GoogleAction):
    keyword = google.topic
    cached_result = google_news_cache.get(keyword)
    if cached_result:
        return {"data": cached_result}
    google_news = GNews()
    total_results = google_news.get_news(keyword)
    googlenews = GoogleNews(lang="en_gb", period='1d')
    googlenews.search(keyword)
    results = googlenews.results(sort=True)

    results_dict = json.loads(json.dumps(results, cls=CustomJsonEncoder))
    google_news_cache[keyword] = results_dict

    return {"data": total_results}


@router.post("/google-news-topic")
async def root(google: GoogleAction):
    cached_result = cache.get(google.topic)
    if cached_result:
        return {"data": cached_result}
    google_news = GNews()
    google_news.period = '1d'
    google_news.max_results = 30
    google_news.country = 'United Kingdom'
    results_dict = google_news.get_news(google.topic)
    cache[google.topic] = results_dict

    return {"data": results_dict}

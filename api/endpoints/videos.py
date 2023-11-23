from fastapi import APIRouter, Path, Query, Depends
from pydantic import BaseModel
from cachetools import TTLCache
from youtube_search import YoutubeSearch
from datetime import datetime, timedelta
from dateutil import parser, relativedelta


router = APIRouter()


class VideosAction(BaseModel):
    keyword: str


def parse_publish_time(publish_time):
    if "ago" in publish_time:
        words = publish_time.split()
        delta = int(words[0])
        if "years" in words:
            return (datetime.now() - timedelta(days=365 * delta)).strftime("%Y-%m-%d")
        elif "year" in words:
            return (datetime.now() - timedelta(days=365 * delta)).strftime("%Y-%m-%d")
        elif "month" in words:
            return (datetime.now() - timedelta(days=30 * delta)).strftime("%Y-%m-%d")
        elif "months" in words:
            return (datetime.now() - timedelta(days=30 * delta)).strftime("%Y-%m-%d")
        elif "week" in words:
            return (datetime.now() - timedelta(weeks=delta)).strftime("%Y-%m-%d")
        elif "weeks" in words:
            return (datetime.now() - timedelta(weeks=delta)).strftime("%Y-%m-%d")
        elif "day" in words:
            return (datetime.now() - timedelta(days=delta)).strftime("%Y-%m-%d")
        elif "days" in words:
            return (datetime.now() - timedelta(days=delta)).strftime("%Y-%m-%d")
    return parser.parse(publish_time)


@router.post("/videos/youtube")
async def root(post: VideosAction):
    results = YoutubeSearch(post.keyword, max_results=30).to_dict()

    # Extract the list of videos
    videos = results

    # Sort the videos by publish date in descending order
    sorted_videos = sorted(videos, key=lambda x: parse_publish_time(x['publish_time']), reverse=True)

    return {"data": {"search_terms": post.keyword, "max_results": 30, "videos": sorted_videos}}

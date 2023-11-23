from fastapi import APIRouter
from pydantic import BaseModel
import feedparser
from feedfinder2 import find_feeds
router = APIRouter()


class FeedReader(BaseModel):
    link: str


@router.post("/feed/reader")
async def root(feed: FeedReader):
    response = feedparser.parse(feed.link)
    return {"data": {
        "feed-link": feed.link,
        "response": {
            "title": response.feed.get('title', ''),
            "entries": response.entries
        },

    }}


@router.post("/feed/finder")
async def root(feed: FeedReader):
    response = find_feeds(feed.link)
    return {"data": {
        "feed-link": feed.link,
        "response": response,
    }}

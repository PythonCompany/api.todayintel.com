from fastapi import APIRouter, Path, Query, Depends
from pydantic import BaseModel
from cachetools import TTLCache

router = APIRouter()


class VideosAction(BaseModel):
    keyword: str


class TikTokAction(BaseModel):
    token: str


@router.post("/videos")
async def root(post: VideosAction):
    from youtube_search import YoutubeSearch
    results = YoutubeSearch(post.keyword, max_results=10)
    return {"data": results}


@router.post("/tiktok")
async def tiktok(post: TikTokAction):
    results = await get_hashtag_videos(post.token)
    return {"data": results}

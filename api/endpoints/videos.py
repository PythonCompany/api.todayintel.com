from fastapi import APIRouter, Path, Query, Depends
from pydantic import BaseModel
from cachetools import TTLCache

router = APIRouter()


class VideosAction(BaseModel):
    keyword: str


class TikTokAction(BaseModel):
    token: str


async def get_hashtag_videos(token):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=token, num_sessions=1, sleep_after=3)
        tag = api.hashtag(name="funny")
        return tag.videos(count=30)


@router.post("/videos")
async def root(post: VideosAction):
    from youtube_search import YoutubeSearch
    results = YoutubeSearch(post.keyword, max_results=10)
    return {"data": results}


@router.post("/tiktok")
async def tiktok(post: TikTokAction):
    results = await get_hashtag_videos(post.token)
    return {"data": results}

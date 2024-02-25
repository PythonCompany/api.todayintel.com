from fastapi import APIRouter, Path, Query, Depends
from pydantic import BaseModel
from cachetools import TTLCache
import spacy
import os
from newspaper import Config, Article
nlp = spacy.load("en_core_web_md")
router = APIRouter()
import requests
API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/e2fa0631e7c2fafc79e68a70a5968569/ai/run/"
headers = {"Authorization": "Bearer LIlFXCIYGIv1H_Z3h4EG2DYazo6s-EIXgW0DKKxR"}


class SeoPostGenerator(BaseModel):
    domainLink: str
    newsLink: str
    token: str
    model: str

@router.post("/social/generate")
async def root(generator: SeoPostGenerator):

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/50.0.2661.102 Safari/537.36 '
    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 10
    config.fetch_images = True
    config.memoize_articles = True
    config.follow_meta_refresh = True

    #Domain
    domain = Article(generator.domainLink, config=config, keep_article_html=True)
    domain.download()
    domain.parse()
    domain.nlp()

    #Article
    article =Article(generator.newsLink, config=config, keep_article_html=True)
    article.download()
    article.parse()
    article.nlp()

    combined = domain.summary + article.summary
    model = generator.model
    token = generator.token
    inputs = [
        {"role": "system", "content": "You are a friendly assistant that helps write social media posts"},
        {"role": "user", "content": "Write a short media post from this content:" + combined}
    ]

    headers = {"Authorization": "Bearer " + token}

    input = { "messages": inputs }

    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    print(response)
    cloudflare =  response.json()

    print(cloudflare)
    return {
        "data": {
            "summary_domain": domain.summary,
            "keywords_domain": domain.keywords,
            "summary_news": article.summary,
            "keywords_news": article.keywords,
            "combinedText": combined,
            "cloudflare": cloudflare
        }
    }

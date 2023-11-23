import asyncio

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware


from api.endpoints import feeds
from api.endpoints import scrapper
from api.endpoints import google
from api.endpoints import seo
from api.endpoints import nlp as nlp_endpoint

app = FastAPI(
    title="Today Intel",
    description="This is the api behind the Today Intel app.",
    version="1.1",
    terms_of_service="https://todayintel.com/terms/",
    contact={
        "name": "Stefan Laravel Developer",
        "url": "https://LzoMedia.com/",
        "email": "stefan@LzoMedia.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Endpoints
app.include_router(feeds.router)
app.include_router(scrapper.router)
app.include_router(google.router)
app.include_router(seo.router)
app.include_router(nlp_endpoint.router)


@app.get("/")
async def root():
    return {"data": "Welcome to the NLP API - for documentation please visit /docs for "}


if __name__ == "__main__":
    # Create and run the event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tiktok())

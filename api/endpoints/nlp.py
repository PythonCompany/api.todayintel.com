import spacy
import yake
import socials
import socid_extractor


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from markdownify import markdownify as md

from fastapi import APIRouter, Path, Query, Depends
from pydantic import BaseModel
from cachetools import TTLCache
from newspaper import Config, Article
from spacy import displacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English

router = APIRouter()

nlp = spacy.load("en_core_web_md")


class ArticleAction(BaseModel):
    link: str


class SummarizeAction(BaseModel):
    text: str


@router.post("/nlp/article")
async def root(article: ArticleAction):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/50.0.2661.102 Safari/537.36 '
    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 10
    config.fetch_images = True
    config.memoize_articles = True
    config.follow_meta_refresh = True
    crawler = Article(article.link, config=config, keep_article_html=True)
    crawler.download()
    crawler.parse()
    # Basic NLP using NTLK
    crawler.nlp()
    # New NLP
    doc = nlp(crawler.text)

    sentiment = SentimentIntensityAnalyzer()

    remove_entities = ["TIME", "DATE", "LANGUAGE", "PERCENT", "MONEY", "QUANTITY", "ORDINAL",
                       "CARDINAL"]

    entities = [(e.label_, e.text, e.start_char, e.end_char) for e in doc.ents]

    filtered_entities = [ent for ent in entities if ent[0] not in remove_entities]

    unique_values = set()

    filtered_entities_unique = [ent for ent in filtered_entities if
                                ent[1] not in unique_values and not unique_values.add(ent[1])]

    social = socials.extract(article.link).get_matches_per_platform()

    # List of entities to remove from the rendered HTML
    entities_to_remove = ["TIME", "DATE", "LANGUAGE", "PERCENT", "MONEY", "QUANTITY", "ORDINAL",
                          "CARDINAL"]

    # ...

    # Filter out entities to be removed
    filtered_entities_unique = [ent for ent in filtered_entities_unique if ent[1] not in entities_to_remove]

    # Render HTML with filtered entities
    spacy_html = displacy.render(doc, style="ent", options={"ents": [ent[0] for ent in filtered_entities_unique]})

    import socialshares
    counts = socialshares.fetch(article.link, ['facebook', 'pinterest', 'linkedin', 'google', 'reddit'])

    text = crawler.text
    language = "en"
    max_ngram_size = 1
    deduplication_threshold = 0.9
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=5,
                                                features=None)

    sorted_keyword = sorted_keywords = sorted(custom_kw_extractor.extract_keywords(text), key=lambda x: x[1], reverse=False)
    return {
        "data": {
            "title": crawler.title,
            "date": crawler.publish_date,
            "text": crawler.text,
            "markdown": md(crawler.article_html, newline_style="BACKSLASH", strip=['a'], heading_style="ATX"),
            "html": crawler.article_html,
            "summary": crawler.summary,
            "keywords":sorted_keywords,
            "authors": crawler.authors,
            "banner": crawler.top_image,
            "images": crawler.images,
            "entities": filtered_entities_unique,
            "videos": crawler.movies,
            "social": social,
            "spacy": spacy_html,
            "spacy_markdown": md(spacy_html, newline_style="BACKSLASH", strip=['a'],heading_style="ATX"),
            "sentiment": sentiment.polarity_scores(crawler.text),
            'accounts': socid_extractor.extract(crawler.text),
            'social-shares': counts
        },
    }


@router.post("/nlp/tags")
async def root(article: SummarizeAction):
    text = article.text
    language = "en"
    max_ngram_size = 3
    deduplication_threshold = 0.9
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,top=5, features=None)
    return {
        "data": custom_kw_extractor.extract_keywords(text)
    }

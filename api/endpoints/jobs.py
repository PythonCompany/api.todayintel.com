import logging
import json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
from jobspy import scrape_jobs

# Initialize logger
logger = logging.getLogger(__name__)

router = APIRouter()


class JobsSearch(BaseModel):
    keyword: str


@router.post("/jobs")
async def root(jobSearch: JobsSearch):
    try:
        jobs: pd.DataFrame = scrape_jobs(
            site_name=["indeed", "linkedin", "glassdoor"],
            search_term=jobSearch.keyword,
            description_format="html",
            location="United Kingdom",
            results_wanted=50,
            country_indeed="uk",
        )

        # Convert DataFrame to JSON, ignoring NaN and infinite values
        json_data = jobs.to_json(orient="records", date_format="iso", double_precision=10, force_ascii=False,
                                 date_unit="ms", default_handler=None)

        # Parse JSON data to Python dictionary
        python_dict = json.loads(json_data)

        return {
            "data": python_dict
        }
    except ValueError as e:
        # Handle ValueError (e.g., non-compliant float values)
        logger.error(f"ValueError: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # Handle other exceptions
        logger.error(f"Internal server error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

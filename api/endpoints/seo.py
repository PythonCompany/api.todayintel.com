from fastapi import APIRouter, Path, Query, Depends
from pydantic import BaseModel
from cachetools import TTLCache
import os
from seoanalyzer import analyze
from lighthouse import LighthouseRunner

router = APIRouter()


class SeoAnalise(BaseModel):
    link: str
    format: str


class LightHouseAction(BaseModel):
    link: str


@router.post("/seo/analyze")
async def root(data: SeoAnalise):
    import inspect
    module_path = os.path.dirname(inspect.getfile(analyze))
    response = analyze(data.link, follow_links=False, analyze_headings=True, analyze_extra_tags=True)
    if data.format == 'html':
        from jinja2 import Environment
        from jinja2 import FileSystemLoader
        env = Environment(loader=FileSystemLoader(os.path.join(module_path, 'templates')))
        template = env.get_template('index.html')
        output = template.render(result=response)
        return output
    else:
        output = response
        return {"data": output}


@router.post("/seo/lighthouse")
async def root(action: LightHouseAction):
    report = LighthouseRunner(action.link, form_factor='desktop', quiet=False, additional_settings=[]).report
    return {"data": report}

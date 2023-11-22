from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ScrapperAction(BaseModel):
    network: str
    what: str


@router.post("/run-scrapper")
def run_cli(scrapper: ScrapperAction):
    result = subprocess.run(['./skrapper/skraper ' + scrapper.network + ' ' + scrapper.what + ' -t json'],
                            capture_output=True, text=True, check=True)

    # Access the output of the command
    output = result.stdout
    return {"data": output}

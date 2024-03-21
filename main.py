from typing import List
import uvicorn
from fastapi import FastAPI, UploadFile, APIRouter, Depends, Header, HTTPException
from starlette.middleware.cors import CORSMiddleware

from jinja_process.cards_router import card_router
from jinja_process.examples_router import examples_router
from service import create_single_draft_test, create_single_draft

from config import settings


def check_api_key(api_key: str = Header(..., alias="X-API-KEY")):
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid api key.")
    return True


app = FastAPI(
    title="Service for wix block draft posts creating",
    docs_url="/bmxbikesworld/api/v1/docs",
    openapi_url="/bmxbikesworld/api/v1/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(
    prefix="/bmxbikesworld/api/v1",
    # dependencies=[Depends(check_api_key)]
)

examples = APIRouter(
    prefix="/examples",
    # dependencies=[Depends(check_api_key)]
)

examples.include_router(examples_router)


@router.post("/upload", response_model=None)
async def upload(files: List[UploadFile]):
    draft_posts_ids = []
    not_proc = []
    for file in files:
        try:
            result = await create_single_draft(file)
            print(result)
        except Exception as e:
            print(e)
            not_proc.append(file.filename)
        # draft_posts_ids.append(result["draftPost"]["id"])
    return not_proc


# @router.post("/test")
# async def test():
#     return await create_single_draft_test()

app.include_router(router)
app.include_router(examples)
app.include_router(card_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


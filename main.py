from typing import List
import uvicorn
from fastapi import FastAPI, UploadFile, APIRouter, Depends, Header, HTTPException
from starlette.middleware.cors import CORSMiddleware

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


@router.post("/upload", response_model=None)
async def upload(files: List[UploadFile]):
    draft_posts_ids = []
    for file in files:
        result = await create_single_draft(file)
        draft_posts_ids.append(result["draftPost"]["id"])
    return draft_posts_ids


@router.post("/test")
async def test():
    return await create_single_draft_test()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


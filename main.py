import uvicorn
from fastapi import FastAPI, UploadFile


app = FastAPI()


@app.post("/upload")
async def upload(file: UploadFile):
    content = await file.read()
    return {"filename": file.filename, "content": content}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


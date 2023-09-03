from fastapi import FastAPI

from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/ping")
async def ping():
    pass

@app.get("/files/{filename}")
async def file(filename):
    return FileResponse(f'files/{filename}')
from fastapi import FastAPI

app = FastAPI()

import time
@app.get("/sync")
def read_sync():
    time.sleep(2)
    return {"message": "Synchronous blocking endpoint"}

import asyncio
@app.get("/async")
async def read_async():
    await asyncio.sleep(2)
    return {"message": "Asyncing non-blocking endpoint"}
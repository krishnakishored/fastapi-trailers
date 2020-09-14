from fastapi import FastAPI 

from app.api import ping
from app.db import engine, metadata, database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

#wire the router to the main app
app.include_router(ping.router)


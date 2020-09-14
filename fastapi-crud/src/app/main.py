from fastapi import FastAPI 

from app.api import ping, notes
from app.db import engine, metadata, database

metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

#wire the router to the main app
app.include_router(ping.router)
# Take note of the prefix URL along with the "notes" tag, 
# which will be applied to the OpenAPI schema (for grouping operations).
app.include_router(notes.router, prefix="/notes", tags=["notes"])

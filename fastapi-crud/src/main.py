from fastapi import BackgroundTasks, Body, FastAPI, Query

from config import Settings, get_settings

settings: Settings = get_settings()

# from app.api import notes, ping
# from app.db import database, engine, metadata
# metadata.create_all(engine)

from typing import Optional

from pydantic import BaseModel

from db import models
from db.database import get_db_engine, get_db_tables

# tags_metadata = [
#     {
#     }
# ]
app = FastAPI(
    title="FastAPI-CRUD",
    description="A sample FastAPI application that does CRUD operations",
    version="1.0.0.0",
    servers=[
        {
            "url": f"http://localhost:{settings.PORT}",
            "description": "Local environment",
        },
    ],
    # openapi_tags=tags_metadata,
)


@app.post("/databases")
def create_database(
    db_name: str = Body(..., embed=True),
):
    # TODO: error handling - failure to create DB
    engine = get_db_engine(db_name=db_name, create_db=True)
    if engine is not None:
        return {"status": "OK", "message": f"database:{db_name} is created"}

    else:
        return {"status": "NOT OK", "message": f"database:{db_name} is not created"}


@app.get("/databases")
def get_database_list(
    # Query
):
    list_of_databases = []
    return {"list_of_databases": list_of_databases}


@app.post("/tables")
def create_tables(
    background_tasks: BackgroundTasks,
    db_name: str = Body(..., embed=True),
):
    engine = get_db_engine(db_name=db_name, create_db=False)
    if engine is not None:
        models.Base.metadata.create_all(engine)
        # background_tasks.add_task(models.Base.metadata.create_all, engine)
        return {"status": "OK", "message": f"table creation started in db:{db_name}"}
    else:
        return {"status": "OK", "message": f"Failed to create tables in db:{db_name}"}
    # return {"status": "OK", "service": app.title, "version": app.version}


@app.get("/tables")
def get_table_list(
    db_name: str = Query("fastapi_crud", description="database name"),
):
    ## TODO: handle db_name invalid
    list_of_tables = get_db_tables(db_name)
    return {"database": db_name, "list_of_tables": list_of_tables}


@app.get("/status")
def status():
    return {"status": "OK", "service": app.title, "version": app.version}


# @app.on_event("startup")
# async def startup():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()

# wire the router to the main app
# app.include_router(ping.router)
# # Take note of the prefix URL along with the "notes" tag,
# # which will be applied to the OpenAPI schema (for grouping operations).
# app.include_router(notes.router, prefix="/notes", tags=["notes"])


if __name__ == "__main__":
    import uvicorn

    # TODO: read the app version
    # print(settings.dict().keys())
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )

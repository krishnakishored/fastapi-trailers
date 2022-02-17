from os import path, sys
from typing import Optional

from celery.result import AsyncResult
from fastapi import Body, FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

import tasks

sys.path.append(path.dirname(path.abspath(__file__)))

app = FastAPI(
    title="TASKER",
    description="App that makes use of celery to run tasks",
    version="1.0.0.0",
    servers=[
        {"url": "http://localhost:40008", "description": "Local environment"},
    ],
    # openapi_tags=tags_metadata,
    # exception_handlers={
    #     # RequestValidationError: request_validation_exception_handler,
    # }
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/status")
async def status():
    return {"status": "OK", "service": app.title, "version": app.version}


class AdditionTask(BaseModel):
    a: int = Field(5, title="first number")
    b: int = Field(10, title="second number")


class CrontabModel(BaseModel):
    minute: str = "*"
    hour: str = "*"
    day_of_week: str = "*"
    day_of_month: str = "*"
    month_of_year: str = "*"


@app.post("/periodictask")
async def run_periodic_task(crontab: CrontabModel = Body(..., embed=True)):
    # periodic_task_key = tasks.setup_periodic_task(**crontab.__dict__)
    periodic_task_key = tasks.setup_periodic_task()
    # print(f"task created:{current_task.id}")
    # return JSONResponse({"task": task.get()})
    # return JSONResponse({"task_id": current_task})
    return {"periodic_task_key": periodic_task_key}


@app.post("/task")
async def run_task(
    delay: Optional[int] = Query(5, description="Default delay is 5 seconds"),
    numbers: AdditionTask = Body(..., embed=True),
):
    # current_task = tasks.delayed_addition.delay(delay, numbers.a, numbers.b)
    current_task = tasks.delayed_addition.apply_async((delay, numbers.a, numbers.b))
    # current_task = tasks.delayed_addition.apply_async(
    #     (delay, numbers.a, numbers.b), queue="lopri", countdown=10
    # )
    # add.apply_async((2, 2), queue="lopri", countdown=10)
    print(f"task created:{current_task.id}")
    # return JSONResponse({"task": task.get()})
    return JSONResponse({"task_id": current_task.id})


@app.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return JSONResponse(result)


if __name__ == "__main__":
    import uvicorn

    from config import Settings, get_settings

    settings: Settings = get_settings()
    # TODO: read the app version
    # print(f"Running the version:{settings.APP_VERSION}")
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.TASKER_PORT,
    )

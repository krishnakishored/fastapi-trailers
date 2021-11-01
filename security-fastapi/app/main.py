from fastapi import FastAPI
from routes.user import router as user_router

app = FastAPI()


app.include_router(user_router, prefix="")


if __name__ == "__main__":
    import uvicorn

    # TODO: read the app version
    # print(f"Running the version:{settings.APP_VERSION}")
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        reload=True,
        port=7622,
    )

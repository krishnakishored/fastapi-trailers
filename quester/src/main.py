from fastapi import FastAPI

# TODO: from fastapi.middleware.gzip import GZipMiddleware
## enable 'CORSMiddleware' to test using the swagger spec
from fastapi.middleware.cors import CORSMiddleware

from api import search_api
from clients.aiohttp_session import SingletonAiohttp
from common.middlewares import add_security_headers
from config import Settings, get_settings

settings: Settings = get_settings()

tags_metadata = [
    {
        "name": "Search",
        "description": "The Search API enables proximity search on free-form"
        + "text for Points of Interest (POI), Businesses, and addresses."
        + "Results are ranked by relevance based on text pattern match and "
        + "distance from the specified search_center, offering comprehensive"
        + " location-based search capabilities. It supersedes the geocode API "
        + "with expanded features.",
    },
]
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    servers=[
        {
            "url": f"http://{settings.HOST}:{settings.PORT}",
            "description": "Local",
        },
        # {
        #     "url": "https://api.webmapping.com/v1/quester",
        #     "description": "Production environment",
        # },
    ],
    openapi_tags=tags_metadata,
    # No custom exception handlers are used as of now
    # exception_handlers= {
    #     # QuesterBaseError: quester_exception_handler
    #     #     # RequestValidationError: request_validation_exception_handler,
    # },
)

# Add custom middlewares that apply to all APIRouter instances
##############################################################################

# app.middleware("http")(request_response_logger)
# app.add_middleware(GZipMiddleware, minimum_size=500) # TODO
# enable this only for debugging
# app.middleware("http")(add_process_time_header)

"""
# to show swagger-spec: disable - 'add_security_headers' middleware
# while running locally @ http://localhost:7600/docs
# to test via swagger-spec: enable -'CORSMiddleware' for testing via swagger
"""
#####
# app.middleware("http")(add_security_headers)
#####
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
################################################################################


@app.on_event("startup")
async def startup_event():
    ## gRPCClient instance is not created per request now
    # get_nws_grpc_client()
    SingletonAiohttp.get_aiohttp_client()


@app.on_event("shutdown")
async def shutdown_event():
    # close_nws_grpc_client()
    await SingletonAiohttp.close_aiohttp_client()


@app.get("/status")
async def status():
    return {"status": "OK", "service": app.title, "version": app.version}


app.include_router(search_api.router, tags=["Search"])
# ,dependencies=[Depends(logging_dependency)])


if __name__ == "__main__":
    import uvicorn

    print(f"Running the version:{settings.APP_VERSION}")
    print(f"quester is running on {settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG_MODE,
    )

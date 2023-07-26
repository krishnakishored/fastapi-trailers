from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from common.exceptions import QuesterBadRequestError
from common.logger import get_logger
from common.utilities import is_valid_lat_lon, retrieve_lat_lon, string_pruner
from config import Settings, get_settings
from drivers.search_driver import search_core

settings: Settings = get_settings()
router = APIRouter()
logger = get_logger(__name__, log_type="json")


@router.get("/search", status_code=200, dependencies=[])
async def search(
    api_key: str = Query(..., description="APIKEY", example="SampleAPIKey"),
    search_center: str = Query(
        ...,
        description="comma separated - lat,lon string ",
        example="33.663664, -117.9195484",
    ),
    query: Optional[str] = Query(
        None,
        description="Freeform text query for the search",
        example="Anaheim",
    ),
    place_id: Optional[str] = Query(
        None, description="Unique Identifier to retrieve the place"
    ),
    iterator_length: Optional[int] = Query(
        10,
        description="Number of matching records in the resu. Default is 10",
    ),
):
    # # TODO: log the request using Depends or middleware

    # trim the string of unwanted characters
    query = string_pruner(query) if query is not None else ""
    response = {}
    if not query and not place_id:
        logger.error("query or place_id must be provided")
        raise HTTPException(
            status_code=400, detail="query or place_id must be provided"
        )

    if query and place_id:
        error_message = "only one of query or place_id must be provided"
        logger.error(error_message)
        raise HTTPException(status_code=400, detail=error_message)
    try:
        # TODO: allow (lal,lon) search from the same search bar
        if is_valid_lat_lon(str(search_center)):
            #  if query param looks like a valid lat,lon invoke reverseGeocode
            # named_road is set to 'True' by default
            #   - house number & street will be part of the formatted address
            # language is set to 'en' by default
            response = await search_core(
                lat_lon_string=search_center,
                search_term=query if query else place_id,
                iterator_length=iterator_length,
            )
    except (QuesterBadRequestError, ValueError, LookupError) as error:
        logger.exception(error)
        raise HTTPException(status_code=400, detail=str(error))
    else:
        return response

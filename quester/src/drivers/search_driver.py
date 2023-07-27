import json

from clients.aiohttp_request_handler import (
    AioHttpGetData,
    fetch_aiohttp_results,
)
from clients.solr_client import SolrQueryBuilder


async def search_core(
    lat_lon: str,
    search_term: str,
    resp_max_limit: int,
    # country: str = "USA",
):
    """_summary_
    1. builds solr_query_url for multiple collections
    2. Asynchronous make the multiple search requests
    3. Await for all the results
    4. Merge them in the response object & return it

    Args:
        lat_lon (str): _description_
        search_term (str): _description_
        resp_max_limit (int): _description_

    Returns:
        _type_: _description_
    """

    query_builder = SolrQueryBuilder()
    collection_names = ["usa_csz"]
    solr_query_list = []
    req_obj_list = []
    for collection_name in collection_names:
        # Set the base URL and collection name
        query_builder.with_collection(collection_name)
        solr_query_list.append(
            query_builder.spatial_search(
                search_term=f":{search_term}",
                lat_lon=lat_lon,
                # set the radius parameter to exclude distance limitation for CSZ
                spatial_field="centroid",
                resp_max_limit=resp_max_limit,
                radius_in_km=5000,  # max radial distance for CSZ search
            )
        )

    for solr_query_url in solr_query_list:
        req_obj_list.append(AioHttpGetData(url=solr_query_url))

    result_raw = await fetch_aiohttp_results(
        verb="GET", req_obj_list=req_obj_list
    )
    print(result_raw)
    # TODO: response formatter
    return result_raw

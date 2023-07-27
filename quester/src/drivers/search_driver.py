import json

from clients.aiohttp_request_handler import (
    AioHttpGetData,
    fetch_aiohttp_results,
)
from clients.solr_client import SolrQueryBuilder
from common.utilities import full_address_formatter
from schemas import Location


def convert_solr_result_to_search_resp(solr_reply: dict, lat_lon_input: str):
    """Convert SOLR Record to reverse geocode reply

    Args:
        solr_reply (dict): [description]
        lat_lon_input (str): comma separated latititde and longitude

    Returns:
        results_solr: formatted as reverse_geocode response

    """
    results_solr = {}
    places = []
    place = {}
    results_solr["places"] = places

    if not solr_reply or "response" not in solr_reply:
        # log No reply from SOLR
        return results_solr

    for solr_record in solr_reply["response"]["docs"]:
        # location = {}
        place = {}
        place["location"] = solr_record
        places.append(place)

    # solr_locations_map = {
    #     "country": "country_code",
    #     "state": "state_code",
    #     "city": "city",
    #     "street1": "street",
    #     "zip": "postal",
    # }

    # for solr_record in solr_reply["response"]["docs"]:
    #     location = {}
    #     for key, val in solr_locations_map.items():
    #         location[val] = solr_record[key]
    #     location["coordinates"] = [
    #         {
    #             "latitude": solr_record["lat"],
    #             "longitude": solr_record["lon"],
    #             "type": "display_point",  # always display_point
    #         }
    #     ]
    #     location["house_number"] = solr_record.get("streetnum")
    #     # ToDo: lookup the country_name from country_code
    #     location[
    #         "country_name"
    #     ] = "United States of America"  # hardcoded to USA for now

    #     # Each solr_record represents an address_point_id. If there are
    #     # more than site_record for an address_point_id, return all
    #     for solr_site in solr_record["ddti_pairs"]:
    #         site_record = json.loads(solr_site)
    #         site_unique_id = list(site_record.keys())[0]
    #         enhanced_contents = {}
    #         # enhanced_contents['site_unique_id'] = site_unique_id
    #         for k, v in site_record[site_unique_id].items():
    #             if not v.strip():
    #                 continue
    #             if k.strip() == "streetnum" and v.strip != "0":
    #                 location["house_number"] = v.strip()
    #             else:
    #                 enhanced_contents[k] = v.strip()

    #         place = {}
    #         location["formatted_address"] = full_address_formatter(
    #             location.get("house_number", ""),
    #             location.get("street", ""),
    #             location.get("intersection", ""),
    #             location.get("city", ""),
    #             location.get("state_code", ""),
    #             location.get("postal", ""),
    #             location.get("country_code", ""),
    #         )

    #         # SOLR may or may not return the following fields in response
    #         optional_fields_mapping = {
    #             "municipality": "municipality",
    #             "landmark": "landmark",
    #             "building": "building",
    #             "floor": "floor",
    #             # "unit":"unit"
    #         }

    #         for key, value in optional_fields_mapping.items():
    #             if key in solr_record.keys():
    #                 location[value] = solr_record.get(key, "")

    #         location["unit"] = site_record[site_unique_id].get("unit", "")
    #         place["result_type"] = "point_address"  # always point_address
    #         place["place_id"] = "PA:" + solr_record["searchable_ids"][0]
    #         place["site_id"] = site_unique_id

    #         place["location"] = location.copy()
    #         places.append(place)

    results_solr["places"] = places
    return results_solr


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
    solr_req_list = []
    for collection_name in collection_names:
        # Set the base URL and collection name
        # query_builder.with_collection(collection_name)
        solr_req_url = query_builder.with_collection(
            collection_name
        ).spatial_search(
            search_term=f"place:{search_term}",
            lat_lon=lat_lon,
            # set the radius parameter to exclude distance limitation for CSZ
            spatial_field="centroid",
            resp_max_limit=resp_max_limit,
            radius_in_km=5000,  # max radial distance for CSZ search
        )
        solr_req_list.append(AioHttpGetData(url=solr_req_url))

    # for solr_query_url in solr_query_list:
    #     req_obj_list.append(AioHttpGetData(url=solr_query_url))

    result_raw = await fetch_aiohttp_results(
        verb="GET", req_obj_list=solr_req_list
    )
    # Convert bytes to string & parse JSON string to dict
    result_list = [json.loads(data.decode("utf-8")) for data in result_raw]
    # TODO: response formatter
    response_list = []
    for solr_reply in result_list:
        response_list.append(
            convert_solr_result_to_search_resp(
                solr_reply=solr_reply, lat_lon_input=lat_lon
            )
        )
    # TODO: merge the responses
    return response_list

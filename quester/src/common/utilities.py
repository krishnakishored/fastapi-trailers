# from pathlib import Path
from math import atan2, cos, radians, sin, sqrt

from fastapi import Request

from common.exceptions import QuesterBadRequestError
from common.logger import get_logger
from config import Settings, get_settings

logger = get_logger(__name__, log_type="json")


settings: Settings = get_settings()


async def log_request_body(request: Request):
    """Use this for HTTP POST requests"""
    request_body = await request.json()
    logger.info(request_body)


def retrieve_lat_lon(lat_lon_string: str):
    """retrieves latitude & longitude

    validates:
        - to have , separator
        - to have 2 vals (must be floats)
        - valid lat/lon range

    Args:
        lat_lon_string (str): comma separated lat and lon as a single string

    Raises:
        QuesterBadRequestError: [description]

    Returns:
        str,str: latitude,longitude
    """
    try:
        lat, lon = lat_lon_string.split(",", 1)  # should have only two parts
        f_lat = float(lat.strip())
        f_lon = float(lon.strip())
    except (ValueError, AttributeError) as error:
        logger.debug(error)
        # To suppress chaining, use raise from None
        # Avoid - "During handling of the above exception,
        # another exception occurred:"
        #
        raise QuesterBadRequestError(
            "Invalid latitude/longitude received"
        ) from None
    # validate the range
    if f_lat > 90 or f_lat < -90:
        raise QuesterBadRequestError(
            f"latitude out of range: {f_lat}"
        ) from None
    if f_lon > 180 or f_lon < -180:
        raise QuesterBadRequestError(
            f"longitude out of range: {f_lon}"
        ) from None
    return lat.strip(), lon.strip()


def string_pruner(value: str) -> str:
    """Trims the passed value.

    1. Removes the trailing and leading spaces.
    2. Removes unwanted characters from the end.

    Args:
        value (str): The string to be pruned.

    Returns:
        str: The pruned value.
    """
    # TODO: more characters to trim shall be added later
    chars_to_discard = "\\"
    pruned_value = value.strip().rstrip(chars_to_discard).strip()
    return pruned_value


def is_valid_lat_lon(lat_lon_string: str) -> bool:
    """A wrapper function to check the validity of lat,lon"""

    try:
        lat, lon = retrieve_lat_lon(lat_lon_string)
        # logger.debug(f"valid lat,lon:({lat},{lon})")
        return True
    except (ValueError, TypeError) as error:
        logger.error(f"Invalid lat, lon: {error}")
        return False


def line_of_sight_distance(lat_lon_1, lat_lon_2):
    # approximate radius of Earth in meters
    R = 6378137
    lat1, lon1 = retrieve_lat_lon(lat_lon_1)
    lat2, lon2 = retrieve_lat_lon(lat_lon_2)
    # convert degrees to radians
    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))
    # using Haversine formula to calculate distance
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance


def full_address_formatter(
    streetnum=None,
    street1=None,
    xstreet=None,
    city=None,
    state=None,
    postal=None,
    country_code="USA",
    area_name=None,
):
    formatted_address = ""

    if area_name:
        # Area matches have no street info
        formatted_address = area_name + ", "
    else:
        # Street Address
        if streetnum:
            formatted_address += str(streetnum) + " "

        if xstreet and street1:
            formatted_address += str(street1) + " & " + str(xstreet) + ", "
        elif street1:
            formatted_address += str(street1) + ", "

    formatted_address += f"{city}, {state} {postal}, {country_code}"
    return formatted_address

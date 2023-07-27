from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class Coordinate(BaseModel):
    latitude: float = Field(..., description="Latitude of the address")
    longitude: float = Field(..., description="Longitude of the address")
    type: str = Field(
        ...,
        enum=[
            "interpolated_point",
            "street_point",
            "display_point",
            "route_point",
            "polygon_point",
        ],
        description="Type of the coordinate",
    )


class ResultType(str, Enum):
    poi = Field(
        "poi", description="Points Of Interest (POI) or Business result"
    )
    street = Field("street", description="Street address result")
    point_address = Field("point_address", description="Address point result")
    intersection = Field("intersection", description="Intersection result")
    region = Field(
        "region",
        description="Administrative area result. Eg city, state, postal etc",
    )
    polygon = Field(
        "polygon",
        description="Polygon based result. Eg Pacific Ocean, Irvine Lake etc",
    )
    category = Field(
        "category",
        description="Category result. Eg pizza, coffee shops. Used only for suggestions",
    )
    brand = Field(
        "brand",
        description="Brand result. Eg Starbucks, Chase Bank. Used only for suggestions",
    )


class Location(BaseModel):
    house_number: str = Field(
        ...,
        description="The house number of the address. This can be interpolated number based on a street number range or a precise number based on point address",
    )
    street: str = Field(..., description="Name of the street")
    intersection: str = Field(
        ...,
        description="Name of the intersecting street for intersection based results",
    )
    city: str = Field(..., description="City name or the primary locality")
    postal: str = Field(
        ..., description="Postal code used in the postal address of the place"
    )
    state_code: str = Field(..., description="State code")
    state_name: str = Field(..., description="State name")
    country_code: str = Field(
        ..., description="The ISO 3166-1 three character country code"
    )
    country_name: str = Field(
        ..., description="Localized country name used for display"
    )
    area_name: str = Field(..., description="Name of the polygon")
    formatted_address: str = Field(
        ...,
        description="One line string containing human readable localized address of the place",
    )
    coordinates: List[Coordinate] = Field(
        ...,
        description="Array of one or more coordinates associated with the place where each item in the array represents a unique type of coordinate",
    )
    unit: str = Field(
        ...,
        description="Unit or suite number associated with the house_number",
    )
    floor: str = Field(..., description="Floor associated with the address")
    building: str = Field(
        ..., description="Building associated with the address"
    )
    landmark: str = Field(
        ..., description="Landmark name associated with the address"
    )
    neighborhood: str = Field(
        ..., description="Neighbourhood where the address is located"
    )
    municipality: str = Field(
        ..., description="Municipality where the address is located"
    )


class Place(BaseModel):
    result_type: ResultType = Field(...)  # required field
    distance: float = Field(
        ...,
        description="distance from the search_center in meters",
        example=121.8,
    )
    location: Location = Field(...)
    name: str = Field(
        description="Display name of the result. Used only for POI result_type",
        example="KFC",
    )
    place_id: str = Field(
        description="Unique identifier of the place. Used only when the place is a POI or address point",
        example="123456789",
    )
    # site_id: str = Field(description="Unique identifier for the site. This is used only only when a place has more than one site")
    accuracy: int = Field(
        ...,
        description="Accuracy of the match compared to the input query. Possible values are 1 to 10 where 10 is the highest",
        ge=0,
        le=10,
        example=9,
    )


class PlacesResponse(BaseModel):
    places: List[Place]

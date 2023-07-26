# Quester

## APIs

1. search API (Geocode)

   - search_center: str (lat,lon)
   - query: str
   - Convert it to a solr req object
   - It makes parallel requests to solr(multiple cores)
   - Define the model for response
   - Define the sort order of the responses from each solr request.
   - Discard the records with low scores
   - Configurable to limit of geo-distance (set to a default, if it's not set)

1. Suggestions API
1. Select API
1. reverseGeocode API

## Query Parser

1. Parse the query string to extract the fields to be passed to the solr requests
1. Differentiate - house no, street/road, city, state, country
1. Constraints - follow the order of addressing

## SOLR-Client

1. create a class to build solr request

## Scoring

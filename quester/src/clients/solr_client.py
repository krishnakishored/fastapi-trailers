from config import Settings, get_settings

settings: Settings = get_settings()


class SolrQueryBuilder:
    def __init__(self):
        self.base_url = settings.SOLR_BASE_URL
        self.collection_name = ""
        self.exclude_chars = ":()"

        # default query_params - TODO: build a config based on collection_name
        self.query_params = {"q.op": "OR", "wt": "json"}

    def with_base_url(self, base_url):
        self.base_url = base_url.rstrip("/")
        return self

    def with_collection(self, collection_name):
        self.collection_name = collection_name
        return self

    def with_query_param(self, name, value):
        self.query_params[name] = value
        return self

    def build_select_query(self):
        from urllib.parse import urlencode

        base_query_url = f"{self.base_url}/solr/{self.collection_name}/select?"
        encoded_params = urlencode(self.query_params, safe=self.exclude_chars)
        query = base_query_url + encoded_params
        return query

    def spatial_search(
        self,
        search_term: str,
        lat_lon: str,
        radius_in_km: float,
        resp_max_limit: int = 10,
        spatial_field: str = "centroid",
    ):
        self.with_query_param("q", search_term)
        self.with_query_param("pt", lat_lon)
        self.with_query_param("sfield", spatial_field)
        self.with_query_param("rows", resp_max_limit)
        self.with_query_param("d", radius_in_km)
        ## TODO: build a config based on collection_name
        self.with_query_param("fq", "{!geofilt}")
        self.with_query_param("fl", "*,score,distance:geodist()")
        self.with_query_param("sort", "geodist() asc")

        return self.build_select_query()

    def auto_suggest(self, query):
        self.with_query_param("suggest", "true")
        self.with_query_param("suggest.dictionary", "mySuggester")
        self.with_query_param("suggest.q", query)
        self.with_query_param("suggest.count", 10)
        return self.build_select_query()


if __name__ == "__main__":
    # Create an instance of SolrQueryBuilder
    query_builder = SolrQueryBuilder()
    collection_name = "usa_csz"

    # Set the base URL and collection name
    # query_builder.with_base_url(settings.SOLR_BASE_URL).with_collection(
    #     collection_name
    # )
    query_builder.with_collection(collection_name)

    # Build a spatial search query
    spatial_query = query_builder.spatial_search(
        search_term="place:Grove",
        lat_lon="33.663664, -117.9195484",
        radius_in_km=100,
    )
    print(f"Spatial Query: {spatial_query}")

    # # Build an auto-suggest query
    # suggest_query = query_builder.auto_suggest("search query")
    # print(f"Auto-Suggest Query: {suggest_query}")

async def search_core(
    lat_lon_string: str,
    search_term: str,
    iterator_length: int,
    # country: str = "USA",
):
    return {
        "lat_lon_string": lat_lon_string,
        "search_term": search_term,
        "iterator_length": iterator_length,
    }

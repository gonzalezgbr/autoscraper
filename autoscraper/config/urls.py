class UrlBuilder:
    """Arma los distintos tipos de url usadas por el scraper."""

    def __init__(self):
        self._BASE_URL = 'https://www.hiperlibertad.com.ar/'
        self._STORES_URL = 'files/fit-institucional-sucursales.js'
        self._PRODUCT_BASE_URL = 'api/catalog_system/pub/products/search'
        self._CATEGORIES_URL = 'api/catalog_system/pub/facets/search?ft'

    def build_store_url(self) -> str:
        """Devuelve url para scrapear sucursales."""

        return self._BASE_URL + self._STORES_URL

    def build_categories_url(self):
        """Devuelve url para scrapear categorías."""

        return self._BASE_URL + self._CATEGORIES_URL

    def build_product_url(self, start: int, subcategory_link: str, store: int) -> str:
        """Devuelve url para scrapear productos por subcategoría."""
        # ej:tecnologia/tv-y-video?O=OrderByTopSaleDESC&_from=0&_to=49&ft&sc=12
        # La api permite como max. 50 productos por request.
        end = start + 49
        search_url = f'?O=OrderByTopSaleDESC&_from={start}&_to={end}&ft&sc={store}'

        return self._BASE_URL + self._PRODUCT_BASE_URL + subcategory_link + search_url

class UrlBuilder:
    """Arma los distintos tipos de url usadas por el scraper."""

    def __init__(self):
        self._BASE_URL = 'https://www.hiperlibertad.com.ar/'
        self._STORES_URL = 'files/fit-institucional-sucursales.js'
        self._PRODUCT_BASE_URL = 'api/catalog_system/pub/products/search'
        #tecnologia/tv-y-video?O=OrderByTopSaleDESC&_from=0&_to=49&ft&sc=12
        self._CATEGORIES_URL = 'api/catalog_system/pub/facets/search?category:"all"'

    def build_categories_url(self):
        """Devuelve url para scrapear categorías."""

        return self._BASE_URL + self._CATEGORIES_URL

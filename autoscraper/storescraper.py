import json

import requests

from config.urls import UrlBuilder
from models import Store


class StoreScraper:

    def __init__(self):
        self._url_builder = UrlBuilder()

    def parse_stores(self, text: str) -> list[Store]:
        """Parsea los datos de las sucursales."""
        start = text.find('{"states"')
        end = text.find('\'', start)
        stores_data = json.loads(text[start:end])['stores']
        stores = []
        for store in stores_data:
            if store['ecommerce']:
                stores.append(Store(
                    name=store['name'].encode('latin-1').decode(),
                    sc=store['sc']))
        return stores

    def get_stores(self) -> list[Store]:
        """Descarga y persiste el listado de sucursales disponibles"""
        url = self._url_builder.build_store_url()
        r = requests.get(url, timeout=10)
        stores = self.parse_stores(r.text)

        return stores

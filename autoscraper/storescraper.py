import json
import sys

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
        """Descarga el listado de sucursales disponibles"""
        url = self._url_builder.build_store_url()
        try:
            r = requests.get(url, timeout=10)
            stores = self.parse_stores(r.text)
        except requests.exceptions.RequestException as e:
            print(f'ERROR: no se pudo realizar la descarga {e}')
            sys.exit(1)
        except json.decoder.JSONDecodeError as e:
            print(f'ERROR: json descargado inválido {e}')
            sys.exit(1)

        return stores

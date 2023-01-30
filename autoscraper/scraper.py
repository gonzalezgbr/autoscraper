import json

import requests

from config.stores import STORES
from config.urls import UrlBuilder
from models import Category


class Scraper:
    """Descarga los datos de categorías y productos de una sucursal."""

    def __init__(self, store_name: str):
        self._store_name = store_name
        self._store = STORES[store_name]
        self._url_builder = UrlBuilder()

    def parse_categories(self, text: str) -> list[Category]:
        """Devuelve categorías extraídas del json descargado."""
        categories_data_list = json.loads(text)['CategoriesTrees']
        categories = []
        for category_data in categories_data_list:
            category = Category(category_data['Name'])
            # Hay 3 niveles max. de categorías, pero los productos se pueden
            # consultar por la categoría intermedia. Por ej, Electrodomésticos
            # > Pequeños electrodomésticos para traer Pava Eléctrica, Batidoras
            for child in category_data['Children']:
                category.add_subcategory(child['Name'], child['Link'])
            categories.append(category)

        return categories

    def get_categories(self) -> list[Category]:
        """Descarga todas las categorías de productos disponibles."""

        categories_url = self._url_builder.build_categories_url()
        # TODO: agregar headers
        r = requests.get(categories_url, timeout=10)
        categories = self.parse_categories(r.text)

        return categories

import json
import sys

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from models import Category, Store, SubCategory
from config.urls import UrlBuilder


class CategoryScraper:

    def __init__(self, store: Store):
        self._store_name = store.name
        self._store = store.sc
        self._url_builder = UrlBuilder()

    def get_subcategories(self, category: Category):

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            url = self._url_builder.build_category_url(category.link, self._store)
            page.goto(url)
            page.wait_for_timeout(2000)
            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, 'html.parser')
        links = soup.select('a[class*="styles__LinkImage"]')
        subcategories = []
        for link in links:
            subcategories.append(SubCategory(link.attrs['href']))

        return subcategories

    def parse_categories(self, text: str) -> list[Category]:
        """Devuelve categorías extraídas del json descargado."""
        categories_data_list = json.loads(text)['CategoriesTrees']
        categories = []
        for category_data in categories_data_list:
            if len(categories) % 4 == 0:
                print('...')
            category = Category(category_data['Name'], category_data['Link'])
            # Hay 3 niveles max. de categorías, pero los productos se pueden
            # consultar por la categoría intermedia. Por ej, Electrodomésticos
            # > Pequeños electrodomésticos para traer Pava Eléctrica, Batidoras, etc.
            subcategories = self.get_subcategories(category)
            category.add_subcategories(subcategories)

            categories.append(category)

        return categories

    def get_categories(self) -> list[Category]:
        """Descarga todas las categorías de productos disponibles."""

        categories_url = self._url_builder.build_categories_url()
        try:
            r = requests.get(categories_url, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f'ERROR: no se pudo realizar la descarga {e}')
            sys.exit(1)
        except json.decoder.JSONDecodeError as e:
            print(f'ERROR: json descargado inválido {e}')
            sys.exit(1)
        categories = self.parse_categories(r.text)

        return categories

import json
import sys

import asyncio
import requests
from pyppeteer import launch
from bs4 import BeautifulSoup

from models import Category, Store, SubCategory
from config.urls import UrlBuilder


class CategoryScraper:

    def __init__(self, store: Store):
        self._store_name = store.name
        self._store = store.sc
        self._url_builder = UrlBuilder()

    async def get_subcategories(self, category: Category):
        """Descarga las subcategorías de una categoría y una sucursal."""
        browser = await launch({"headless": True})
        page = await browser.newPage()
        url = self._url_builder.build_category_url(category.link, self._store)

        await page.goto(url)
        await page.waitForSelector("a.category-name", visible=True)
        html = await page.content()
        await browser.close()

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
            category = Category(category_data['Name'], category_data['Link'])
            # Hay 3 niveles max. de categorías, pero los productos se pueden
            # consultar por la categoría intermedia. Por ej, Electrodomésticos
            # > Pequeños electrodomésticos para traer Pava Eléctrica, Batidoras, etc.
            subcategories = asyncio.get_event_loop().run_until_complete(self.get_subcategories(category))
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

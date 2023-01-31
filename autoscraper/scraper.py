import csv
import json
import sys

import requests

from config.urls import UrlBuilder
from models import Category, Product, Store, SubCategory


class Scraper:
    """Descarga los datos de categorías y productos de una sucursal."""

    def __init__(self, store: Store):
        self._store_name = store.name
        self._store = store.sc
        self._url_builder = UrlBuilder()

    def set_writer(self, outfile):
        """Inicializa writer y filepath para persistir los productos."""

        self._outfile = outfile
        self._writer = csv.DictWriter(self._outfile, Product.get_fields(), lineterminator='\n')
        self._writer.writeheader()

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

    def parse_products(self, products_data: list, category_name: str, subcategory_name: str) -> list[Product]:
        """Retorna una lista de productos parseados del json descargado."""
        products = []
        for product_data in products_data:
            # product_data es un dict con toda la data (de la api) p un producto
            start_specific_category = product_data['categories'][0][:-2].rfind('/')+1
            products.append(Product(
                name=product_data['productName'],
                regular_price=product_data['items'][0]['sellers'][0]['commertialOffer']['ListPrice'],
                promotional_price=product_data['items'][0]['sellers'][0]['commertialOffer']['Price'],
                general_category=category_name,
                subcategory=subcategory_name,
                specific_category=product_data['categories'][0][start_specific_category:-1].lower(),
                sku=product_data['productId'],
                url=product_data['link'],
                stock=product_data['items'][0]['sellers'][0]['commertialOffer']['AvailableQuantity'],
                description=product_data['description'],
                ))

        return products

    def save_products(self, products: list[Product]):
        """Persiste en disco la data de productos procesados al momento."""
        self._writer.writerows(map(lambda p: p.__dict__, products))

    def get_products(self, category_name: str, subcategory: SubCategory) -> int:
        """Descarga todos los productos de la sucursal y los persiste en disco."""
        items_nbr = 0
        items_found = True
        start = 0
        # ciclo de a 50 items, lo max permitido por la api en una consulta
        while items_found:
            url = self._url_builder.build_product_url(start, subcategory.link, self._store)
            try:
                r = requests.get(url, timeout=10)
                products_data = json.loads(r.text)
            except requests.exceptions.RequestException as e:
                print(f'ERROR: no se pudo realizar la descarga {e}')
                sys.exit(1)
            except json.decoder.JSONDecodeError as e:
                print(f'ERROR: json descargado inválido {e}')
                sys.exit(1)

            # chequeo si el resultado de la consulta tiene items o está vacío
            if not products_data:
                items_found = False
                break

            # products_data es una lista de max. 50 productos
            products = self.parse_products(products_data, category_name, subcategory.name)
            items_nbr += len(products)
            self.save_products(products)
            start += 50

        return items_nbr

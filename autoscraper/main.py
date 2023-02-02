import argparse
import os
import sys
import time

from dotenv import load_dotenv

from autoscraper import __version__
from scraper import Scraper
from categoryscraper import CategoryScraper
from storescraper import StoreScraper
from utils import get_full_path, find_store


def configure():
    """Abre el archivo de config en el editor de texto default del SO."""

    os.system('notepad ' + 'config/config.env')


def parse_cmd_line_arguments():
    """Return the parsed cmd line arguments."""
    parser = argparse.ArgumentParser(
        prog="autoscraper",
        description="Scraper de productos del Hipermercado Libertad.",
        epilog="Gracias por usar autoscraper!",
    )
    parser.version = __version__
    help_msge_config = """Configurar proxies y/o ruta y/o nombre de archivo de salida. Default:
    home_usuario/nro_sucursal-nombre_sucursal-productos-fecha-hora.csv"""
    parser.add_argument("-v", "--version", action="version")
    parser.add_argument("-vc", "--ver-sucursales", action="store_true",
                        help="Ver listado de sucursales disponibles")
    parser.add_argument("-s", "--sucursal", help="Nro de sucursal a scrapear. Default: 12 (SDE)")
    parser.add_argument("-c", "--config", action='store_true', help=help_msge_config)

    return parser.parse_args()


def main():
    """Función principal, direcciona ejecución del programa."""

    start_time = time.time()
    load_dotenv(dotenv_path='config/config.env')
    args = parse_cmd_line_arguments()

    print('***Bienvenido a autoscraper!')

    if args.config:
        configure()
        return

    print('***Obteniendo información de sucursales')
    stores = StoreScraper().get_stores()
    if args.ver_sucursales:
        for store in sorted(stores, key=lambda x: x.sc):
            print(store)
        return

    # Valido store ingresada
    if args.sucursal:
        selected_store = find_store(stores, int(args.sucursal))
        if not selected_store:
            print('ERROR: Nro de sucursal inválido. Use la opción -vc para ver las sucursales disponibles',
                  file=sys.stderr)
            return
    else:
        selected_store = find_store(stores, 12)

    # Setear ruta
    if os.getenv('FILEPATH'):
        path, filename = get_full_path(os.getenv('FILEPATH'), selected_store)
    else:
        path, filename = get_full_path('', selected_store)

    print(f'***Obteniendo información de categorías para la sucursal {selected_store.name}')
    scraper = Scraper(selected_store)
    categories = CategoryScraper(selected_store).get_categories()

    print(f'***Iniciando scraping para sucursal {selected_store.name}')
    with open(path / filename, 'w', encoding='utf8') as outfile:
        total_items = 0
        scraper.set_writer(outfile)
        for category in categories:
            print(f'***Recolectando datos de productos de {category.name}')
            for subcategory in category.subcategories:
                items_nbr = scraper.get_products(category.name, subcategory)
                print(f'***{items_nbr} productos de {subcategory.name} recolectados.')
                total_items += items_nbr
        total_time = int(time.time() - start_time) // 60
        print(f'***{total_items} productos recolectados en {total_time} minutos.')
        print(f'***Productos guardados en: {str(path / filename)}')


if __name__ == '__main__':
    main()

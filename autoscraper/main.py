import argparse
import sys

from autoscraper import __version__
from scraper import Scraper
from storescraper import StoreScraper
from utils import get_full_path


def parse_cmd_line_arguments():
    """Return the parsed cmd line arguments."""
    parser = argparse.ArgumentParser(
        prog="autoscraper",
        description="Scraper de productos del Hipermercado Libertad.",
        epilog="Gracias por usar autoscraper!",
    )
    parser.version = __version__
    help_msge_ruta = """Ruta y nombre de archivo de salida. Por defecto, se 
    guarda en home del usuario como: nro_sucursal-nombre_sucursal-productos-fecha-hora.csv"""
    parser.add_argument("-v", "--version", action="version")
    parser.add_argument("-vc", "--ver-sucursales", action="store_true",
                        help="Ver listado de sucursales disponibles")
    parser.add_argument("sucursal", help="Nro de sucursal a scrapear")
    parser.add_argument("-r", "--ruta", help=help_msge_ruta)

    return parser.parse_args()


def main():
    """Función principal, direcciona ejecución del programa."""

    stores = StoreScraper().get_stores()

    args = parse_cmd_line_arguments()
    if args.ver_sucursales:
        for store in stores:
            print(store)
        return

    # Valido store ingresada
    for store in stores:
        if store.sc == int(args.sucursal):
            selected_store = store
            break
    else:
        print('ERROR: Nro de sucursal inválido. Use la opción -vc para ver las sucursales disponibles',
              file=sys.stderr)
        return

    # Setear ruta
    if args.ruta:
        path, filename = get_full_path(args.ruta, store)
    else:
        path, filename = get_full_path('', store)

    scraper = Scraper(selected_store)
    categories = scraper.get_categories()

    print(f'***Iniciando scraping para sucursal {store.name}')
    with open(path / filename, 'w', encoding='utf8') as outfile:
        total_items = 0
        scraper.set_writer(outfile)
        for category in categories[5:8]:
            print(f'***Recolectando datos de productos de {category.name}')
            for subcategory in category.subcategories:
                items_nbr = scraper.get_products(category.name, subcategory)
                print(f'***{items_nbr} productos de {subcategory.name} recolectados.')
                total_items += items_nbr
        print(f'***{total_items} productos recolectados.')
        print(f'***Productos guardados en: {str(path)}\{filename}')


if __name__ == '__main__':
    main()

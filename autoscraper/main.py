import argparse

from scraper import Scraper
from storescraper import StoreScraper

from autoscraper import __version__


def parse_cmd_line_arguments():
    """Return the parsed cmd line arguments."""
    parser = argparse.ArgumentParser(
        prog="autoscraper",
        description="Scraper de productos del Hipermercado Libertad.",
        epilog="Gracias por usar autoscraper!",
    )
    parser.version = __version__

    parser.add_argument("-v", "--version", action="version")
    parser.add_argument("-vc", "--ver-sucursales", action="store_true",
                        help="Ver listado de sucursales disponibles")

    return parser.parse_args()


def main():
    """Función principal, direcciona ejecución del programa."""

    args = parse_cmd_line_arguments()
    if args.ver_sucursales:
        stores = StoreScraper().get_stores()
        for store in stores:
            print(store)
        return

    store_name = 'Hipermercado Sgo. Del Estero'
    scraper = Scraper(store_name)
    categories = scraper.get_categories()
    for cat in categories:
        print(cat)
    print(f'Total categorias: {len(categories)}')

    filename = '../data/products-hiper-sde.txt'
    with open(filename, 'w', encoding='utf8') as outfile:
        scraper.set_writer(outfile)
        for category in categories:
            for subcategory in category.subcategories:
                scraper.get_products(category.name, subcategory)


if __name__ == '__main__':
    main()

from scraper import Scraper


def main():
    """Función principal, direcciona ejecución del programa."""

    store_name = 'Hipermercado Sgo. Del Estero'
    scraper = Scraper(store_name)
    categories = scraper.get_categories()
    for category in categories:
        print(category)


if __name__ == '__main__':
    main()

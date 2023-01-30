from scraper import Scraper


def main():
    """Función principal, direcciona ejecución del programa."""

    store_name = 'Hipermercado Sgo. Del Estero'
    scraper = Scraper(store_name)
    categories = scraper.get_categories()
    for cat in categories:
        print(cat)
    print(f'Total categorias: {len(categories)}')

    filename = '../data/products-hiper-sde.txt'
    with open(filename, 'w', encoding='utf8') as outfile:
        scraper.set_writer(outfile)
        for category in categories[18:]:
            for subcategory in category.subcategories:
                scraper.get_products(category.name, subcategory)


if __name__ == '__main__':
    main()

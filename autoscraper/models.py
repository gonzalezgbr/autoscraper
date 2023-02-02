from dataclasses import dataclass, fields


class SubCategory:
    """Subcategoría de una Categoría de productos."""

    def __init__(self, link: str):
        backslash = link[1:].find('/')
        self.name = link[backslash+2:].lower().replace('-', ' ').strip()
        self.link = link

    def __str__(self):
        return f'{self.name}({self.link})'


class Category:
    """Categoría de productos."""

    def __init__(self, name: str, link: str):
        self.name = name.lower()
        self.link = link[:-6].lower()
        self.subcategories = []

    def __str__(self):
        subcats = [str(subcat) for subcat in self.subcategories]

        return f'{self.name.upper()}: {",".join(subcats)}'

    def add_subcategories(self, subcategories: list[SubCategory]):
        """Agregar todas las subcategoría de una categoría."""
        self.subcategories.extend(subcategories)


@dataclass
class Product:
    """Producto final que se persiste."""
    name: str
    regular_price: int
    promotional_price: int
    general_category: str
    subcategory: str
    specific_category: str
    sku: int
    url: str
    stock: int
    description: str

    @staticmethod
    def get_fields() -> list[str]:
        """Devuelve los nombres de los campos de la clase."""
        return [field.name for field in fields(Product)]


@dataclass
class Store:
    """Sucursal disponible para scraping."""
    name: str
    sc: int

    def __str__(self):
        return f'{str(self.sc)}: {self.name}'

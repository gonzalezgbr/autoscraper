from dataclasses import dataclass, fields


class SubCategory:
    """Subcategoría de una Categoría de productos."""

    def __init__(self, name: str, link: str):
        self.name = name
        self.link = link

    def __str__(self):
        return f'{self.name}({self.link})'


class Category:
    """Categoría de productos."""

    def __init__(self, name: str):
        self.name = name.lower()
        self.subcategories = []

    def __str__(self):
        subcats = [str(subcat) for subcat in self.subcategories]

        return f'{self.name.upper()}: {",".join(subcats)}'

    def add_subcategory(self, name: str, link: str):
        """Agregar una subcategoría a su Categoría padre."""
        # se elimina el final del link: ?map=c,c,c
        self.subcategories.append(
            SubCategory(name.lower(), link[:-8].lower())
            )


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

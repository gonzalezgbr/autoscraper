
class SubCategory:
    """Subcategoría de una Categoría de productos."""

    def __init__(self, name: str, link: str):
        self._name = name
        self._link = link

    def __str__(self):
        return f'{self._name}({self._link})'


class Category:
    """Categoría de productos."""

    def __init__(self, name: str):
        self._name = name.lower()
        self._subcategories = []

    def __str__(self):
        subcats = [str(subcat) for subcat in self._subcategories]

        return f'{self._name.upper()}: {",".join(subcats)}'

    def add_subcategory(self, name: str, link: str):
        """Agregar una subcategoría a su Categoría padre."""
        # se elimina el final del link: ?map=c,c,c
        self._subcategories.append(
            SubCategory(name.lower(), link[:-8].lower())
            )

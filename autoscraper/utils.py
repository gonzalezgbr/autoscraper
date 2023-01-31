from datetime import datetime
from pathlib import Path
import sys

from models import Store


def make_filename(store: Store) -> str:
    """Devuelve el nombre del archivo de salida."""
    today = datetime.today().strftime('%Y%m%d_%H%M%S')
    store_name = store.name.replace('-', '_').title().replace(' ', '').replace('.', '')

    return f'{store.sc}_{store_name}_{today}.csv'


def get_full_path(path: str, store: Store) -> tuple[Path, str]:
    """Devuelve el path y filename donde almacenar los resultados"""

    if path:
        path = Path(path)
        if path.suffix:
            # tengo path y filename
            only_path = path.parent
            filename = path.name
        else:
            # tengo solo path, genero filename default
            only_path = path
            filename = make_filename(store)

        if not only_path.exists():
            # path no existe, debo crearlo
            try:
                only_path.mkdir(parents=True, exist_ok=False)
            except FileNotFoundError:
                print('ERROR: el directorio proporcionado es incorrecto.',
                      file=sys.stderr)
                sys.exit(1)
    else:
        only_path = Path.home()
        filename = make_filename(store)

    return only_path, filename

# Scraper HL

> *Este repositorio corresponde al challenge Python Web Scraping proporcionado por Autoscraping.*

`autoscraper` es una app cli que permite descargar información sobre los productos disponibles en las distintas sucursales del Hipermercado Libertad.

## Instalación
1. Crear una carpeta para el proyecto en la máquina local 

2. Clonar el proyecto en la carpeta creada
```sh
git clone git@github.com:gonzalezgbr/autoscraper.git .
```

3. Crear un entorno virtual usando `venv`
```sh
py -m venv venv
```

4. Activar el entorno creado
```sh
venv/Scripts/Activate
```

5. Instalar los paquetes necesarios desde el archivo de requerimientos
```sh
pip install -r autoscraper/requirements.txt
```
6. Ejecutar la app desde la terminal
```sh
py autoscraper/main.py nro_sucursal
```

## Ejecución

- El scraper tiene como parámetro obligatorio el nro de sucursal de donde se quiere descargar la info de los productos.
```sh
py autoscraper/main.py 12
```
- Opcionalmente, se puede proporcionar una ruta y/o un nombre de archivo. Si no se proporcionan, los datos se guardan en la carpeta home del usuario en un archivo de nombre `{nro sucursal}_{nombre sucursal}_{fecha}_{hora}.csv`
```sh
py autoscraper/main.py 12 -r mi_carpeta/productos.csv
```
- Para ver los números de sucursales disponibles:
```sh
py autoscraper/main.py -vc
```
- Para ver todas estas opciones:
```sh
py autoscraper/main.py -h
```

## Breve descripción del proyecto

El proyecto se estructura en 4 archivos principales:
- `main.py` es el script de ejecución. Convoca a las funciones de cada módulo para obtener sucursales y categoría, y descargar, procesar y almacenar los datos de los productos de la sucursal elegida. 
- `storescraper.py` contiene una clase que descarga los datos de las sucursales disponibles para poder parametrizar la recuperación de los productos.
- `scraper.py` contiene una clase que descarga los datos de las categorías y de los productos, de la sucursal seleccionada. 
- `models.py` contiene las clases que representan las EDs usadas para procesar las categorías, subcategorías, sucursales y productos. 

Adicionalmente: 
- en la carpeta `config` se encuentra el archivo `urls.py` que se encarga de construir las urls de descarga en base a un conjunto de urls base.
- en el archivo `utils.py` se encuentran las funciones usadas para chequear/crear la ruta de guardado y generar el nombre de archivo default.

## Hecho con
Este proyecto se desarrolló con `python`:
- `argparse` para procesar las opciones de linea de comandos.
- `pathlib` para gestionar con archivos y carpetas.
- `csv`, para persistir los archivos.
- `json`, para procesar los datos descargados.
- `requests`, para descargar los datos de la web.

---

**By GG** · [`github` @gonzalezgbr](https://github.com/gonzalezgbr/) · [`linkedin` @gonzalezgbr](https://www.linkedin.com/in/gonzalezgbr/) 

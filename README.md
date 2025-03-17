# Proyecto de ETL con JSONPlaceholder y SQLite

Este proyecto es un proceso de ETL (Extracción, Transformación y Carga) que obtiene datos de la API de [JSONPlaceholder](https://jsonplaceholder.typicode.com), los procesa y los carga en una base de datos SQLite.

## Descripción

Este script utiliza la API pública de JSONPlaceholder para obtener datos simulados de "posts". Luego, los procesa para extraer los campos `userId`, `id`, `title`, y `body`, y los almacena en una base de datos SQLite llamada `jsonplaceholder.db`.

### El flujo de trabajo (ETL) es el siguiente:

1. **Extracción**: Obtiene datos de la API de JSONPlaceholder.
2. **Transformación**: Procesa los datos para extraer la información relevante (`userId`, `id`, `title`, `body`).
3. **Carga**: Inserta los datos procesados en una tabla de SQLite llamada `post`.

## Requisitos

- Python 3.x
- Las siguientes bibliotecas de Python:
  - `requests`
  - `sqlite3` (incluida en la biblioteca estándar de Python)
  - `prefect` (para gestionar el flujo de trabajo ETL)

Puedes instalar las dependencias utilizando `pip`:

```bash
pip install requests prefect

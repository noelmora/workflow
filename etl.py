import requests
import sqlite3
import logging
from contextlib import contextmanager
from prefect import task, flow


DB_NAME = "jsonplaceholder.db"
API_URL = "https://jsonplaceholder.typicode.com/posts"
REQUEST_SIZE = 5  


logging.basicConfig(filename="etl_errors.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        logging.error(f"Error en la base de datos: {e}")
    finally:
        conn.close()


def create_table():
    with get_db_connection() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS post (
                user_id INTEGER,
                id INTEGER,
                title TEXT,
                body TEXT
            )
        ''')

session = requests.Session()

@task(retries=3, retry_delay_seconds=10, persist_result=True)
def get_post_data():
    try:
        response = session.get(API_URL, params={'_limit': REQUEST_SIZE})
        response.raise_for_status()
        return response.json()  
    except requests.exceptions.RequestException as e:
        logging.error(f"Error en la API: {e}")
        return simulate_data()  


def simulate_data():
    logging.info("Usando datos simulados")
    return [
        {'userId': 1, 'id': 1, 'title': 'Título post 1', 'body': 'Contenido post 1'},
        {'userId': 2, 'id': 2, 'title': 'Título post 2', 'body': 'Contenido post 2'}
    ]


@task(persist_result=True)
def parse_post_data(raw):
    posts = []

    for row in raw:
        post_tuple = (
            row.get('userId', 0),
            row.get('id', 0),
            row.get('title', 'Sin título'),
            row.get('body', 'Sin contenido')
        )
        posts.append(post_tuple)

    logging.info(f"Se procesaron {len(posts)} posts.")
    return posts


def validate_post(post):
    user_id, post_id, title, body = post
    return isinstance(user_id, int) and isinstance(post_id, int) and isinstance(title, str) and isinstance(body, str)

@task(persist_result=True)
def store_posts(parsed):
    if not parsed:
        logging.warning("No hay datos para almacenar.")
        return
    
    filtered_posts = [p for p in parsed if validate_post(p)]
    
    with get_db_connection() as cursor:
        cursor.executemany("INSERT INTO post VALUES (?, ?, ?, ?)", filtered_posts)

    logging.info(f"Se insertaron {len(filtered_posts)} registros en la base de datos.")


@flow
def my_etl_flow():
    create_table()  
    raw = get_post_data()
    parsed = parse_post_data(raw)
    store_posts(parsed)


if __name__ == "__main__":
    my_etl_flow()

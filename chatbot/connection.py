import psycopg

def get_connection():
    return psycopg.connect(
        host='localhost',
        port='5432',
        dbname='test_shop',
        user='postgres',
        password='postgres'
    )
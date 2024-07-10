
import psycopg2



DATABASE_CONFIG = {
    'user':'postgres',
    'password': '2022',
    'host': '127.0.0.1',
    'database': 'socios',
    'port': 5432
}

def test_connection():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    conn.commit()
    cur.close()
    conn.close()

    print('TEST CONECTION - 0K')
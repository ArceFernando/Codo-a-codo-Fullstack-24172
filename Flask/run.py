from flask import Flask, request, jsonify, send_file
from psycopg2 import connect, extras
from app.database import *

app = Flask(__name__)

test_connection()

host = 'localhost'
port = 5432
database = 'socios'
user ='postgres'
password = '2022'

def get_connection():
    conn = connect(host=host, port=port, database=database, user=user, password=password)
    return conn



@app.get('/api/users')
def get_users():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    cur.close()
    conn.close()

    
    return 'jsonify(users)'

@app.post('/api/users')
def create_user():
    new_user = request.get_json()
    username = new_user['username']
        
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor) # asi me devuelve un diccionario

    cur.execute('INSERT INTO users (username) VALUES (%s) RETURNING*',(username))
    new_created_user = cur.fecthone()
    print(new_created_user)

    conn.commit()

    cur.close()
    conn.close()

    return jsonify(new_created_user)

@app.get('/')
def home():
    return send_file('templates/contacto.html')


if __name__ == '__main__':
    app.run(debug=True)
    
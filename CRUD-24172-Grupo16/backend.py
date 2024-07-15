from flask import Flask, jsonify, request, send_file
from psycopg2 import connect, extras
from cryptography.fernet import Fernet

backend = Flask (__name__)
key = Fernet.generate_key()

host = 'localhost'
port = 5432
dbname = 'sociosdb'
user = 'postgres'
password = '2022'

def get_connection():
    conn = connect(host=host, port=port, dbname=dbname, user=user, password=password)
    return conn

""""
# opcion de prueba de consulta a la base de datos sin usar Test Connection
@backend.get('/')
def home():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 + 1")
    result = cur.fetchone() # fecthone para que el cursor me del resultado en consola  

    print (result)

    return 'Hola, mundo'
"""
@backend.get('/api/users')
def get_users():    
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify(users)


@backend.post('/api/users')
def create_user():
    """" 
    # pruebo el request
    print (request.get_json()) # con get_json obtengo lo que envio en el objeto request
    """
    new_user = request.get_json()
    username = new_user['username']
    email = new_user['email']

    # print(username, email) 

    
    password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8'))

    
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING *",
                (username, email, password))
    
    new_created_user = cur.fetchone()
    print(new_created_user)  
    """
    Con esto pruebo que me devuelve una tupla y con el metdo extras me devuelve un diccionario
    """  

    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_created_user)

    
    #return 'creating users'


@backend.get('/api/users/<id>')
def get_user(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    """
    # prueba Get
    print(user)

    return 'getting user 1'
    """
    if user is None:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(user)  


@backend.put('/api/users/<id>')
def update_user(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    new_user = request.get_json()
    username = new_user['username']
    email = new_user['email']
    password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8'))
    cur.execute("UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s RETURNING *",
                (username, email, password, id))
    updated_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if updated_user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(updated_user)


@backend.delete('/api/users/<id>')
def delete_user(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("DELETE FROM users WHERE id = %s RETURNING *", (id,))
    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user)


@backend.get('/')
def home():
    return send_file('static/index.html') 

# Atencion no cambiarme el nombre de carpeta  static {{url_for('static', filename='style.css')}}

if __name__ == '__main__':
   backend.run(debug=True)

# debug = True Reinicia el codigo por si solo




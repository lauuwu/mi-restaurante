from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'restaurante'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'password')
    )

@app.route('/menu')
def menu():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT nombre, descripcion, precio FROM platos')
    platos = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([
        {'nombre': p[0], 'descripcion': p[1], 'precio': p[2]}
        for p in platos
    ])

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

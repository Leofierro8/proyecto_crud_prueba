from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'clave_secreta_provisional'

# --- BASE DE DATOS (Modelo) ---
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS productos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, descripcion TEXT)')
    conn.commit()
    conn.close()

# --- RUTAS (Controlador) ---

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    user = request.form['user']
    password = request.form['pass']
    if user == 'admin' and password == '1234': # Login simple
        session['user'] = user
        return redirect(url_for('index'))
    return "Usuario incorrecto", 401

@app.route('/dashboard')
def index():
    if 'user' not in session: return redirect(url_for('login'))
    
    search = request.args.get('search')
    conn = get_db_connection()
    
    if search:
        items = conn.execute('SELECT * FROM productos WHERE nombre LIKE ?', ('%' + search + '%',)).fetchall()
    else:
        items = conn.execute('SELECT * FROM productos').fetchall()
    
    conn.close()
    return render_template('index.html', items=items)

@app.route('/create', methods=['POST'])
def create():
    nombre = request.form['nombre']
    desc = request.form['descripcion']
    conn = get_db_connection()
    conn.execute('INSERT INTO productos (nombre, descripcion) VALUES (?, ?)', (nombre, desc))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)


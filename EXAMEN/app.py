from flask import Flask, request, jsonify, render_template_string, send_from_directory, redirect, abort
import os
from flask_mysqldb import MySQL
from typing import cast
from MySQLdb.connections import Connection

import config

app = Flask(__name__)

# Configuración MySQL
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)


def get_conn_cursor():
    """Devuelve (conn, cursor) con typing.cast para que Pylance no marque None."""
    conn = cast(Connection, mysql.connection)
    cur = conn.cursor()
    return conn, cur




@app.route('/', methods=['GET'])
def home():
    # Redirige a la UI estática en `frontend/`
    return redirect('/app')


# API: lista de estudiantes
@app.route('/estudiantes', methods=['GET'])
def get_estudiantes():
    conn, cur = get_conn_cursor()
    cur.execute("SELECT * FROM estudiantes")
    estudiantes = cur.fetchall()
    cur.close()
    return jsonify(estudiantes)


# API: lista de materias
@app.route('/materias', methods=['GET'])
def get_materias():
    conn, cur = get_conn_cursor()
    cur.execute("SELECT * FROM materias")
    materias = cur.fetchall()
    cur.close()
    return jsonify(materias)


# API: registrar nota (JSON)
@app.route('/notas', methods=['POST'])
def add_nota():
    data = request.get_json(force=True)
    estudiante_id = data.get('estudiante_id')
    materia_id = data.get('materia_id')
    nota = data.get('nota')
    if nota is None or nota == '':
        return jsonify({'error': 'La nota no puede estar vacía'}), 400
    try:
        n = float(nota)
    except Exception:
        return jsonify({'error': 'La nota debe ser un número'}), 400
    if not (0 <= n <= 100):
        return jsonify({'error': 'La nota debe estar entre 0 y 100'}), 400
    conn, cur = get_conn_cursor()
    cur.execute("SELECT id FROM estudiantes WHERE id=%s", (estudiante_id,))
    if not cur.fetchone():
        cur.close()
        return jsonify({'error': 'El estudiante no existe'}), 400
    cur.execute("SELECT id FROM materias WHERE id=%s", (materia_id,))
    if not cur.fetchone():
        cur.close()
        return jsonify({'error': 'La materia no existe'}), 400
    cur.execute("INSERT INTO notas (estudiante_id, materia_id, nota) VALUES (%s, %s, %s)",
                (estudiante_id, materia_id, n))
    conn.commit()
    cur.close()
    return jsonify({'message': 'Nota registrada correctamente'}), 201


# API: notas por estudiante + promedio (HTML)
@app.route('/notas/estudiante', methods=['GET'])
def notas_estudiante_html():
    # Redirige a la vista del frontend (hash route) que muestra las notas del estudiante
    id = request.args.get('id')
    if not id:
        return redirect('/app')
    return redirect(f'/app/consultar?id={id}')


# API: notas por estudiante (JSON)
@app.route('/notas/estudiante/<int:id>', methods=['GET'])
def get_notas_estudiante(id):
    conn, cur = get_conn_cursor()
    cur.execute("""SELECT n.nota, m.nombre
                   FROM notas n
                   JOIN materias m ON n.materia_id = m.id
                   WHERE n.estudiante_id = %s""", (id,))
    notas = cur.fetchall()
    cur.execute("SELECT AVG(nota) FROM notas WHERE estudiante_id = %s", (id,))
    promedio = cur.fetchone()[0]
    cur.close()
    return jsonify({'notas': notas, 'promedio': promedio})


@app.route('/<path:filename>')
def serve_static(filename):
    # Servir archivos estáticos desde la carpeta `frontend`
    front_dir = os.path.join(app.root_path, 'frontend')
    file_path = os.path.join(front_dir, filename)
    if os.path.exists(file_path):
        return send_from_directory(front_dir, filename)
    # si no existe, devolver 404
    abort(404)


@app.route('/app')
@app.route('/app/')
def app_index():
    front_dir = os.path.join(app.root_path, 'frontend')
    return send_from_directory(front_dir, 'index.html')


@app.route('/app/registrar')
def app_registrar():
    front_dir = os.path.join(app.root_path, 'frontend')
    return send_from_directory(front_dir, 'registrar.html')


@app.route('/app/consultar')
def app_consultar():
    front_dir = os.path.join(app.root_path, 'frontend')
    return send_from_directory(front_dir, 'consultar.html')


if __name__ == "__main__":
    app.run(debug=True)
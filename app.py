from flask import Flask, request, jsonify, send_from_directory
import psycopg2
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="static")
CORS(app)

DATABASE_URL = "postgresql://prueba_web_user:GZ93s12cp2s6TmdKAWDwkgIjf8DszFvW@dpg-d6mbd2fafjfc7390hgk0-a.oregon-postgres.render.com/prueba_web?sslmode=require"


def conectar_db():
    return psycopg2.connect(DATABASE_URL)


@app.route("/")
def inicio():
    return send_from_directory("static", "index.html")


@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():

    try:
        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100)
        )
        """)

        cursor.execute("SELECT * FROM usuarios")

        usuarios = cursor.fetchall()

        lista = []

        for u in usuarios:
            lista.append({
                "id": u[0],
                "nombre": u[1]
            })

        cursor.close()
        conexion.close()

        return jsonify(lista)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/usuarios", methods=["POST"])
def crear_usuario():

    try:

        data = request.json
        nombre = data["nombre"]

        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100)
        )
        """)

        cursor.execute(
            "INSERT INTO usuarios (nombre) VALUES (%s)",
            (nombre,)
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        return jsonify({"mensaje": "usuario creado"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
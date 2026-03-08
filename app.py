from flask import Flask, request, jsonify, send_from_directory
import psycopg2
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="static")
CORS(app)

# conexión a PostgreSQL en Render
conexion = psycopg2.connect(
"postgresql://prueba_web_user:GZ93s12cp2s6TmdKAWDwkgIjf8DszFvW@dpg-d6mbd2fafjfc7390hgk0-a.oregon-postgres.render.com/prueba_web?sslmode=require"
)

# crear tabla si no existe
cursor = conexion.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100)
)
""")
conexion.commit()
cursor.close()


# ruta principal
@app.route("/")
def inicio():
    return send_from_directory("static", "index.html")


# obtener usuarios
@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():

    try:
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM usuarios")

        usuarios = cursor.fetchall()

        lista = []

        for u in usuarios:
            lista.append({
                "id": u[0],
                "nombre": u[1]
            })

        cursor.close()

        return jsonify(lista)

    except Exception as e:

        conexion.rollback()

        return jsonify({"error": str(e)}), 500


# crear usuario
@app.route("/usuarios", methods=["POST"])
def crear_usuario():

    try:

        data = request.json

        nombre = data["nombre"]

        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO usuarios (nombre) VALUES (%s)",
            (nombre,)
        )

        conexion.commit()

        cursor.close()

        return jsonify({"mensaje": "usuario creado"})

    except Exception as e:

        conexion.rollback()

        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
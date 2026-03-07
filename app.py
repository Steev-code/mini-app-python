from flask import Flask, request, jsonify, send_from_directory
import psycopg2
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

# conexión a la base de datos (Render PostgreSQL)
conexion = psycopg2.connect(
"postgresql://prueba_web_user:GZ93s12cp2s6TmdKAWDwkgIjf8DszFvW@dpg-d6mbd2fafjfc7390hgk0-a.oregon-postgres.render.com/prueba_web"
)

# ruta principal
@app.route("/")
def inicio():
    return send_from_directory("static", "index.html")


# obtener usuarios
@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():

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


# crear usuario
@app.route("/usuarios", methods=["POST"])
def crear_usuario():

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
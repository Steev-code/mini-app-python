from flask import Flask, request, jsonify, send_from_directory
import psycopg2
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

conexion = psycopg2.connect(
    host="localhost",
    database="prueba_web",
    user="postgres",
    password="3112230437"
)

@app.route("/")
def inicio():
    return send_from_directory("static", "index.html")


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

    return jsonify(lista)


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

    return jsonify({"mensaje": "usuario creado"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
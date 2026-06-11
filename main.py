from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///peliculas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modelo de la base de datos
class Pelicula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(50), nullable=False)
    calificacion = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "genero": self.genero,
            "calificacion": self.calificacion
        }
@app.route("/")
def home():
    return jsonify({"message": "Bienvenido a la API de PEli. Usa peliculas para ver los datos."})

# --- Rutas de la API ---

# 1. Obtener todas las películas
@app.route("/peliculas", methods=["GET"])
def get_peliculas():
    peliculas = Pelicula.query.all()
    return jsonify([p.to_dict() for p in peliculas])

# 2. Obtener una película por ID
@app.route("/peliculas/<int:id>", methods=["GET"])
def get_pelicula(id):
    peli = Pelicula.query.get(id)
    if peli:
        return jsonify(peli.to_dict())
    return jsonify({"error": "Película no encontrada"}), 404

# 3. Crear una nueva película
@app.route("/peliculas", methods=["POST"])
def add_pelicula():
    data = request.get_json()
    new_peli = Pelicula(
        titulo=data["titulo"],
        genero=data["genero"],
        calificacion=data["calificacion"]
    )
    db.session.add(new_peli)
    db.session.commit()
    return jsonify(new_peli.to_dict()), 201

# 4. Actualizar una película existente
@app.route("/peliculas/<int:id>", methods=["PUT"])
def update_pelicula(id):
    data = request.get_json()
    peli = Pelicula.query.get(id)
    if peli:
        peli.titulo = data.get("titulo", peli.titulo)
        peli.genero = data.get("genero", peli.genero)
        peli.calificacion = data.get("calificacion", peli.calificacion)
        db.session.commit()
        return jsonify(peli.to_dict())
    return jsonify({"error": "Película no encontrada"}), 404
        
# 5. Eliminar una película
@app.route("/peliculas/<int:id>", methods=["DELETE"])
def delete_pelicula(id):
    peli = Pelicula.query.get(id)
    if peli:
        db.session.delete(peli)
        db.session.commit()
        return jsonify({"message": "Película eliminada correctamente"})
    return jsonify({"error": "No existe la película para eliminar"}), 404

# Iniciar aplicación
if __name__ == "__main__":
    with app.app_context():
        db.create_all() # Crea el archivo peliculas.db automáticamente
    app.run(debug=True)
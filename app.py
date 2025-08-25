from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuración de la base de datos (Render inyecta DATABASE_URL)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modelo para almacenar los SMS
class SMS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50))
    message = db.Column(db.Text)

# Crear las tablas (solo la primera vez)
with app.app_context():
    db.create_all()

@app.route("/sms", methods=["POST"])
def sms():
    try:
        data = request.get_json()
        sender = data.get("from")
        message = data.get("message")

        # Guardar en la base de datos
        nuevo_sms = SMS(sender=sender, message=message)
        db.session.add(nuevo_sms)
        db.session.commit()

        print(f"📩 Guardado SMS de {sender}: {message}")
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 400

# Endpoint para listar los SMS
@app.route("/list", methods=["GET"])
def listar_sms():
    mensajes = SMS.query.all()
    return jsonify([
        {"id": m.id, "from": m.sender, "message": m.message}
        for m in mensajes
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

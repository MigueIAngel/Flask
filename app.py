from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/sms", methods=["POST"])
def sms():
    try:
        data = request.get_json()
        sender = data.get("from")
        message = data.get("message")

        print(f"📩 SMS recibido de {sender}: {message}")

        # Guardar en archivo
        with open("sms_log.txt", "a", encoding="utf-8") as f:
            f.write(f"De: {sender} | Mensaje: {message}\n")

        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

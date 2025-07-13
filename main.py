# main.py
from flask import Flask, request, jsonify
from services.zapi_sender import enviar_documento_formatado

app = Flask(__name__)

@app.route("/enviar-pdf", methods=["POST"])
def enviar_pdf():
    try:
        data = request.json
        response = enviar_documento_formatado(data)

        return jsonify({
            "status": response.status_code,
            "resposta": response.text
        }), response.status_code

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

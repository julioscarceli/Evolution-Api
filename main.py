import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configurações fixas ou via variável de ambiente
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID", "3E41CFD6E358C17CE6F98258D1F0342D")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN", "0805E5918986E2F446970EAB")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN", "F3344a9f851a041f2a24ec073eb47e5e0S")

ZAPI_URL = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-document/pdf"

def formatar_mensagem(texto: str) -> str:
    """
    Ajusta quebras de linha (\n) para mensagem no WhatsApp.
    """
    return texto.replace("\\n", "\n")

@app.route("/enviar-pdf", methods=["POST"])
def enviar_pdf():
    try:
        data = request.json

        phone = data.get("phone")
        mensagem = formatar_mensagem(data.get("mensagem", ""))
        nome_arquivo = data.get("nome_arquivo")
        url_arquivo = data.get("arquivo")

        if not all([phone, mensagem, nome_arquivo, url_arquivo]):
            return jsonify({"erro": "Campos obrigatórios faltando."}), 400

        payload = {
            "phone": phone,
            "document": url_arquivo,
            "fileName": nome_arquivo,
            "caption": mensagem
        }

        headers = {
            "Content-Type": "application/json",
            "client-token": ZAPI_CLIENT_TOKEN
        }

        response = requests.post(ZAPI_URL, headers=headers, json=payload)

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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

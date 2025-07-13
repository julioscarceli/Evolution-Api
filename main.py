from flask import Flask, request, jsonify
import requests
import logging
import os

app = Flask(__name__)

EVOLUTION_BASE_URL = os.getenv("EVOLUTION_BASE_URL", "https://evolution-evolution.lmpta7.easypanel.host")
EVOLUTION_INSTANCIA = os.getenv("EVOLUTION_INSTANCIA", "automacao-whatsapp")
EVOLUTION_APIKEY = os.getenv("EVOLUTION_APIKEY", "SUA_API_KEY_AQUI")

@app.route("/enviar-mensagem", methods=["POST"])
def enviar_mensagem():
    try:
        data = request.json

        numero = data.get("numero")
        mensagem = data.get("mensagem")
        url_arquivo = data.get("arquivo")
        nome_arquivo = data.get("nome_arquivo")

        if not all([numero, mensagem, url_arquivo, nome_arquivo]):
            return jsonify({"erro": "Campos obrigatórios faltando."}), 400

        headers = {
            "Content-Type": "application/json",
            "apikey": EVOLUTION_APIKEY
        }

        payload = {
            "number": numero,
            "options": {
                "delay": 100,
                "presence": "composing"
            },
            "mediaMessage": {
                "mediaType": "document",  # pode ser: image, audio, document, etc.
                "fileName": nome_arquivo,
                "caption": mensagem,
                "media": url_arquivo
            }
        }

        api_url = f"{EVOLUTION_BASE_URL}/message/sendMedia/{EVOLUTION_INSTANCIA}"
        response = requests.post(api_url, headers=headers, json=payload)

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

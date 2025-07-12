from flask import Flask, request, jsonify
import requests
import logging
import os

app = Flask(__name__)

# Configurações da Evolution API (coloque suas credenciais aqui)
EVOLUTION_BASE_URL = os.getenv("EVOLUTION_BASE_URL", "https://evolution-evolution.lmpta7.easypanel.host")
EVOLUTION_INSTANCIA = os.getenv("EVOLUTION_INSTANCIA", "automacao-whatsapp")
EVOLUTION_APIKEY = os.getenv("EVOLUTION_APIKEY", "5f2a8c4b7d1e9f3c6b0d4a7e2c9f1b8d")

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

        # Cabeçalhos para a API Evolution
        headers = {
            "Content-Type": "application/json",
            "apikey": EVOLUTION_APIKEY
        }

        payload = {
            "number": numero,
            "caption": mensagem,
            "fileName": nome_arquivo,
            "url": url_arquivo
        }

        api_url = f"{EVOLUTION_BASE_URL}/message/sendFile/{EVOLUTION_INSTANCIA}"

        logging.info(f"Enviando para Evolution API: {api_url}")
        logging.info(f"Payload: {payload}")

        response = requests.post(api_url, headers=headers, json=payload)

        return jsonify({
            "status": response.status_code,
            "resposta": response.text
        }), response.status_code

    except Exception as e:
        logging.exception("Erro inesperado no envio da mensagem")
        return jsonify({"erro": str(e)}), 500

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
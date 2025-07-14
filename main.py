import requests
import base64
from flask import Flask, request, jsonify
from config import EVOLUTION_BASE_URL, EVOLUTION_INSTANCE, EVOLUTION_TOKEN, PORT

app = Flask(__name__)

# URL completa da Evolution API
EVOLUTION_URL = f"{EVOLUTION_BASE_URL}/message/sendMedia/{EVOLUTION_INSTANCE}"


def formatar_mensagem(texto: str) -> str:
    return texto.replace("\\n", "\n")


def baixar_arquivo_base64(url_arquivo: str) -> str:
    """Faz download de um arquivo e retorna em base64"""
    response = requests.get(url_arquivo)
    response.raise_for_status()
    return base64.b64encode(response.content).decode("utf-8")


def formatar_numero(numero: str) -> str:
    """Formata o número para o padrão da Evolution API"""
    numero = ''.join(filter(str.isdigit, numero))
    if not numero.startswith("55"):
        numero = f"55{numero}"
    return f"{numero}@s.whatsapp.net"


@app.route("/enviar-pdf", methods=["POST"])
def enviar_pdf_cliente():
    try:
        data = request.json

        phone = data.get("phone")
        mensagem = formatar_mensagem(data.get("mensagem", ""))
        nome_arquivo = data.get("nome_arquivo")
        url_arquivo = data.get("arquivo")

        if not all([phone, mensagem, nome_arquivo, url_arquivo]):
            return jsonify({"erro": "Campos obrigatórios faltando."}), 400

        numero_formatado = formatar_numero(phone)
        pdf_base64 = baixar_arquivo_base64(url_arquivo)

        payload = {
            "number": numero_formatado,
            "options": {
                "delay": 100,
                "presence": "composing"
            },
            "mediatype": "document",
            "fileName": nome_arquivo,
            "caption": mensagem,
            "media": pdf_base64
        }

        headers = {
            "Content-Type": "application/json",
            "apikey": EVOLUTION_TOKEN
        }

        response = requests.post(EVOLUTION_URL, headers=headers, json=payload)
        return jsonify({
            "status": response.status_code,
            "resposta": response.text
        }), response.status_code

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/enviar-pdf-controle", methods=["POST"])
def enviar_pdf_controle():
    try:
        data = request.json

        nome_cliente = data.get("nome_cliente")
        endereco = data.get("endereco_cliente")
        qtd_persianas = data.get("quantidade_persianas")
        numero_pedido = data.get("numero_pedido")
        url_arquivo = data.get("arquivo")
        nome_arquivo = data.get("nome_arquivo")
        phone = "5511986152909"

        if not all([nome_cliente, endereco, qtd_persianas, numero_pedido, url_arquivo, nome_arquivo]):
            return jsonify({"erro": "Campos obrigatórios faltando."}), 400

        mensagem = (
            f"Automatik Persianas\n"
            f"Novo Pedido feito por {nome_cliente}!\n"
            f"Endereço do cliente :\n{endereco}\n\n"
            f"📄 Segue detalhes do pedido :\n\n"
            f"Quantidade de persianas : {qtd_persianas}\n"
            f"Número do pedido : {numero_pedido}"
        )

        numero_formatado = formatar_numero(phone)
        pdf_base64 = baixar_arquivo_base64(url_arquivo)

        payload = {
            "number": numero_formatado,
            "options": {
                "delay": 100,
                "presence": "composing"
            },
            "mediatype": "document",
            "fileName": nome_arquivo,
            "caption": mensagem,
            "media": pdf_base64
        }

        headers = {
            "Content-Type": "application/json",
            "apikey": EVOLUTION_TOKEN
        }

        response = requests.post(EVOLUTION_URL, headers=headers, json=payload)
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
    app.run(host="0.0.0.0", port=PORT)



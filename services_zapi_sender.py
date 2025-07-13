# services/zapi_sender.py
import requests
import os

def formatar_mensagem(texto_bruto: str) -> str:
    """
    Realiza substituições simples para formatação do WhatsApp.
    """
    return texto_bruto.replace("\\n", "\n")

def enviar_documento_formatado(data: dict):
    ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID", "3E41CFD6E358C17CE6F98258D1F0342D")
    ZAPI_TOKEN = os.getenv("ZAPI_TOKEN", "0805E5918986E2F446970EAB")
    ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN", "F3344a9f851a041f2a24ec073eb47e5e0S")

    BASE_URL = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-document/pdf"

    phone = data.get("phone")
    mensagem = formatar_mensagem(data.get("mensagem", ""))
    nome_arquivo = data.get("nome_arquivo")
    url_arquivo = data.get("arquivo")

    if not all([phone, mensagem, nome_arquivo, url_arquivo]):
        raise ValueError("Campos obrigatórios faltando.")

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

    response = requests.post(BASE_URL, json=payload, headers=headers)
    return response

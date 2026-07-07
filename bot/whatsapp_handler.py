import os
import logging
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from llm.normalizer import MedicamentoNormalizer
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
normalizer = MedicamentoNormalizer()

def register_webhook(webhook_url: str):
    """Registra el webhook en Twilio automáticamente."""
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)
    phone_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
    try:
        incoming = client.incoming_phone_numbers.list(phone_number=phone_number)[0]
        incoming.update(sms_url=webhook_url, sms_method="POST")
        logging.info(f"✅ Webhook registrado en {webhook_url}")
    except Exception as e:
        logging.warning(f"No se pudo registrar webhook automáticamente: {e}")

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.form.get("Body", "").strip()
    sender = request.form.get("From", "desconocido")
    logging.info(f"Mensaje de {sender}: {incoming_msg}")
    
    resp = MessagingResponse()
    msg = resp.message()
    
    if not incoming_msg:
        msg.body("Por favor, envía el nombre de un medicamento.")
        return Response(str(resp), mimetype="application/xml")
    
    # Quitar /medicamento si está presente (compatibilidad)
    if incoming_msg.lower().startswith("/medicamento"):
        incoming_msg = incoming_msg[len("/medicamento"):].strip()
    
    resultado = normalizer.normalizar(incoming_msg)
    
    if "error" in resultado:
        msg.body(f"❌ Error: {resultado['error']}")
    else:
        # WhatsApp usa *negrita* y _cursiva_
        respuesta = (
            f"*📋 Ficha de {resultado.get('nombre_ingresado', incoming_msg)}*\n\n"
            f"*Nombre genérico:* {resultado.get('nombre_generico', 'N/D')}\n"
            f"*Uso principal:* {resultado.get('uso_principal', 'N/D')}\n"
            f"*¿Requiere receta?* {'Sí' if resultado.get('requiere_receta') else 'No'}"
        )
        msg.body(respuesta)
    
    return Response(str(resp), mimetype="application/xml")

@app.route("/", methods=["GET"])
def health():
    return "WhatsApp webhook activo ✅"

def run_whatsapp_bot(port=5000):
    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
        register_webhook(webhook_url)
    else:
        logging.warning("WEBHOOK_URL no definida, configura manualmente en Twilio.")
    app.run(host="0.0.0.0", port=port, debug=False)
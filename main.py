from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Cargar API key desde variables de entorno
openai.api_key = os.environ['OPENAI_API_KEY']

@app.route("/incoming", methods=['POST'])
def incoming():
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From', '')

    # Preparar mensaje para ChatGPT
    prompt = f"Mensaje recibido por WhatsApp: {incoming_msg}. ¿Qué acción deseas que el asistente realice?"

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    reply = completion.choices[0].message['content']

    # Enviar respuesta por Twilio
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(f"🤖 Asistente:\n{reply}\n\n¿Confirmas esta acción? (Responde SÍ o NO)")
    return str(resp)

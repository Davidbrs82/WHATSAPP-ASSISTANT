from flask import Flask, request
import openai
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Clave desde Replit/Render Secrets
openai.api_key = os.environ['OPENAI_API_KEY']

@app.route("/incoming", methods=["POST"])
def incoming():
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From', '')
    
    prompt = f"El usuario escribió por WhatsApp: {incoming_msg}. ¿Qué tarea quiere hacer?"
    
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    
    reply = completion.choices[0].message['content']

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(f"🤖 Asistente: {reply}\n\n¿Confirmas esta acción? (Responde SÍ o NO)")
    
    return str(resp)

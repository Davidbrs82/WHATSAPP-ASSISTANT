from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ['OPENAI_API_KEY']

@app.route("/incoming", methods=['POST'])
def incoming():
    print("📨 Mensaje recibido de Twilio")
    incoming_msg = request.values.get('Body', '').strip()
    prompt = f"El usuario escribió por WhatsApp: {incoming_msg}. ¿Qué tarea quiere hacer?"

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    reply = completion.choices[0].message['content']
    resp = MessagingResponse()
    resp.message(f"🤖 Asistente: {reply}\n\n¿Confirmas esta acción? (Responde SÍ o NO)")
    return str(resp)

@app.route("/")
def home():
    return "Bot activo en Render."

if __name__ == "__main__":
    app.run(debug=True)

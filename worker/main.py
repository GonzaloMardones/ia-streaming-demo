import os
import json
from dotenv import load_dotenv
from google.cloud import pubsub_v1
from google.cloud import firestore
import openai

load_dotenv()

project_id = os.getenv("GCP_PROJECT")
subscription_id = os.getenv("PUBSUB_SUBSCRIPTION")
subscription_path = f"projects/{project_id}/subscriptions/{subscription_id}"

subscriber = pubsub_v1.SubscriberClient()
db = firestore.Client()
openai.api_key = os.getenv('OPENAI_API_KEY')

def process_prompt(prompt):
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def callback(message):
    data = json.loads(message.data.decode("utf-8"))
    prompt = data.get("prompt")
    request_id = data.get("request_id")
    print(f"\nMensaje recibido:\n  prompt: {prompt}\n  request_id: {request_id}")

    reply = process_prompt(prompt)
    print(f"Respuesta IA: {reply}")

    # Guarda en Firestore
    db.collection("ai_responses").document(request_id).set({
        "prompt": prompt,
        "response": reply,
        "status": "completed"
    })
    print(f"Respuesta guardada en Firestore para {request_id}")

    message.ack()
    print(f"Mensaje {request_id} confirmado.\n")

print(f"Escuchando mensajes en {subscription_path}...")
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()

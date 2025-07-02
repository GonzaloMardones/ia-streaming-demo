from fastapi import FastAPI
from google.cloud import pubsub_v1
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

import os
import json
import uuid

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(
    os.getenv("GCP_PROJECT"),
    os.getenv("PUBSUB_TOPIC")
)

@app.post("/generate")
async def generate(payload: dict):
    prompt = payload.get("prompt")
    request_id = str(uuid.uuid4())

    message = {
        "prompt": prompt,
        "request_id": request_id
    }

    future = publisher.publish(topic_path, json.dumps(message).encode('utf-8'))
    return {"request_id": request_id, "status": "queued"}

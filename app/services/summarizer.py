import requests
import os

HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = os.getenv("HF_MODEL", "facebook/bart-large-cnn")

API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

def summarize(text):
    response = requests.post(API_URL, headers=headers, json={
        "inputs": text,
        "parameters": {
            "max_length": 130,
            "min_length": 30
        }
    })

    return response.json()
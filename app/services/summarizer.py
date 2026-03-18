from app.core.config import HF_API_KEY, HF_MODEL
import requests
import time

# The new Hugging Face Inference AI Router (OpenAI-compatible)
API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}


def summarize(text: str):
    if not text or len(text.strip()) < 10:
        return "Not enough meaningful content to summarize."

    payload = {
        "model": HF_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a professional content analyst. "
                    "Summarize content in 2-3 sentences. "
                    "Do not mention HTML, website, or code. "
                    "Focus on the actual meaning and key insights."
                )
            },
            {
                "role": "user",
                "content": text[:4000]  # prevent overflow
            }
        ],
        "temperature": 0.3,
        "max_tokens": 150
    }

    for _ in range(3):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)

            if response.status_code != 200:
                print(f"DEBUG: HF API ERROR {response.status_code}: {response.text}")
                time.sleep(2)
                continue

            data = response.json()
            return data["choices"][0]["message"]["content"]

        except Exception as e:
            print(f"DEBUG: Exception during summarization: {str(e)}")
            time.sleep(2)

    return "Error: Failed to generate summary after multiple attempts. Check server logs."
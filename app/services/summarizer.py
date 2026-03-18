import requests
import os
import time

HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = os.getenv("HF_MODEL", "google/flan-t5-large")

API_URL = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

def summarize(text: str):
    if not text or len(text.strip()) < 10:
        return "The system could not extract enough meaningful text."

    # 🔥 YOUR PROMPT MOVED HERE
    prompt = (
        "You are a professional content analyst.\n"
        "Summarize the following content in 2-3 sentences.\n\n"
        "Rules:\n"
        "- Do NOT mention HTML, website, styles, or code.\n"
        "- Focus on the actual meaning and key takeaways.\n"
        "- If it's a portfolio, describe the person's role and expertise.\n"
        "- Start directly with the summary.\n\n"
        f"Content:\n{text}"
    )

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.3
        }
    }

    for _ in range(3):
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code != 200:
            time.sleep(2)
            continue

        data = response.json()

        if isinstance(data, list):
            return data[0].get("generated_text")

        if isinstance(data, dict) and "error" in data:
            time.sleep(2)
            continue

    return "Error: Failed to generate summary"
import requests
from app.core.config import HF_API_KEY, HF_MODEL

def summarize(text: str) -> str:
    """Sends content to the Hugging Face Inference API for summarization."""
    if not text or len(text.strip()) < 10:
        return "Insufficient content to provide a meaningful summary."

    if not HF_API_KEY:
        return "Error: Hugging Face API key is not configured. Please set the HF_API_KEY secret."

    api_url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    
    payload = {
        "inputs": text,
        "parameters": {"max_length": 150, "min_length": 40, "do_sample": False}
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        
        # Handle specifically for "Model is loading" which is common in HF free tier
        if response.status_code == 503:
            return "Error: The model is currently loading on Hugging Face. Please try again in a few seconds."

        if response.status_code != 200:
            return f"Error: Inference failed with status {response.status_code}: {response.text}"
            
        result = response.json()
        
        # BART/T5 usually return a list with a single dictionary
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("summary_text", "Failed to parse summary.")
            
        return str(result)
        
    except Exception as e:
        return f"Error: Summarization failed - {str(e)}"
import requests
from app.core.config import OLLAMA_URL

def summarize(text: str):
    if not text or len(text.strip()) < 10:
        return "The system could not extract enough meaningful text from this URL to provide a summary. The site may be protected or content-minimal."
    try:
        # We hook into a local Llama instance for processing.
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama2",
                "prompt": (
                    "SYSTEM: You are a professional content analyst. Your task is to summarize the ACTUAL SUBSTANCE of the provided text. "
                    "USER: Summarize the following content in 2-3 sentences. "
                    "RULES:\n"
                    "- DO NOT mention the words 'HTML', 'website', 'document', 'styles', or 'code'.\n"
                    "- DO NOT describe the webpage structure.\n"
                    "- FOCUS ON THE MESSAGE: Who is the person? What is the article about? What are the key takeaways?\n"
                    "- If the content is a professional portfolio, summarize the individual's expertise and role.\n"
                    "- START DIRECTLY with the summary. Output ONLY the summary.\n\n"
                    f"CONTENT TO SUMMARIZE:\n{text}"
                ),
                "stream": False
            },
            timeout=60
        )
        
        if response.status_code != 200:
            error_msg = f"Inference failed with status {response.status_code}: {response.text}"
            print(error_msg)
            return f"Error: {error_msg}"
            
        data = response.json()
        if "response" not in data:
            error_msg = f"Unexpected payload from inference engine: {data}"
            print(error_msg)
            return f"Error: {error_msg}"
            
        return data["response"]
    except requests.exceptions.RequestException as e:
        error_msg = f"Connection to inference engine failed: {str(e)}"
        print(error_msg)
        return f"Error: {error_msg}"
    except Exception as e:
        error_msg = f"Processing error: {str(e)}"
        print(error_msg)
        return f"Error: {error_msg}"
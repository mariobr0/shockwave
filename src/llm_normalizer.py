import requests
import config

class LLMNormalizer:
    def normalize(self, text):
        if not text:
            return ""
            
        headers = {
            "Content-Type": "application/json"
        }
        if config.LLM_API_KEY:
            headers["Authorization"] = f"Bearer {config.LLM_API_KEY}"
            
        user_prompt = f"Raw transcript to punctuate and format (return ONLY the corrected text):\n{text}"
        
        payload = {
            "model": config.LLM_MODEL,
            "messages": [
                {"role": "system", "content": config.STT_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 1024,
            "temperature": 0.1
        }
        
        try:
            response = requests.post(config.LLM_ENDPOINT, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            normalized = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return normalized.strip() if normalized else text
        except requests.exceptions.RequestException as e:
            print(f"LLM API Error: {e}")
            return text  # Fallback to raw text
        except Exception as e:
            print(f"Unknown LLM Error: {e}")
            return text

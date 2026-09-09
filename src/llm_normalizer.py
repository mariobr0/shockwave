import requests
import config

class LLMNormalizer:
    def normalize(self, text, translate_en=False, ai_task=False):
        if not text:
            return ""
            
        red = "\033[38;2;231;76;60m"
        reset = "\033[0m"

        if not config.LLM_ENDPOINT:
            print(f"{red}Notice: LLM Endpoint is not configured. Returning raw transcript.{reset}")
            return text
            
        headers = {
            "Content-Type": "application/json"
        }
        if config.LLM_API_KEY:
            headers["Authorization"] = f"Bearer {config.LLM_API_KEY}"
            
        user_prompt = f"Raw transcript to process:\n{text}"
        
        # Select active system prompt & status message based on mode toggles
        if translate_en and ai_task:
            system_prompt = getattr(config, "LLM_PROMPT_AI_TASK_EN", config.DEFAULT_AI_TASK_EN_PROMPT)
            action_name = "Generating AI task (EN)"
        elif ai_task:
            system_prompt = getattr(config, "LLM_PROMPT_AI_TASK", config.DEFAULT_AI_TASK_PROMPT)
            action_name = "Generating AI task"
        elif translate_en:
            system_prompt = getattr(config, "LLM_PROMPT_TRANSLATE_EN", config.DEFAULT_TRANSLATE_EN_PROMPT)
            action_name = "Translating to EN"
        else:
            system_prompt = config.STT_SYSTEM_PROMPT
            action_name = "Normalizing"
        
        model_name = getattr(config, "LLM_MODEL", "gemini-2.5-flash-lite")
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 1024,
            "temperature": 0.1
        }
        
        print(f"{action_name} with {model_name}... ", end="", flush=True)
        
        timeout_sec = getattr(config, "LLM_TIMEOUT", 25)
        try:
            response = requests.post(config.LLM_ENDPOINT, json=payload, headers=headers, timeout=timeout_sec)
            if not response.ok:
                err_detail = ""
                try:
                    err_json = response.json()
                    err_detail = err_json.get("error", {}).get("message") or str(err_json)
                except Exception:
                    err_detail = response.text.strip()[:200]
                print(f"{red}Failed (HTTP {response.status_code}: {err_detail}){reset}")
                return text
                
            data = response.json()
            normalized = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            if normalized and normalized.strip():
                # Guardrail: detect provider warning/error messages returned under HTTP 200
                suspicious_phrases = [
                    "is no longer available",
                    "please switch to",
                    "model is deprecated",
                    "model not found"
                ]
                lower_norm = normalized.lower()
                lower_orig = text.lower()
                detected = next((p for p in suspicious_phrases if p in lower_norm and p not in lower_orig), None)
                if detected:
                    clean_msg = normalized.replace("\n", " ").strip()[:90]
                    print(f"{red}Failed (Provider: {clean_msg}){reset}")
                    return text
                    
                print("Success")
                return normalized.strip()
            else:
                print(f"{red}Failed (Model returned empty response){reset}")
                return text
                
        except requests.exceptions.Timeout:
            print(f"{red}Failed (Connection timeout: server did not respond within {timeout_sec}s){reset}")
            return text
        except requests.exceptions.ConnectionError:
            print(f"{red}Failed (Connection error: unable to reach endpoint {config.LLM_ENDPOINT}){reset}")
            return text
        except requests.exceptions.RequestException as e:
            print(f"{red}Failed ({e}){reset}")
            return text
        except Exception as e:
            print(f"{red}Failed ({e}){reset}")
            return text

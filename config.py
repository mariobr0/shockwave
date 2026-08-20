import os
from dotenv import load_dotenv

load_dotenv()

STT_ENGINE = os.getenv("STT_ENGINE", "whisper")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "large-v3-turbo")
WHISPER_MODEL_PATH = os.getenv("WHISPER_MODEL_PATH", "")
GIGAAM_MODEL_PATH = os.getenv("GIGAAM_MODEL_PATH", "")
GIGAAM_QUANTIZATION = os.getenv("GIGAAM_QUANTIZATION", "")

LLM_ENDPOINT = os.getenv("LLM_ENDPOINT", "http://127.0.0.1:8045/v1/chat/completions")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-3.1-flash-lite")

HOTKEY = os.getenv("HOTKEY", "f12")
UI_POSITION = os.getenv("UI_POSITION", "bottom-left")

AUDIO_TEMP_FILE = "temp_audio.wav"

# Prompt
STT_SYSTEM_PROMPT = """Перепиши текст с исправлением ошибок.
Удали слова-паразиты и лишние звуки.
Сохраняй технические термины и код на английском.
Ничего другого не меняй. Перевод не делай.

КРИТИЧЕСКИЕ ИСПРАВЛЕНИЯ ТЕРМИНОВ:
- "докер" -> "Docker"
- "джейсон" -> "JSON"
- "реактом" -> "React"
- "тайпскрипт" -> "TypeScript"
- "гит" / "гид" -> "Git"
- "асинк" -> "async"
- "кэш" -> "cache"
"""

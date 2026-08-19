import os
from dotenv import load_dotenv

load_dotenv()

SOX_PATH = os.getenv("SOX_PATH", r"C:\Program Files (x86)\sox-14-4-2\sox.exe")
WHISPER_PATH = os.getenv("WHISPER_PATH", r"C:\tools\whisper\whisper-cli.exe")
MODEL_PATH = os.getenv("MODEL_PATH", r"C:\Users\dzam\.local\share\whisper-cpp\ggml-large-v3-turbo-q5_0.bin")

LLM_ENDPOINT = os.getenv("LLM_ENDPOINT", "http://127.0.0.1:8045/v1/chat/completions")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-3.1-flash-lite")

HOTKEY = os.getenv("HOTKEY", "f12")
UI_POSITION = os.getenv("UI_POSITION", "bottom-left")

AUDIO_TEMP_FILE = "temp_audio.wav"
TXT_OUTPUT_FILE = "temp_audio"  # Whisper appends .txt

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

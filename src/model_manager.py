import os
import sys

# Отключаем предупреждения Hugging Face
os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

import config

from huggingface_hub import constants
from faster_whisper import download_model
from dotenv import set_key, load_dotenv

def get_env_path():
    cwd_env = os.path.abspath(".env")
    if os.path.exists(cwd_env):
        return cwd_env
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
        exe_env = os.path.join(exe_dir, ".env")
        if os.path.exists(exe_env):
            return exe_env
        parent_env = os.path.abspath(os.path.join(exe_dir, "..", ".env"))
        if os.path.exists(parent_env):
            return parent_env
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    candidate = os.path.join(root_dir, ".env")
    if os.path.exists(candidate):
        return candidate
    return ".env"

def update_env(key, value):
    env_path = get_env_path()
    if not os.path.exists(env_path):
        with open(env_path, "w", encoding="utf-8") as f:
            f.write("\n")
    set_key(env_path, key, value)
    load_dotenv(env_path, override=True)
    os.environ[key] = str(value)
    setattr(config, key, value)

def check_and_prompt(auto_start=True):
    whisper_model = os.getenv("WHISPER_MODEL", config.WHISPER_MODEL)
    gigaam_model = os.getenv("GIGAAM_MODEL", config.GIGAAM_MODEL)
    engine = (os.getenv("STT_ENGINE") or config.STT_ENGINE).lower()
    hub_cache = os.environ.get("HF_HUB_CACHE", constants.HF_HUB_CACHE)
    
    needs_download = False
    
    if engine == "whisper" and not config.WHISPER_MODEL_PATH:
        try:
            download_model(whisper_model, local_files_only=True, cache_dir=hub_cache)
        except Exception:
            needs_download = True
            
    if engine == "gigaam" and not config.GIGAAM_MODEL_PATH:
        cache_dir = os.path.join(hub_cache, "models--istupakov--gigaam-v3-onnx")
        if not os.path.exists(cache_dir):
            needs_download = True

    if not needs_download:
        if not auto_start:
            print("\n✅ Выбранная модель уже загружена локально и готова к работе!")
        return
        
    print("\n" + "="*65)
    print("  ОБНАРУЖЕНО ОТСУТСТВИЕ МОДЕЛИ РАСПОЗНАВАНИЯ РЕЧИ")
    print("="*65)
    print(f"Выбранный движок [{engine.upper()}] не найден локально.")
    print(f"Все загрузки будут сохранены в папку проекта: \n{config.MODELS_DIR}")
    print("-"*65)
    print("Какую модель вы хотите скачать сейчас?")
    print(f"  1. Только Whisper ({whisper_model}) [~800 МБ] - Для IT терминов")
    print(f"  2. Только GigaAM (gigaam-v3-onnx)  - Быстрый русский")
    print("  3. Скачать обе модели")
    print("  4. Отмена")
    print("="*65)
    
    while True:
        choice = input("Ваш выбор (1-4): ").strip()
        if choice in ["1", "2", "3", "4"]:
            break
        print("Пожалуйста, введите число от 1 до 4.")
        
    if choice == "4":
        if auto_start:
            print("Выход из программы...")
            sys.exit(0)
        else:
            return
            
    quant_choice = ""
    if choice in ["2", "3"]:
        print("\n" + "-"*65)
        print("Какое качество для GigaAM вы хотите использовать?")
        print("  1. Сжатая (INT8) ~ 216 МБ (Очень быстрая, рекомендуется)")
        print("  2. Полная (Float32) ~ 885 МБ (Максимальное качество)")
        while True:
            q_ans = input("Ваш выбор (1-2): ").strip()
            if q_ans in ["1", "2"]:
                break
            print("Введите 1 или 2.")
        if q_ans == "1":
            quant_choice = "int8"
            
    if choice in ["1", "3"]:
        print(f"\n📥 Загрузка Whisper ({whisper_model}) в {config.MODELS_DIR}...")
        download_model(whisper_model, cache_dir=hub_cache)
        if choice == "1" and engine != "whisper":
            update_env("STT_ENGINE", "whisper")
            print("Настройка в .env автоматически изменена на STT_ENGINE=whisper")
            
    if choice in ["2", "3"]:
        q_text = quant_choice if quant_choice else "None"
        print(f"\n📥 Загрузка GigaAM ({gigaam_model}, quantization={q_text}) в {config.MODELS_DIR}...")
        import onnx_asr
        onnx_asr.load_model(gigaam_model, quantization=quant_choice if quant_choice else None)
        
        if choice == "2" and engine != "gigaam":
            update_env("STT_ENGINE", "gigaam")
            print("Настройка в .env автоматически изменена на STT_ENGINE=gigaam")
            
        update_env("GIGAAM_QUANTIZATION", quant_choice)

    print("\n✅ Все необходимые модели успешно скачаны в папку models/!\n")

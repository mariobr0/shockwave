import os
import sys

# Отключаем предупреждение об отсутствии токена Hugging Face
os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from huggingface_hub import constants
from faster_whisper import download_model
from dotenv import set_key

import config

def update_env(key, value):
    env_path = ".env"
    if not os.path.exists(env_path):
        with open(env_path, "w", encoding="utf-8") as f:
            f.write("\n")
    set_key(env_path, key, value)

def check_and_prompt(auto_start=True):
    whisper_model = config.WHISPER_MODEL
    gigaam_model = "gigaam-v3-e2e-rnnt"
    engine = config.STT_ENGINE.lower()
    
    needs_download = False
    
    if engine == "whisper" and not config.WHISPER_MODEL_PATH:
        try:
            download_model(whisper_model, local_files_only=True)
        except Exception:
            needs_download = True
            
    if engine == "gigaam" and not config.GIGAAM_MODEL_PATH:
        cache_dir = os.path.join(constants.HF_HUB_CACHE, "models--istupakov--gigaam-v3-onnx")
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
    print(f"Все загрузки будут сохранены в: \n{constants.HF_HUB_CACHE}")
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
        print(f"\n📥 Загрузка Whisper ({whisper_model})...")
        download_model(whisper_model)
        if choice == "1" and engine != "whisper":
            update_env("STT_ENGINE", "whisper")
            config.STT_ENGINE = "whisper"
            print("Настройка в .env автоматически изменена на STT_ENGINE=whisper")
            
    if choice in ["2", "3"]:
        q_text = quant_choice if quant_choice else "None"
        print(f"\n📥 Загрузка GigaAM ({gigaam_model}, quantization={q_text})...")
        import onnx_asr
        onnx_asr.load_model(gigaam_model, quantization=quant_choice if quant_choice else None)
        
        if choice == "2" and engine != "gigaam":
            update_env("STT_ENGINE", "gigaam")
            config.STT_ENGINE = "gigaam"
            print("Настройка в .env автоматически изменена на STT_ENGINE=gigaam")
            
        update_env("GIGAAM_QUANTIZATION", quant_choice)
        config.GIGAAM_QUANTIZATION = quant_choice

    print("\n✅ Все необходимые модели успешно скачаны!\n")


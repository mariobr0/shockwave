import os
import sys
import subprocess
from dotenv import load_dotenv, set_key

def get_env_path():
    return os.path.join(os.path.dirname(__file__), ".env")

def ensure_env_exists():
    env_path = get_env_path()
    if not os.path.exists(env_path):
        with open(env_path, "w", encoding="utf-8") as f:
            f.write("STT_ENGINE=whisper\n")
            f.write("WHISPER_MODEL=large-v3-turbo\n")
            f.write("LLM_ENDPOINT=http://127.0.0.1:8045/v1/chat/completions\n")
            f.write("LLM_API_KEY=\n")
            f.write("LLM_MODEL=gemini-3.1-flash-lite\n")
            f.write("HOTKEY=f12\n")
            f.write("UI_POSITION=bottom-left\n")

def read_env(key, default=""):
    load_dotenv(override=True)
    return os.getenv(key, default)

def update_env(key, value):
    env_path = get_env_path()
    set_key(env_path, key, value)
    load_dotenv(override=True)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def menu():
    ensure_env_exists()
    while True:
        clear_screen()
        engine = read_env("STT_ENGINE", "whisper").upper()
        llm_key = read_env("LLM_API_KEY", "")
        key_display = "Set" if llm_key else "NOT SET"
        llm_model = read_env("LLM_MODEL", "gemini-3.1-flash-lite")
        
        print("================================================")
        print("1. Запустить Shockwave (Старт)")
        print("2. Настроить API-ключ и LLM")
        print("3. Выбрать движок распознавания (STT)")
        print("4. Скачать/Проверить модели распознавания")
        print("5. Выход")
        print("================================================")
        
        choice = input("Ваш выбор: ").strip()
        
        if choice == "1":
            print("\nПроверка моделей перед запуском...")
            import model_manager
            # Передадим флаг, что мы запускаем из лаунчера
            model_manager.check_and_prompt(auto_start=True)
            
            print("\nЗапуск Shockwave... (Логи будут выводиться в этот терминал)")
            import main
            app = main.WinVoiceApp()
            app.run()
            sys.exit(0)
            
        elif choice == "2":
            setup_llm()
        elif choice == "3":
            setup_stt()
        elif choice == "4":
            import model_manager
            model_manager.check_and_prompt(auto_start=False)
            input("\nНажмите Enter, чтобы вернуться в меню...")
        elif choice == "5":
            sys.exit(0)

def setup_llm():
    clear_screen()
    print("--- Настройка LLM ---")
    current_key = read_env("LLM_API_KEY", "")
    print(f"Текущий ключ: {'Установлен' if current_key else 'Отсутствует'}")
    new_key = input("Введите новый API-ключ (или Enter, чтобы оставить без изменений): ").strip()
    if new_key:
        update_env("LLM_API_KEY", new_key)
        print("Ключ сохранен!")
        
    current_model = read_env("LLM_MODEL", "gemini-3.1-flash-lite")
    print(f"\nТекущая модель: {current_model}")
    new_model = input("Введите название модели (или Enter, чтобы оставить без изменений): ").strip()
    if new_model:
        update_env("LLM_MODEL", new_model)
        print("Модель сохранена!")
    
    input("\nНажмите Enter для возврата...")

def setup_stt():
    clear_screen()
    print("--- Выбор движка распознавания (STT) ---")
    print("1. Whisper (Отлично для смешанной речи и IT-терминов)")
    print("2. GigaAM (Очень быстро для чистой русской речи)")
    
    choice = input("\nВыберите движок (1-2): ").strip()
    if choice == "1":
        update_env("STT_ENGINE", "whisper")
        print("Установлен движок: Whisper")
    elif choice == "2":
        update_env("STT_ENGINE", "gigaam")
        print("Установлен движок: GigaAM")
        
    input("\nНажмите Enter для возврата...")

if __name__ == "__main__":
    menu()

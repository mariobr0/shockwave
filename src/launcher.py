import os
import sys
import subprocess
from dotenv import load_dotenv, set_key

# Enable UTF-8 encoding for console output
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Ensure modules from src import cleanly
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import config

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    candidate = os.path.join(root_path, relative_path)
    if os.path.exists(candidate):
        return candidate
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

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
        return cwd_env
        
    root_dir = os.path.abspath(os.path.join(current_dir, ".."))
    candidate = os.path.join(root_dir, ".env")
    if os.path.exists(candidate):
        return candidate
    return ".env"

def ensure_env_exists():
    env_path = get_env_path()
    if not os.path.exists(env_path):
        with open(env_path, "w", encoding="utf-8") as f:
            f.write("STT_ENGINE=gigaam\n")
            f.write("WHISPER_MODEL=large-v3-turbo\n")
            f.write("WHISPER_LANGUAGE=ru\n")
            f.write("GIGAAM_MODEL=gigaam-v3-e2e-rnnt\n")
            f.write("GIGAAM_QUANTIZATION=int8\n")
            f.write("APP_LANGUAGE=en\n")
            f.write("LLM_ENDPOINT=\n")
            f.write("LLM_API_KEY=\n")
            f.write("LLM_MODEL=gemini-2.5-flash-lite\n")
            f.write("HOTKEY=ctrl+space\n")
            f.write("UI_POSITION=bottom-left\n")

def read_env(key, default=""):
    env_path = get_env_path()
    load_dotenv(env_path, override=True)
    return os.getenv(key, default)

def update_env(key, value):
    env_path = get_env_path()
    set_key(env_path, key, value)
    load_dotenv(env_path, override=True)
    os.environ[key] = str(value)
    try:
        setattr(config, key, value)
    except Exception:
        pass

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    ansi_path = get_resource_path(os.path.join("icons", "shockwave_transparent.ansi"))
    if os.path.exists(ansi_path):
        try:
            with open(ansi_path, "r", encoding="utf-8") as f:
                lines = f.read().split("\n")
                pad = " " * 7
                for line in lines:
                    if line.strip():
                        print(pad + line)
        except Exception:
            pass
            
    # Iconic tagline centered in yellow (#FFD700)
    tagline = "WHAT IS YOUR COMMAND, MEGATRON?"
    yellow_quote = "\033[1;3;38;2;255;215;0m" + tagline + "\033[0m"
    print(f"          {yellow_quote}\n")

def menu():
    ensure_env_exists()
    
    # ANSI color codes
    PURPLE = "\033[38;2;180;95;235m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    while True:
        clear_screen()
        print_banner()
        
        lang = read_env("APP_LANGUAGE", "en").lower()
        engine = read_env("STT_ENGINE", "gigaam").lower()
        
        if engine == "whisper":
            whisper_m = read_env("WHISPER_MODEL", "large-v3-turbo")
            stt_display = f"Whisper ({whisper_m})"
        else:
            gigaam_m = read_env("GIGAAM_MODEL", "gigaam-v3-e2e-rnnt")
            quant = read_env("GIGAAM_QUANTIZATION", "int8")
            q_suffix = f", {quant}" if quant else ""
            stt_display = f"GigaAM ({gigaam_m}{q_suffix})"

        llm_endpoint = read_env("LLM_ENDPOINT", "")
        llm_model = read_env("LLM_MODEL", "gemini-2.5-flash-lite")
        llm_key = read_env("LLM_API_KEY", "")
        version = getattr(config, "APP_VERSION", "0.9.2")
        
        if lang == "ru":
            endpoint_display = llm_endpoint if llm_endpoint else "НЕ УСТАНОВЛЕН"
            key_display = f"{llm_key[:7]}...{llm_key[-4:]}" if len(llm_key) > 10 else (f"{llm_key[:4]}..." if llm_key else "НЕ УСТАНОВЛЕН")
            print(f"{PURPLE}{BOLD}===================================================={RESET}")
            print(f"      {PURPLE}{BOLD}SHOCKWAVE v{version} - ПАНЕЛЬ УПРАВЛЕНИЯ{RESET}")
            print(f"{PURPLE}{BOLD}===================================================={RESET}")
            print("Текущие настройки:")
            print(f"- STT Движок:   {stt_display}")
            print(f"- LLM Эндпоинт: {endpoint_display}")
            print(f"- LLM Модель:   {llm_model}")
            print(f"- Ключ LLM:     {key_display}")
            print(f"{PURPLE}{BOLD}===================================================={RESET}")
            print("1. Запустить Shockwave")
            print("2. Настроить API-ключ и LLM")
            print("3. Выбрать движок распознавания (STT)")
            print("4. Скачать/Проверить модели распознавания")
            print("5. Change language to English")
            print("6. Выход")
            print(f"{PURPLE}{BOLD}===================================================={RESET}")
            prompt_text = "Ваш выбор (1-6): "
        else:
            endpoint_display = llm_endpoint if llm_endpoint else "NOT SET"
            key_display = f"{llm_key[:7]}...{llm_key[-4:]}" if len(llm_key) > 10 else (f"{llm_key[:4]}..." if llm_key else "NOT SET")
            print(f"{PURPLE}{BOLD}===================================================={RESET}")
            print(f"       {PURPLE}{BOLD}SHOCKWAVE v{version} - CONTROL PANEL{RESET}")
            print(f"{PURPLE}{BOLD}===================================================={RESET}")
            print("Current Settings:")
            print(f"- STT Engine:   {stt_display}")
            print(f"- LLM Endpoint: {endpoint_display}")
            print(f"- LLM Model:    {llm_model}")
            print(f"- LLM Key:      {key_display}")
            print(f"{PURPLE}{BOLD}===================================================={RESET}")
            print("1. Start Shockwave")
            print("2. Configure API Key & LLM")
            print("3. Select STT Engine")
            print("4. Download / Verify STT Models")
            print("5. Сменить язык на русский")
            print("6. Exit")
            print(f"{PURPLE}{BOLD}===================================================={RESET}")
            prompt_text = "Your choice (1-6): "
        
        choice = input(prompt_text).strip()
        
        if choice == "1":
            if lang == "ru":
                print("\nПроверка моделей перед запуском...")
            else:
                print("\nChecking models before start...")
                
            import model_manager
            model_manager.check_and_prompt(auto_start=True)
            
            # Synchronize active engine in config
            config.STT_ENGINE = read_env("STT_ENGINE", "gigaam")
            
            if lang == "ru":
                print(f"\nЗапуск Shockwave ({stt_display})...")
            else:
                print(f"\nStarting Shockwave ({stt_display})...")
                
            import main
            app = main.WinVoiceApp()
            app.run()
            sys.exit(0)
            
        elif choice == "2":
            setup_llm(lang)
        elif choice == "3":
            setup_stt(lang)
        elif choice == "4":
            import model_manager
            model_manager.check_and_prompt(auto_start=False)
            if lang == "ru":
                input("\nНажмите Enter, чтобы вернуться в меню...")
            else:
                input("\nPress Enter to return to menu...")
        elif choice == "5":
            new_lang = "ru" if lang == "en" else "en"
            update_env("APP_LANGUAGE", new_lang)
        elif choice == "6":
            sys.exit(0)

def setup_llm(lang="en"):
    current_endpoint = read_env("LLM_ENDPOINT", "")
    current_key = read_env("LLM_API_KEY", "")
    current_model = read_env("LLM_MODEL", "gemini-2.5-flash-lite")
    
    if lang == "ru":
        print("\n--- Настройка LLM ---")
        print(f"Текущий эндпоинт: {current_endpoint if current_endpoint else 'Отсутствует'}")
        new_endpoint = input("Введите новый URL эндпоинта (или Enter, чтобы оставить): ").strip()
        if new_endpoint:
            update_env("LLM_ENDPOINT", new_endpoint)
            print("Эндпоинт сохранен!")
            
        key_info = f"{current_key[:7]}...{current_key[-4:]}" if len(current_key) > 10 else ("Установлен" if current_key else "Отсутствует")
        print(f"\nТекущий ключ: {key_info}")
        new_key = input("Введите новый API-ключ (или Enter, чтобы оставить): ").strip()
        if new_key:
            update_env("LLM_API_KEY", new_key)
            print("Ключ сохранен!")
            
        print(f"\nТекущая модель: {current_model}")
        new_model = input("Введите название модели (или Enter, чтобы оставить): ").strip()
        if new_model:
            update_env("LLM_MODEL", new_model)
            print("Модель сохранена!")
        input("\nНажмите Enter для возврата...")
    else:
        print("\n--- LLM Settings ---")
        print(f"Current Endpoint: {current_endpoint if current_endpoint else 'Not Set'}")
        new_endpoint = input("Enter new Endpoint URL (or press Enter to keep): ").strip()
        if new_endpoint:
            update_env("LLM_ENDPOINT", new_endpoint)
            print("Endpoint saved!")
            
        key_info = f"{current_key[:7]}...{current_key[-4:]}" if len(current_key) > 10 else ("Set" if current_key else "Not Set")
        print(f"\nCurrent API Key: {key_info}")
        new_key = input("Enter new API Key (or press Enter to keep): ").strip()
        if new_key:
            update_env("LLM_API_KEY", new_key)
            print("API Key saved!")
            
        print(f"\nCurrent Model: {current_model}")
        new_model = input("Enter model name (or press Enter to keep): ").strip()
        if new_model:
            update_env("LLM_MODEL", new_model)
            print("Model saved!")
        input("\nPress Enter to return...")

def setup_stt(lang="en"):
    whisper_m = read_env("WHISPER_MODEL", "large-v3-turbo")
    gigaam_m = read_env("GIGAAM_MODEL", "gigaam-v3-e2e-rnnt")
    
    if lang == "ru":
        print("\n--- Выбор движка распознавания (STT) ---")
        print(f"1. Whisper ({whisper_m}) — отлично для смешанной речи и IT-терминов")
        print(f"2. GigaAM ({gigaam_m}) — очень быстро для русской речи")
        choice = input("\nВыберите движок (1-2): ").strip()
        if choice == "1":
            update_env("STT_ENGINE", "whisper")
            print(f"Установлен движок: Whisper ({whisper_m})")
        elif choice == "2":
            update_env("STT_ENGINE", "gigaam")
            print(f"Установлен движок: GigaAM ({gigaam_m})")
        input("\nНажмите Enter для возврата...")
    else:
        print("\n--- Select STT Engine ---")
        print(f"1. Whisper ({whisper_m}) — great for mixed speech & IT terms")
        print(f"2. GigaAM ({gigaam_m}) — ultra-fast for Russian speech")
        choice = input("\nSelect engine (1-2): ").strip()
        if choice == "1":
            update_env("STT_ENGINE", "whisper")
            print(f"Selected engine: Whisper ({whisper_m})")
        elif choice == "2":
            update_env("STT_ENGINE", "gigaam")
            print(f"Selected engine: GigaAM ({gigaam_m})")
        input("\nPress Enter to return...")

if __name__ == "__main__":
    menu()

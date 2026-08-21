import os
import sys
import subprocess
from dotenv import load_dotenv, set_key

# Гарантируем, что модули из src корректно импортируются
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def get_env_path():
    # 1. Проверяем текущую рабочую директорию
    cwd_env = os.path.abspath(".env")
    if os.path.exists(cwd_env):
        return cwd_env
        
    # 2. Если запущен скомпилированный EXE (в dist/)
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
        exe_env = os.path.join(exe_dir, ".env")
        if os.path.exists(exe_env):
            return exe_env
        parent_env = os.path.abspath(os.path.join(exe_dir, "..", ".env"))
        if os.path.exists(parent_env):
            return parent_env
        return cwd_env
        
    # 3. Если запущен из исходников (src/launcher.py)
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
            f.write("GIGAAM_MODEL=gigaam-v3-e2e-rnnt\n")
            f.write("GIGAAM_QUANTIZATION=int8\n")
            f.write("LLM_ENDPOINT=http://127.0.0.1:8045/v1/chat/completions\n")
            f.write("LLM_API_KEY=\n")
            f.write("LLM_MODEL=gemini-2.5-flash-lite\n")
            f.write("HOTKEY=f12\n")
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
        import config
        setattr(config, key, value)
    except Exception:
        pass

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def menu():
    ensure_env_exists()
    while True:
        clear_screen()
        engine = read_env("STT_ENGINE", "gigaam").lower()
        if engine == "whisper":
            whisper_m = read_env("WHISPER_MODEL", "large-v3-turbo")
            stt_display = f"Whisper ({whisper_m})"
        else:
            gigaam_m = read_env("GIGAAM_MODEL", "gigaam-v3-e2e-rnnt")
            quant = read_env("GIGAAM_QUANTIZATION", "int8")
            q_suffix = f", {quant}" if quant else ""
            stt_display = f"GigaAM ({gigaam_m}{q_suffix})"

        llm_model = read_env("LLM_MODEL", "gemini-2.5-flash-lite")
        llm_key = read_env("LLM_API_KEY", "")
        if llm_key:
            if len(llm_key) > 10:
                key_display = f"{llm_key[:7]}...{llm_key[-4:]}"
            else:
                key_display = f"{llm_key[:4]}..."
        else:
            key_display = "НЕ УСТАНОВЛЕН"
        
        print("================================================")
        print("          SHOCKWAVE - ПАНЕЛЬ УПРАВЛЕНИЯ         ")
        print("================================================")
        print("Текущие настройки:")
        print(f"- STT Движок: {stt_display}")
        print(f"- LLM Модель: {llm_model}")
        print(f"- Ключ LLM:   {key_display}")
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
            model_manager.check_and_prompt(auto_start=True)
            
            # Синхронизируем перед запуском
            import config
            config.STT_ENGINE = read_env("STT_ENGINE", "gigaam")
            
            print(f"\nЗапуск Shockwave ({stt_display})...")
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
    key_info = f"{current_key[:7]}...{current_key[-4:]}" if len(current_key) > 10 else ("Установлен" if current_key else "Отсутствует")
    print(f"Текущий ключ: {key_info}")
    new_key = input("Введите новый API-ключ (или Enter, чтобы оставить без изменений): ").strip()
    if new_key:
        update_env("LLM_API_KEY", new_key)
        print("Ключ сохранен!")
        
    current_model = read_env("LLM_MODEL", "gemini-2.5-flash-lite")
    print(f"\nТекущая модель: {current_model}")
    new_model = input("Введите название модели (или Enter, чтобы оставить без изменений): ").strip()
    if new_model:
        update_env("LLM_MODEL", new_model)
        print("Модель сохранена!")
    
    input("\nНажмите Enter для возврата...")

def setup_stt():
    clear_screen()
    print("--- Выбор движка распознавания (STT) ---")
    whisper_m = read_env("WHISPER_MODEL", "large-v3-turbo")
    gigaam_m = read_env("GIGAAM_MODEL", "gigaam-v3-e2e-rnnt")
    print(f"1. Whisper ({whisper_m}) — отлично для смешанной речи и IT-терминов")
    print(f"2. GigaAM ({gigaam_m}) — очень быстро для чистой русской речи")
    
    choice = input("\nВыберите движок (1-2): ").strip()
    if choice == "1":
        update_env("STT_ENGINE", "whisper")
        print(f"Установлен движок: Whisper ({whisper_m})")
    elif choice == "2":
        update_env("STT_ENGINE", "gigaam")
        print(f"Установлен движок: GigaAM ({gigaam_m})")
        
    input("\nНажмите Enter для возврата...")

if __name__ == "__main__":
    menu()

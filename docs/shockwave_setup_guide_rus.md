# Shockwave — Руководство по установке и использованию

---

## 🚀 Вариант 1. Быстрый старт (Без установки Python)

*Этот вариант подходит для большинства пользователей. Python и дополнительные программы устанавливать не требуется.*

1. **Скачайте готовый архив:**  
   Перейдите на страницу **[GitHub Releases](https://github.com/mariobr0/shockwave/releases)** и скачайте **`Shockwave-v0.9.2-Portable.zip`**.
2. **Распакуйте архив** в любую удобную папку (например, `C:\Shockwave`).
3. **Запустите `Shockwave.exe`**.
4. В открывшейся панели управления:
   * Нажмите **`4`** (`Скачать/Проверить модели`), чтобы программа скачала нейросеть Whisper и/или GigaAM в локальную папку `models/`.
   * Нажмите **`2`** (`Настроить API-ключ и LLM`), если хотите включить умную расстановку пунктуации через LLM.
5. Нажмите **`1. Запустить Shockwave`** — в углу экрана появится фиолетовый виджет.
6. Нажмите **Ctrl + Space** в любой программе, чтобы начать запись, и повторно — чтобы её завершить. Надиктуйте текст и вставьте результат (Ctrl + V).

---

## 🛠️ Вариант 2. Сборка из исходного кода

Если вы хотите запустить проект из исходников или модифицировать код под себя:

### 1. Требования
* Windows 10 / 11
* Python 3.10 или новее (при установке обязательно поставьте галочку **Add python.exe to PATH**)
* Git (опционально)

### 2. Клонирование и установка зависимостей
```bat
git clone https://github.com/mariobr0/shockwave.git
cd shockwave

python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Сборка `.exe` или прямой запуск
* **Сборка бинарника:** запустите **`build.bat`** (создаст `dist\Shockwave.exe` и ярлык `Shockwave.lnk`).
* **Прямой запуск через Python:** запустите **`start.bat`**.

---

## ⚙️ Настройка LLM (Нейросеть для пунктуации)

| Провайдер | Эндпоинт (`LLM_ENDPOINT`) | Модель (`LLM_MODEL`) | Где получить ключ |
| :--- | :--- | :--- | :--- |
| **Google AI Studio** | `https://generativelanguage.googleapis.com/v1beta/openai/chat/completions` | `gemini-2.5-flash-lite` | [aistudio.google.com](https://aistudio.google.com/) |
| **OpenAI** | `https://api.openai.com/v1/chat/completions` | `gpt-4o-mini` | [platform.openai.com](https://platform.openai.com/) |
| **OpenRouter** | `https://openrouter.ai/api/v1/chat/completions` | `google/gemini-2.5-flash-lite` | [openrouter.ai](https://openrouter.ai/) |
| **Ollama (Локально)** | `http://localhost:11434/v1/chat/completions` | `qwen2.5:7b` | Не требуется (оффлайн) |

---

## 🎛️ Настройка через `.env`

Параметры можно задать в файле `.env` (шаблон доступен в `.env.example`):
* `HOTKEY=ctrl+space` — системная комбинация клавиш.
* `WHISPER_LANGUAGE=ru` — язык распознавания Whisper (`ru`, `auto` для 99 языков, `en`, `de` и др.).
* `UI_POSITION=bottom-left` — начальная позиция виджета (`bottom-left`, `bottom-right`, `top-center`).

#### Выбор горячих клавиш:
* ✅ **Рекомендуемые:** `ctrl+space`, `alt+space`, `f9`, `f8`, `f10`, `pause`.
* ⚠️ **Не рекомендуемые:** `f12` (зарезервирована Windows Debugger), `f11` (полный экран), `f5` (обновление).

---

## 🖱️ Управление виджетом

* **Левая ручка (`⋮⋮`):** Зажмите левой кнопкой мыши для свободного перемещения плашки по экрану.
* **Глаз Shockwave (🟡):** Кликабельная кнопка включения/выключения записи с визуальной индикацией (горит жёлтым при работе).
* **Чекбокс `LLM norm`:** Включение/выключение нормализации текста через нейросеть.
* **Чекбокс `alert`:** Включение/выключение звукового сигнала по завершении распознавания.
* **Кнопка `×`:** Закрытие программы.

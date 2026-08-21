<p align="center">
  <img src="docs/shockwave.gif" alt="Shockwave">
</p>

# Shockwave

*(Описание на русском ниже)*

**Shockwave** is an open-source, local-first background voice dictation tool for Windows. It allows you to dictate text via a global hotkey or by clicking the on-screen glowing eye, automatically normalizes punctuation and tech terminology using an LLM, and copies the resulting text directly to your clipboard.

### Speech Recognition Models (STT):
- **Whisper (`large-v3-turbo`)**: State-of-the-art turbo model by OpenAI, optimized for speed. Ideal for mixed English/Russian speech and programming terminology. Runs locally via `faster-whisper`.
- **GigaAM (`gigaam-v3-e2e-rnnt`)**: ONNX version of Sber's GigaAM acoustic model, ported by Ilya Stupakov for fast CPU execution. Runs in `int8` or `float32` format via `onnx-asr`.

### Text Normalization Engine (LLM):
- **Gemini (`gemini-2.5-flash-lite`) / OpenAI Compatible**: Lightweight, fast AI model used for punctuation restoration, formatting, and technical term capitalization.

## Features
* **Rock-Solid System Hotkey:** Native Win32 `RegisterHotKey` (Default `Ctrl + Space`). Never drops out after system sleep, lock screen, or long background sessions.
* **Interactive Shockwave Eye:** Interactive glowing eye button on the widget that ignites in vibrant yellow (`#FFD700`) during recording. Click-to-record supported!
* **Dual Speech-to-Text (STT):** Choose between Whisper (mixed IT speech) and GigaAM (ultra-fast Russian speech).
* **Fully Portable & Compact Storage:** Flat directory structure saves weights locally in `models/` with zero bloat (only ~1.76 GB for both neural networks).
* **Draggable Floating Widget:** Minimalist on-screen overlay that can be smoothly repositioned across any screen using the left grip handle (`⋮⋮`).
* **Permanent Taskbar Presence:** Clean window lifecycle with permanent icon visibility on Windows Taskbar and smooth flicker-free startup.
* **Bilingual Interactive Launcher:** Console control panel supporting language switching (English / Russian), model management, and transparent API configuration.
* **Audio Notifications:** Subtle sound notification plays when transcription is copied and ready to paste.
* **Safe Terminal Logging:** The console maintains a real-time transcript history to ensure no dictated text is lost.

## Documentation & Installation
Detailed guides are available below:

🇬🇧 **[Setup Guide (English)](docs/shockwave_setup_guide_eng.md)**  
🇷🇺 **[Руководство по настройке (Русский)](docs/shockwave_setup_guide_rus.md)**

---

# Shockwave

**Shockwave** — это легковесный инструмент для голосовой диктовки на Windows, работающий в фоновом режиме. Он позволяет надиктовывать текст по нажатию глобальной горячей клавиши или клику по светящемуся глазу на панели, автоматически расставляет знаки препинания с помощью нейросети и копирует результат в буфер обмена.

### Модели распознавания речи (STT):
- **Whisper (`large-v3-turbo`)**: Новая турбо-версия большой модели Whisper от OpenAI. Идеальна для смешанной русско-английской речи и IT-терминов. Запускается локально через `faster-whisper`.
- **GigaAM (`gigaam-v3-e2e-rnnt`)**: ONNX-версия нейросети GigaAM от Сбера, портированная Ильей Ступаковым для работы на процессорах. Загружается в версии `int8` или `float32` через `onnx-asr`.

### Движок нормализации текста (LLM):
- **Gemini (`gemini-2.5-flash-lite`) / OpenAI-совместимый**: Быстрая языковая модель от Google для восстановления пунктуации, форматирования и исправления опечаток.

## Возможности
* **Надёжная системная горячая клавиша:** Работает через ядро Windows (`RegisterHotKey`, по умолчанию `Ctrl + Space`). Никогда не отваливается после сна или блокировки экрана.
* **Интерактивный «Глаз Shockwave»:** Светящийся глаз-кнопка на виджете, вспыхивающий ярко-жёлтым светом (`#FFD700`) во время записи. Поддерживает запуск диктовки кликом мыши!
* **Два движка распознавания (STT):** Быстрый выбор между Whisper (для смешанной IT-речи) и GigaAM (очень быстрый для русской речи).
* **Полная портативность и компактность:** Оптимизированная структура хранения моделей в `models/` без дубликатов (всего ~1.76 ГБ для двух моделей).
* **Перемещаемый виджет:** Аккуратная плашка статуса, которую можно свободно перетаскивать мышкой за левую ручку (`⋮⋮`) в любое место любого экрана.
* **Постоянная иконка в таскбаре:** Плавный запуск без мерцаний и постоянное отображение иконки приложения на панели задач Windows.
* **Двуязычная панель управления:** Консольный лаунчер с поддержкой переключения языка (RU / EN), проверки моделей и прозрачной настройки эндпоинта и ключа.
* **Звуковой сигнал:** Аудио-оповещение при успешном завершении диктовки.
* **Бекап-лог:** Консоль сохраняет лог и всю историю расшифровок в рамках открытой сессии.

## Документация и Установка
Подробные инструкции по установке:

🇬🇧 **[Setup Guide (English)](docs/shockwave_setup_guide_eng.md)**  
🇷🇺 **[Руководство по настройке (Русский)](docs/shockwave_setup_guide_rus.md)**
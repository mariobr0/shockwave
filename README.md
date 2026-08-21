# Shockwave

![Shockwave](shockwave.jpg)

*(Scroll down for Russian version)*

**Shockwave** is a background tool for voice dictation on Windows. It allows you to dictate text by pressing a global hotkey, corrects punctuation using an LLM, and copies the text to your clipboard.

A local alternative to tools like FluidVoice for Windows.

## Features
* **Global Hotkey:** Default `F12`. Works in any application.
* **Dual Speech-to-Text (STT):** Uses `faster-whisper` (for mixed English/Russian) or `GigaAM` (for ultra-fast Russian dictation). Both run locally and download automatically.
* **Normalization:** An LLM (e.g., Gemini or a local model) fixes typos, adds punctuation, and formats IT terms.
* **Interactive UI:** A floating widget with a checkbox to toggle AI correction on the fly.
* **Backup Log:** The console saves transcription history, preventing data loss.

## Documentation & Installation
Detailed instructions are available in the setup guides:

🇬🇧 **[Setup Guide (English)](shockwave_setup_guide_eng.md)**

---

# Shockwave (Русская версия)

**Shockwave** — это инструмент для голосовой диктовки на Windows, работающий в фоновом режиме. Он позволяет надиктовывать текст по нажатию глобальной клавиши, исправляет пунктуацию с помощью LLM и копирует текст в буфер обмена.

Локальная альтернатива FluidVoice для Windows.

## Возможности
* **Глобальная кнопка:** По умолчанию `F12`. Работает в любом приложении.
* **Два движка распознавания (STT):** Использует `faster-whisper` (отлично для смешанного англо-русского IT-кода) или `GigaAM` (очень быстрый для чистого русского языка). Оба работают локально.
* **Нормализация:** LLM (например, Gemini или локальная модель) расставляет запятые, исправляет опечатки и капитализирует термины.
* **Интерактивный UI:** Плавающий виджет с галочкой для включения/выключения ИИ-коррекции.
* **Бекап-лог:** Консоль сохраняет историю расшифровок, не позволяя потерять текст.

## Документация и Установка
Подробные инструкции по установке (простой через `.exe` и сложной из исходников) доступны здесь:

🇷🇺 **[Руководство по настройке (Русский)](shockwave_setup_guide_rus.md)**

---
*"What is your command, Megatron?"*

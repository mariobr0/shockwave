# Shockwave

![Shockwave](shockwave.jpg)

*(Scroll down for Russian version / Русская версия ниже)*

**Shockwave** is a background tool for voice dictation on Windows. It allows you to dictate text by pressing a global hotkey, corrects punctuation using an LLM, and copies the text to your clipboard.

A local alternative to tools like FluidVoice for Windows.

## 🚀 Features
* **Global Hotkey:** Default `F12`. Works in any application.
* **Dual Speech-to-Text (STT):** Uses `faster-whisper` (for mixed English/Russian code dictation) or `GigaAM` (for ultra-fast Russian dictation). Both run entirely in Python and download automatically.
* **Normalization:** An LLM (e.g., Gemini or a local model) fixes typos, adds punctuation, and capitalizes IT terms.
* **Interactive UI:** A floating widget with a checkbox to toggle AI correction on the fly, showing status indicators (*what is your command?* ➔ *record* ➔ *processing* ➔ *normalization* ➔ *ready*).
* **Backup Log:** The app's console saves the transcription history, preventing data loss if the clipboard is overwritten.

## 📖 Documentation & Installation
A step-by-step guide for setting up the environment, choosing the STT engine, and using the program:

🇬🇧 **[Setup Guide (English)](shockwave_setup_guide_eng.md)**

---

# Shockwave (Русская версия)

**Shockwave** - это инструмент для голосового ввода на Windows, работающий в фоновом режиме. Он позволяет надиктовывать текст по нажатию глобальной клавиши, исправляет пунктуацию с помощью LLM и копирует текст в буфер обмена.

Локальная альтернатива FluidVoice для Windows.

## 🚀 Возможности
* **Глобальная кнопка:** По умолчанию `F12`. Работает в любом приложении.
* **Двойной движок распознавания (STT):** Использует `faster-whisper` (идеален для смешанной русско-английской IT-речи) или `GigaAM` (очень быстрый для чистого русского текста). Запускаются полностью внутри Python и скачивают модели автоматически.
* **Нормализация:** LLM (например, Gemini или локальная модель) исправляет опечатки, расставляет знаки препинания и капитализирует IT-термины.
* **Интерактивный UI:** Плавающий виджет с галочкой для включения/выключения ИИ-коррекции и индикаторами статуса (*what is your command?* ➔ *record* ➔ *processing* ➔ *normalization* ➔ *ready*).
* **Бэкап-лог:** Консоль приложения сохраняет историю распознаваний, не позволяя потерять текст, если буфер обмена был затерт.

## 📖 Документация и установка
Пошаговое руководство по настройке окружения, выбору движка распознавания (STT) и использованию программы:

🇷🇺 **[Руководство по развертыванию (Русский)](shockwave_setup_guide_rus.md)**

---
*"What is your command, Megatron?"*

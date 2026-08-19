# Shockwave 🤖🎤

![Shockwave](shockwave.jpg)

*(Scroll down for Russian version / Русская версия ниже)*

**Shockwave** is a background tool for voice dictation on Windows. It allows you to dictate text by pressing a global hotkey, corrects punctuation using an LLM, and copies the text to your clipboard.

A local alternative to tools like FluidVoice for Windows.

## ✨ Features
* **Global Hotkey:** Default `F12`. Works in any application.
* **Local Speech-to-Text (STT):** Uses `whisper.cpp` for audio transcription.
* **Normalization:** An LLM (e.g., Gemini or a local model) fixes typos, adds punctuation, and capitalizes IT terms.
* **Interactive UI:** A floating widget with a checkbox to toggle AI correction on the fly, showing status indicators (*what is your command?* ➔ *record* ➔ *processing* ➔ *normalization* ➔ *ready*).
* **Backup Log:** The app's console saves the transcription history, preventing data loss if the clipboard is overwritten.

## 📚 Documentation & Installation
A step-by-step guide for installing dependencies (SoX, Whisper), setting up the LLM, and using the program:

👉 **[Setup Guide (English)](shockwave_setup_guide_eng.md)**

---

# Shockwave (Русская версия)

**Shockwave** — это инструмент для голосового ввода на Windows, работающий в фоновом режиме. Он позволяет надиктовывать текст по нажатию глобального хоткея, исправляет пунктуацию с помощью LLM и копирует текст в буфер обмена.

Локальная альтернатива FluidVoice для Windows.

## ✨ Особенности
* **Глобальный хоткей:** По умолчанию `F12`. Работает в любых приложениях.
* **Локальное распознавание (STT):** Использует `whisper.cpp` для транскрибации аудио.
* **Нормализация:** LLM (например, Gemini или локальная модель) исправляет опечатки, расставляет знаки препинания и капитализирует IT-термины.
* **Интерактивный UI:** Плавающий виджет с чекбоксом для включения/отключения ИИ-корректуры и отображением статусов (*what is your command?* ➔ *record* ➔ *processing* ➔ *normalization* ➔ *ready*).
* **Журнал-бэкап:** Консоль приложения сохраняет историю транскрипций, не позволяя потерять текст, если буфер обмена был затерт.

## 📚 Документация и Установка
Пошаговое руководство по установке зависимостей (SoX, Whisper), настройке нейросети и использованию программы:

👉 **[Руководство по установке (Русский)](shockwave_setup_guide_rus.md)**

---
*"What is your command, Megatron?"*

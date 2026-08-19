# Shockwave 🤖🎤

![Shockwave](shockwave.jpg)

*(Scroll down for Russian version / Русская версия ниже)*

**Shockwave** is a smart background tool for global voice dictation on Windows. It allows you to dictate text in any application by pressing a global hotkey, automatically corrects punctuation, cleans up filler words using an LLM, and instantly prepares the perfect text in your clipboard for pasting whenever you need it.

A great local Windows alternative to tools like FluidVoice.

## ✨ Features
* **Global Hotkey:** Default `F12`. Works everywhere—code editors, browsers, messengers. You can dictate even if no text field is currently selected.
* **Local Speech-to-Text (STT):** Uses `whisper.cpp` for fast and private audio transcription.
* **Smart Normalization:** Any LLM (e.g., Gemini or a local model) carefully fixes typos, adds punctuation, and capitalizes IT terms without shortening your original thought.
* **Interactive UI:** A neat, floating widget with a checkbox to quickly toggle AI correction on the fly, showing clear status indicators (*what is your command?* ➔ *record* ➔ *processing* ➔ *normalization* ➔ *ready*).
* **Backup Log:** The app's console saves your entire transcription history, preventing data loss if you accidentally overwrite your clipboard.

## 📚 Documentation & Installation
A full step-by-step guide for installing all dependencies (SoX, Whisper), setting up the neural network, and using the program can be found here:

👉 **[Setup & Deployment Guide (English)](shockwave_setup_guide_eng.md)**

---

# Shockwave (Русская версия)

**Shockwave** — это умный инструмент для глобального голосового ввода на Windows, работающий в фоновом режиме. Он позволяет вам надиктовывать текст в любом приложении по нажатию глобального хоткея, а затем автоматически исправляет пунктуацию, очищает речь от слов-паразитов с помощью LLM и моментально подготавливает идеальный текст в буфере обмена для вставки в любой нужный момент.

Отличная локальная Windows-альтернатива таким инструментам, как FluidVoice.

## ✨ Особенности
* **Глобальный хоткей:** По умолчанию `F12`. Работает везде — в редакторах кода, браузере, мессенджерах. Вы можете диктовать текст, даже если у вас не выбрано ни одного текстового поля.
* **Локальное распознавание (STT):** Использует `whisper.cpp` для быстрой и приватной транскрибации аудио.
* **Умная нормализация:** Любая LLM (например, Gemini или локальная модель) аккуратно исправляет опечатки, расставляет знаки препинания и капитализирует IT-термины, не сокращая вашу оригинальную мысль.
* **Интерактивный UI:** Аккуратный, плавающий виджет с чекбоксом для быстрого включения/отключения ИИ-корректуры на лету и наглядным отображением статусов (*what is your command?* ➔ *record* ➔ *processing* ➔ *normalization* ➔ *ready*).
* **Журнал-бэкап:** Консоль приложения сохраняет всю историю транскрипций, не позволяя вам потерять диктовку, если вы случайно затерли буфер обмена.

## 📚 Документация и Установка
Полное пошаговое руководство по установке всех зависимостей (SoX, Whisper), настройке нейросети и использованию программы находится здесь:

👉 **[Руководство по развертыванию (Русский)](shockwave_setup_guide_rus.md)**

---
*"What is your command, Megatron?"*

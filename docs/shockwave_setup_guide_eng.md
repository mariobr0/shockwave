# Shockwave — Setup & User Guide

---

## 🚀 Scenario 1. Quick Start (No Python Required)

*Recommended for most users. No Python or additional software installation needed.*

1. **Download the prebuilt archive:**  
   Go to the **[GitHub Releases](https://github.com/mariobr0/shockwave/releases)** page and download **`Shockwave-v0.9.2-Portable.zip`**.
2. **Extract the archive** to any folder (e.g., `C:\Shockwave`).
3. **Run `Shockwave.exe`**.
4. In the Control Panel:
   * Press **`4`** (`Download / Verify STT Models`) to let the application download the Whisper and/or GigaAM speech models into the local `models/` folder.
   * Press **`2`** (`Configure API Key & LLM`) if you wish to enable smart punctuation and formatting via an LLM.
5. Press **`1. Start Shockwave`** — a purple floating widget will appear in the corner of your screen.
6. Press **`Ctrl + Space`** in any application to start recording, and press it again to finish. Dictate your speech and paste the result (`Ctrl + V`).

---

## 🛠️ Scenario 2. Build from Source Code

If you prefer to run the project from source or modify the code:

### 1. Requirements
* Windows 10 / 11
* Python 3.10 or newer (make sure to check **Add python.exe to PATH** during installation)
* Git (optional)

### 2. Clone and Install Dependencies
```bat
git clone https://github.com/mariobr0/shockwave.git
cd shockwave

python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Build `.exe` or Run Directly
* **Build standalone binary:** run **`build.bat`** (generates `dist\Shockwave.exe` and shortcut `Shockwave.lnk`).
* **Direct Python launch:** run **`start.bat`**.

---

## ⚙️ LLM Configuration (Punctuation & Formatting)

| Provider | Endpoint URL (`LLM_ENDPOINT`) | Model Name (`LLM_MODEL`) | API Key Source |
| :--- | :--- | :--- | :--- |
| **Google AI Studio** | `https://generativelanguage.googleapis.com/v1beta/openai/chat/completions` | `gemini-2.5-flash-lite` | [aistudio.google.com](https://aistudio.google.com/) |
| **OpenAI** | `https://api.openai.com/v1/chat/completions` | `gpt-4o-mini` | [platform.openai.com](https://platform.openai.com/) |
| **OpenRouter** | `https://openrouter.ai/api/v1/chat/completions` | `google/gemini-2.5-flash-lite` | [openrouter.ai](https://openrouter.ai/) |
| **Ollama (Local)** | `http://localhost:11434/v1/chat/completions` | `qwen2.5:7b` | Not needed (offline) |

---

## 🎛️ Configuration via `.env`

Parameters can be configured in `.env` (template available in `.env.example`):
* `HOTKEY=ctrl+space` — global system hotkey.
* `WHISPER_LANGUAGE=ru` — Whisper recognition language (`ru`, `auto` for 99 languages, `en`, `de`, etc.).
* `UI_POSITION=bottom-left` — initial widget position (`bottom-left`, `bottom-right`, `top-center`).

#### Recommended Hotkeys:
* ✅ **Recommended:** `ctrl+space`, `alt+space`, `f9`, `f8`, `f10`, `pause`.
* ⚠️ **Not recommended:** `f12` (reserved by Windows Debugger), `f11` (browser fullscreen), `f5` (page reload).

---

## 🖱️ Widget Controls

* **Left grip handle (`⋮⋮`):** Click and drag with mouse to reposition the widget anywhere on your desktop.
* **Shockwave Eye (🟡):** Clickable recording button with visual state indication (glows solid yellow during recording).
* **`LLM norm` checkbox:** Toggle AI-based text punctuation and formatting.
* **`alert` checkbox:** Toggle audio chime notification on transcription completion.
* **`×` button:** Exit application.

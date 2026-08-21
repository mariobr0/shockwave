# Shockwave — Setup & User Guide

---

## 🚀 Scenario 1. Quick Start (NO Python Required)

*Recommended for most users. No Python or development tools needed.*

1. **Download the prebuilt release:**  
   Go to **[GitHub Releases](https://github.com/mariobr0/shockwave/releases)** and download **`Shockwave-v0.9.2-Portable.zip`** (or `Shockwave.exe`).
2. **Extract the archive** to any folder (e.g. `C:\Shockwave`).
3. **Double-click `Shockwave.exe`** to launch.
4. In the Control Panel:
   * Press **`4`** (`Download / Verify STT Models`) to let the app download Whisper or GigaAM models into the local `models/` folder.
   * Press **`2`** (`Configure API Key & LLM`) if you wish to enable smart AI punctuation via Google AI Studio, OpenAI, or Ollama.
5. Press **`1. Start Shockwave`** — a purple floating widget will appear on your desktop.
6. **Done!** Press **`Ctrl + Space`** anywhere in Windows, dictate your speech, and paste the result (`Ctrl + V`).

---

## 🛠️ Scenario 2. Build from Source (For Developers)

If you prefer to run from source code or modify the application:

### 1. Requirements
* Windows 10 / 11
* Python 3.10, 3.11, or 3.12 (ensure **Add python.exe to PATH** is checked during installation)
* Git (optional)

### 2. Clone & Install Dependencies
```bat
git clone https://github.com/mariobr0/shockwave.git
cd shockwave

python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Build `.exe` or Run Directly
* **Compile standalone binary:** run **`build.bat`** (generates `dist\Shockwave.exe` and `Shockwave.lnk`).
* **Direct Python launch:** run **`start.bat`**.

---

## ⚙️ LLM Configuration (Punctuation & Formatting)

| Provider | Endpoint URL (`LLM_ENDPOINT`) | Model Name (`LLM_MODEL`) | API Key Source |
| :--- | :--- | :--- | :--- |
| **Google AI Studio** *(Recommended)* | `https://generativelanguage.googleapis.com/v1beta/openai/chat/completions` | `gemini-2.5-flash-lite` | [aistudio.google.com](https://aistudio.google.com/) (Free) |
| **OpenAI** | `https://api.openai.com/v1/chat/completions` | `gpt-4o-mini` | [platform.openai.com](https://platform.openai.com/) |
| **OpenRouter** | `https://openrouter.ai/api/v1/chat/completions` | `google/gemini-2.5-flash-lite` | [openrouter.ai](https://openrouter.ai/) |
| **Ollama (Local)** | `http://localhost:11434/v1/chat/completions` | `qwen2.5:7b` | Not needed (offline) |

---

## 🎛️ Advanced Configuration via `.env` (Optional)

Customize settings in `.env` (template in `.env.example`):
* `HOTKEY=ctrl+space` — global system hotkey.
* `WHISPER_LANGUAGE=ru` — Whisper language (`ru`, `auto` for 99 languages, `en`, `de`, etc.).
* `UI_POSITION=bottom-left` — widget position (`bottom-left`, `bottom-right`, `top-center`).

#### Recommended Hotkeys:
* ✅ **Recommended:** `ctrl+space`, `alt+space`, `f9`, `f8`, `f10`, `pause`.
* ⚠️ **Not recommended:** `f12` (reserved by Windows Debugger), `f11` (browser fullscreen), `f5` (reload).

---

## 🖱️ Widget Controls

* **Left grip handle (`⋮⋮`):** Click and drag with mouse to reposition the widget anywhere on your desktop.
* **Shockwave Eye (🟡):** Interactive recording button with visual state color indicators (solid yellow during recording).
* **`LLM norm` checkbox:** Toggle AI-based punctuation and typo correction.
* **`alert` checkbox:** Toggle audio chime notification on completion.
* **`×` button:** Exit application.

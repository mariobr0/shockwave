# Shockwave — Setup & User Guide

### 1. Requirements
* Windows 10 / 11
* Python 3.10+

---

### 2. Installation & Build
1. Clone the repository or download the source archive:
   ```bat
   git clone https://github.com/mariobr0/shockwave.git
   cd shockwave
   ```
2. Create a virtual environment and install dependencies:
   ```bat
   python -m venv venv
   call venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run the build script:
   ```bat
   build.bat
   ```
   The script compiles `dist\Shockwave.exe` and creates the `Shockwave.lnk` shortcut in the project root.

*(Note: If you prefer not to compile an `.exe`, you can run the application directly via Python by double-clicking **`start.bat`**).*

---

### 3. First Launch & Configuration
1. Launch `Shockwave.lnk` (or `start.bat`).
2. In the Control Panel:
   * **Option 2 (`Configure API Key & LLM`):** Set Endpoint URL, API Key, and Model name.
   * **Option 3 (`Select STT Engine`):** Choose `Whisper` (for code / mixed speech) or `GigaAM` (for Russian speech).
   * **Option 4 (`Download / Verify STT Models`):** Download the selected model weights into the local `models/` directory.
   * **Option 5 (`Сменить язык на русский`):** Toggle interface language if needed.

#### Common LLM Endpoints:
| Provider | Endpoint URL (`LLM_ENDPOINT`) | Model Name (`LLM_MODEL`) |
| :--- | :--- | :--- |
| **Google AI Studio** | `https://generativelanguage.googleapis.com/v1beta/openai/chat/completions` | `gemini-2.5-flash-lite` |
| **OpenAI** | `https://api.openai.com/v1/chat/completions` | `gpt-4o-mini` |
| **OpenRouter** | `https://openrouter.ai/api/v1/chat/completions` | `google/gemini-2.5-flash-lite` |
| **Ollama (Local)** | `http://localhost:11434/v1/chat/completions` | `qwen2.5:7b` |

---

### 4. Advanced Configuration via `.env` (Optional)
You can customize additional parameters in `.env` (template provided in `.env.example`):
* `WHISPER_LANGUAGE=ru` — Whisper recognition language (`ru`, `auto` for auto-detecting 99 languages, `en`, `de`, etc.).
* `HOTKEY=f12` — recording hotkey (e.g. `f9`, `ctrl+space`, `alt+v`).
* `UI_POSITION=bottom-left` — floating widget screen position (`bottom-left`, `bottom-right`, `top-center`).

---

### 5. Usage
1. In the menu, select **`1. Start Shockwave`** — a floating widget will appear on screen.
2. Press **`F12`** in any application and speak your text.
3. Press **`F12`** again to finish recording.
4. When the status displays **`ready`** (accompanied by a chime), the formatted text is already in your clipboard (`Ctrl + V`).

---

### 6. Widget Controls
* **Left grip handle (`⋮⋮`):** Click and drag with mouse to reposition the widget anywhere on your desktop.
* **`LLM norm` checkbox:** Toggle AI-based punctuation and typo correction.
* **`alert` checkbox:** Toggle audio chime notification on completion.
* **`×` button:** Exit application.

# Shockwave (v0.9.0) — Setup & User Guide

## Option 1. Quick Start (Standalone Executable)

The fastest and easiest way to use Shockwave without installing Python or configuring virtual environments manually.

### Step 1: Launch
1. Double-click `Shockwave.lnk` (the root shortcut) or run `dist\Shockwave.exe`.
2. The interactive **Shockwave Control Panel** will open in the console.

### Step 2: Configure API Key & LLM
In the Control Panel, select option **`2. Configure API Key & LLM`**:
* Enter your LLM API Key (e.g. Google Gemini API key).
* Choose or leave the default model `gemini-2.5-flash-lite`.
* Settings are automatically saved into your local `.env` file.

### Step 3: Select and Download STT Models
1. Choose option **`3. Select STT Engine`**:
   * **Whisper** — Recommended for mixed English/Russian speech, coding terms, and acronyms.
   * **GigaAM** — Recommended for ultra-fast Russian speech.
2. Select option **`4. Download / Verify STT Models`** to download required weights directly into the project's local `models/` directory.

### Step 4: Start Dictating
1. Choose option **`1. Start Shockwave`**.
2. A minimalist floating widget will appear showing `what is your command?`.
3. Press **`F12`** in any Windows application and speak your text.
4. Press **`F12`** again to finish recording.
5. When the status displays **`ready`** (accompanied by a chime sound), the text is copied to your clipboard — simply press **`Ctrl + V`** to paste!

---

## Option 2. Developer Setup (From Source Code)

Use this method if you want to develop features, modify the codebase, or build a custom standalone binary.

### System Requirements
* Windows 10 / 11
* Python 3.10+

### Step 1: Environment Setup
Clone the repository and set up your virtual environment:

```bat
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Configuration (.env)
Create your local environment file:
```bat
copy .env.example .env
```
Add your `LLM_API_KEY` into `.env` (or configure it via the interactive menu).

### Step 3: Run in Development Mode
```bat
python src/launcher.py
```
*(Or simply double-click `start.bat`)*.

### Step 4: Build Standalone Executable
To compile everything into a single portable `.exe` with embedded icons and assets:
```bat
build.bat
```
The script will build `dist\Shockwave.exe` and generate the `Shockwave.lnk` shortcut in the project root.

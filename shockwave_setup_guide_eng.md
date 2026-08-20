# Shockwave Setup Guide (English)

This guide will help you install and configure Shockwave on your PC (Windows 10/11).
The script is completely autonomous, written in Python, and downloads all necessary models automatically.

## Step 1: Install Python
Ensure you have Python installed (version 3.10 or newer is recommended).
During installation, **make sure to check the "Add Python to PATH" box**.

## Step 2: Install Dependencies
Open a command prompt in the project folder and install the required libraries:
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Step 3: Configure the .env file
Rename the `.env.example` file to `.env` (or create a new one) and configure it:

```ini
# STT Engine Settings
STT_ENGINE=whisper
WHISPER_MODEL=large-v3-turbo

# Normalization (LLM) Settings
LLM_ENDPOINT=http://127.0.0.1:8045/v1/chat/completions
LLM_API_KEY=your_api_key_here
LLM_MODEL=gemini-3.1-flash-lite

# UI Settings
HOTKEY=f12
UI_POSITION=bottom-left
```

### Engine Selection (STT_ENGINE)
You can choose between two engines:
1. `STT_ENGINE=whisper` (Recommended for developers). Perfectly handles mixed speech (Russian + English). Keeps IT terms (Docker, Python, useEffect) in English.
2. `STT_ENGINE=gigaam` (For pure Russian text). Much faster, but transcribes English words in Cyrillic.

**Models are downloaded automatically!**
On the very first run, the selected model will be downloaded (around 200-800 MB) into the system cache. Subsequent runs will be instant.

If you have already downloaded the models locally and want to use them, add to `.env`:
`WHISPER_MODEL_PATH=C:\path\to\model` or `GIGAAM_MODEL_PATH=C:\path\to\model`.

## Step 4: Run
Launch the script using `start.bat`.
A floating widget will appear in the bottom-left corner showing `what is your command?`.

## Usage
1. Press and **hold** `F12` (or your configured hotkey) while speaking. The widget will show `record`.
2. Release `F12`. The status changes to `processing` (transcribing the audio).
3. If the AI-correction checkbox is checked, it enters `normalization` mode.
4. The final text will be copied to your clipboard, and the widget will say `ready`. You can now paste (`Ctrl+V`) the text anywhere.

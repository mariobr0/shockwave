# Full Deployment Guide for Shockwave (Global Voice Dictation)

Shockwave is a custom Python script that allows you to dictate text in any Windows application using a global hotkey. It records your audio, transcribes it locally (via Whisper), and sends it to an LLM (Neural Network) to correct punctuation and typos, seamlessly copying the polished text to your clipboard.

Since the project relies on local technologies, a few third-party utilities are required.

---

## Part 1. Installing System Dependencies

### 1. Install SoX (Sound eXchange)
SoX is a command-line utility used to capture microphone audio.
1. Download the Windows installer (version 14.4.2): [sox-14.4.2-win32.exe](https://sourceforge.net/projects/sox/files/sox/14.4.2/sox-14.4.2-win32.exe/download)
2. Install the program. By default, it will install to `C:\Program Files (x86)\sox-14-4-2`.
3. **CRITICAL FOR WINDOWS:** On Windows 11, SoX cannot detect the microphone by default. Open PowerShell and run the following command to add the necessary environment variable:
   ```powershell
   [Environment]::SetEnvironmentVariable("AUDIODRIVER", "waveaudio", "User")
   ```

### 2. Install Whisper.cpp (Local Speech Recognition)
Whisper.cpp is an ultra-fast C/C++ port of OpenAI's Whisper model that runs on CPU or GPU.
1. Go to the [whisper.cpp releases page on GitHub](https://github.com/ggerganov/whisper.cpp/releases).
2. Download the archive for your system (e.g., `whisper-bin-x64.zip` for standard PCs or `whisper-cublas-...-bin-x64.zip` if you have an NVIDIA GPU).
3. Extract the archive into a convenient folder (e.g., `C:\tools\whisper`). Inside, you will find the executable file (usually named `whisper-cli.exe` or `main.exe`).
4. **Download the Language Model:**
   Download a model file, for example, [ggml-large-v3-turbo-q5_0.bin](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin). 
   Place it in a convenient folder, e.g.: `C:\Users\%USERNAME%\.local\share\whisper-cpp\`.

### 3. Setup a Local or Cloud LLM
The script requires an OpenAI-compatible API server to "normalize" the text (fixing punctuation and typos without summarizing).
This can be:
* Your own local proxy wrapping the Gemini API (e.g., running on `http://127.0.0.1:8045/v1`).
* A local server using LM Studio or Ollama.
* Direct OpenAI API (the endpoint will be `https://api.openai.com/v1/chat/completions`).

---

## Part 2. Shockwave Project Setup

### 1. Python Preparation
Ensure you have Python installed (version 3.10 or higher).

### 2. Download and Configure the Script
1. Clone or download the `Shockwave` project folder.
2. Open a terminal in the project folder and create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Install the required libraries (`keyboard`, `requests`, `pyperclip`, `python-dotenv`):
   ```bash
   venv\Scripts\pip install -r requirements.txt
   ```

### 3. Configure the .env File
Copy the `.env.example` file and rename it to `.env`. Open it in a text editor and specify the correct paths:

```env
# Paths to the utilities on your PC
SOX_PATH=C:\Program Files (x86)\sox-14-4-2\sox.exe
WHISPER_PATH=C:\tools\whisper\whisper-cli.exe
MODEL_PATH=C:\Users\YOUR_USER\.local\share\whisper-cpp\ggml-large-v3-turbo-q5_0.bin

# LLM Settings
LLM_ENDPOINT=http://127.0.0.1:8045/v1/chat/completions
LLM_API_KEY=your_secret_api_key
LLM_MODEL=gemini-3.1-flash-lite

# Interface Settings
HOTKEY=f12
UI_POSITION=bottom-left
```

---

## Part 3. Usage

1. Launch the script by double-clicking the `start.bat` file. A console window will open, displaying useful operation logs. You can simply minimize this window.
2. A persistent widget saying **"what is your command?"** will appear in the bottom-left corner of your screen. This means the script is ready. You can toggle the **"LLM norm"** checkbox to enable or disable AI text normalization.
3. Press **F12** (or your custom hotkey) **absolutely anywhere**—you don't need to have a text field focused. The widget will change its status to **"🔴 record"**.
4. Dictate your desired text into the microphone.
5. Press **F12** again. The widget will sequentially display **"⚙️ processing"** and **"🧠 normalization"**.
6. Once the status says **"✅ ready"**, the perfected text will be securely placed in your clipboard. Press `Ctrl+V` wherever you need it.
7. After 5 seconds, the widget will return to its standby state **"what is your command?"**, waiting for your next instruction.

> 💡 **Pro Tip:** The console serves as an excellent backup log. If you accidentally copy another text and overwrite your clipboard before pasting your dictation, simply maximize the console window—your text is safely preserved in the log history!

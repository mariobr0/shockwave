# Shockwave — Setup Guide

The application supports two installation methods: **Simple** (for regular users) and **Advanced** (for developers who want to work with the source code).

---

## Option 1. Simple Installation (Standalone EXE)

This is the fastest way to run Shockwave without installing Python or any third-party libraries.

### Step 1: Download
1. Download the `Shockwave.exe` file (found in the `dist` folder if you built the project yourself, or in the GitHub releases).
2. Place it in any convenient folder on your PC.

### Step 2: Configure API Key (.env)
Next to the `Shockwave.exe` file, create a text file named `.env` (note the leading dot) and add your LLM API key (e.g., Gemini) to it:

```env
LLM_API_KEY=your_key_here
STT_ENGINE=gigaam
```

*Valid values for `STT_ENGINE` are `whisper` or `gigaam`.*

### Step 3: Launch
Double-click `Shockwave.exe`.
1. On the first launch, the **Control Panel (Launcher)** will open in the console.
2. The program will automatically download the necessary speech recognition neural network (Whisper or GigaAM) to your system cache. (Note: the first download may take some time and require up to 2-3 GB of free space).
3. Select "Start Shockwave" from the menu.
4. Press `F12` in any Windows application to start dictating.

---

## Option 2. Advanced Installation (Source Code)

Use this option if you want to modify the code or rebuild the `.exe` file yourself.

### Requirements
* OS: Windows 10/11
* Python 3.10 or newer

### Step 1: Install Dependencies
Clone the repository and install the libraries:

```bat
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Environment Setup
Copy the configuration example:
```bat
copy .env.example .env
```
Edit `.env` and insert your `LLM_API_KEY`.

### Step 3: Run from Source
To run via Python, use:
```bat
python launcher.py
```
Or simply run `start.bat`.

### Step 4: Build Your Own EXE
If you made changes to the code and want to build a new standalone `Shockwave.exe`, run:
```bat
build.bat
```
The script will automatically install `PyInstaller`, add all necessary hidden imports and metadata, and then compile the project. The finished file will appear in the `dist` folder.

---

## Using the Application

* **F12 (hold or press)** — start/stop recording.
* The floating widget displays the current status:
  * `what is your command?` — waiting for input.
  * `record` — recording audio from the microphone.
  * `processing` — speech-to-text (STT) conversion.
  * `normalization` — fixing punctuation via LLM.
  * `ready` — text successfully copied to clipboard.
* The checkbox on the widget allows you to toggle AI normalization on the fly. When unchecked, the raw recognized text is copied immediately without waiting for LLM requests.
* To close the application completely, click the red cross (✖) on the widget.

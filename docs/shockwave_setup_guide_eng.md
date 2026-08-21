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
   * **Option 2 (`Configure API Key & LLM`):** Enter your LLM API key for text normalization.
   * **Option 3 (`Select STT Engine`):** Choose `Whisper` (for code / mixed speech) or `GigaAM` (for Russian speech).
   * **Option 4 (`Download / Verify STT Models`):** Download the selected model weights into the local `models/` directory.
   * **Option 5 (`Сменить язык на русский`):** Toggle interface language if needed.

**Manual Configuration via `.env.example` (Optional):**  
You can also configure all settings manually. Simply copy or rename the template `.env.example` to `.env`:
```bat
copy .env.example .env
```
and edit the parameters (e.g. change the global hotkey `HOTKEY=f12`, widget position, or local LLM endpoints) in any text editor.

---

### 4. Usage
1. In the menu, select **`1. Start Shockwave`** — a floating widget will appear on screen.
2. Press **`F12`** in any application and speak your text.
3. Press **`F12`** again to finish recording.
4. When the status displays **`ready`** (accompanied by a chime), the formatted text is already in your clipboard (`Ctrl + V`).

---

### 5. Widget Controls
* **`LLM norm` checkbox:** Toggle AI-based punctuation and typo correction.
* **`alert` checkbox:** Toggle audio chime notification on completion.
* **`×` button:** Exit application.

@echo off
cd /d "%~dp0"

echo [1/3] Activating virtual environment...
call venv\Scripts\activate

echo [2/3] Installing PyInstaller...
python -m pip install pyinstaller

echo [3/3] Building Shockwave.exe...
python -m PyInstaller --name Shockwave --onefile --console --icon=icons\icon.ico --add-data "icons;icons" --add-data "alert;alert" --collect-all onnx_asr --collect-all faster_whisper --copy-metadata onnx-asr --copy-metadata onnx_asr --copy-metadata faster-whisper --hidden-import onnx_asr --hidden-import faster_whisper --hidden-import huggingface_hub --hidden-import sounddevice --hidden-import soundfile --hidden-import keyboard --hidden-import pyautogui --hidden-import dotenv --hidden-import tkinter launcher.py

echo.
echo ===================================================
echo DONE! Check the dist folder for Shockwave.exe
echo ===================================================
pause

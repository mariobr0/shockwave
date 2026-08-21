@echo off
cd /d "%~dp0"

echo [1/3] Activating virtual environment...
call venv\Scripts\activate

echo [2/3] Installing PyInstaller...
python -m pip install pyinstaller

echo [3/3] Building Shockwave.exe...
python -m PyInstaller --name Shockwave --onefile --console --icon=icons\icon.ico --paths=src --add-data "icons;icons" --add-data "alert;alert" --collect-all onnx_asr --collect-all faster_whisper --copy-metadata onnx-asr --copy-metadata onnx_asr --copy-metadata faster-whisper --hidden-import onnx_asr --hidden-import faster_whisper --hidden-import huggingface_hub --hidden-import sounddevice --hidden-import soundfile --hidden-import keyboard --hidden-import pyautogui --hidden-import dotenv --hidden-import tkinter src\launcher.py

echo.
if exist "dist\Shockwave.exe" (
    powershell -NoProfile -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%~dp0Shockwave.lnk'); $s.TargetPath = '%~dp0dist\Shockwave.exe'; $s.WorkingDirectory = '%~dp0'; $s.IconLocation = '%~dp0icons\icon.ico,0'; $s.Save()"
    echo ===================================================
    echo DONE! Shockwave.lnk shortcut is ready in the root!
    echo ===================================================
) else (
    echo Build failed. Please check the logs above.
)
pause

@echo off
cd /d "%~dp0"

echo [1/4] Closing any running Shockwave instances...
taskkill /F /IM Shockwave.exe >nul 2>&1

echo [2/4] Activating virtual environment...
call venv\Scripts\activate

echo [3/4] Ensuring PyInstaller is ready...
python -m pip install pyinstaller >nul 2>&1

echo [4/4] Building Shockwave.exe...
python -m PyInstaller --name Shockwave --onefile --console --icon=icons\icon.ico --paths=src --add-data "icons;icons" --add-data "alert;alert" --collect-all onnx_asr --collect-all faster_whisper --copy-metadata onnx-asr --copy-metadata onnx_asr --copy-metadata faster-whisper --hidden-import onnx_asr --hidden-import faster_whisper --hidden-import huggingface_hub --hidden-import sounddevice --hidden-import soundfile --hidden-import keyboard --hidden-import pyautogui --hidden-import dotenv --hidden-import tkinter src\launcher.py

echo.
if exist "dist\Shockwave.exe" (
    powershell -NoProfile -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%~dp0Shockwave.lnk'); $s.TargetPath = '%~dp0dist\Shockwave.exe'; $s.WorkingDirectory = '%~dp0'; $s.IconLocation = '%~dp0icons\icon.ico,0'; $s.Save(); $s2 = $ws.CreateShortcut('%~dp0Shockwave (Виджет).lnk'); $s2.TargetPath = '%~dp0dist\Shockwave.exe'; $s2.Arguments = '--widget'; $s2.WorkingDirectory = '%~dp0'; $s2.IconLocation = '%~dp0icons\icon.ico,0'; $s2.Save()"
    echo =======================================================================
    echo DONE! Two shortcuts are ready in the root:
    echo  1. Shockwave.lnk           - Control Panel (minimizes to tray)
    echo  2. Shockwave (Виджет).lnk - Direct silent launch (widget only)
    echo =======================================================================
) else (
    echo Build failed. Please check the logs above.
)
pause

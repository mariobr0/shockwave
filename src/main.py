import threading
import queue
import time
import sys
import os

import config

from ui import WinVoiceUI, get_resource_path
from audio_engine import AudioEngine
from llm_normalizer import LLMNormalizer
from typer import Typer
from hotkey_manager import SystemHotkeyManager
from single_instance import check_single_instance, release_single_instance
from tray_manager import SystemTrayManager, hide_console, show_console

class WinVoiceApp:
    def __init__(self, is_silent=False):
        # 1. Single-Instance Protection: Prevent multiple instances running simultaneously
        if not check_single_instance():
            print("\n[Shockwave] Программа уже запущена! / Shockwave is already running!")
            time.sleep(1.5)
            sys.exit(0)
            
        self.is_silent = is_silent
        self.q = queue.Queue()
        self.audio = AudioEngine()
        self.llm = LLMNormalizer()
        self.typer = Typer()
        
        self.is_recording = False
        self.is_processing = False
        self.lock = threading.Lock()
        
        # Initialize UI with click-to-trigger handler
        self.ui = WinVoiceUI(self.q, position=config.UI_POSITION, on_trigger=self.toggle_recording)
        
        # 2. System Tray Manager: Place Shockwave icon next to clock with toggle & exit menu
        icon_path = get_resource_path(os.path.join("icons", "icon.ico"))
        self.tray = SystemTrayManager(
            icon_path=icon_path,
            tooltip=f"Shockwave v{getattr(config, 'APP_VERSION', '0.9.3')}",
            on_quit=self.quit_app
        )
        self.tray.start()
        
        # 3. Register permanent system-level hotkey via Win32 RegisterHotKey
        self.hotkey_mgr = SystemHotkeyManager(config.HOTKEY, self.toggle_recording)
        yellow_eye = "\033[38;2;255;215;0m\033[1mEye\033[0m"
        print(f"Shockwave started. Press {config.HOTKEY.upper()} or click the {yellow_eye} to record.")
        
        # Hide console window to system tray smoothly
        hide_console()

    def toggle_recording(self):
        with self.lock:
            if self.is_processing:
                return
                
            if not self.is_recording:
                self.is_recording = True
                threading.Thread(target=self.start_recording_thread, daemon=True).start()
            else:
                self.is_recording = False
                self.is_processing = True
                threading.Thread(target=self.process_audio_thread, daemon=True).start()

    def start_recording_thread(self):
        self.q.put({"cmd": "show", "text": "record"})
        self.audio.start_recording()

    def process_audio_thread(self):
        self.q.put({"cmd": "show", "text": "processing"})
        
        self.audio.stop_recording()
        raw_text = self.audio.transcribe()
        
        if raw_text:
            if self.ui.llm_enabled:
                self.q.put({"cmd": "show", "text": "normalization"})
                print(f"Sending to LLM: {raw_text}")
                final_text = self.llm.normalize(raw_text)
            else:
                print(f"LLM disabled. Using raw text: {raw_text}")
                final_text = raw_text
                
            print(f"Final text: {final_text}")
            self.typer.type_text(final_text)
            self.q.put({"cmd": "show_ready"})
        else:
            print("Warning: Transcription was empty or failed. Skipping.")
            self.q.put({"cmd": "show", "text": "what is your command?"})
        
        with self.lock:
            self.is_processing = False
            self.is_recording = False

    def quit_app(self):
        """Cleanly signals UI to quit."""
        self.q.put({"cmd": "quit"})

    def cleanup(self):
        if hasattr(self, 'tray'):
            self.tray.stop()
        if hasattr(self, 'hotkey_mgr'):
            self.hotkey_mgr.stop()
        self.audio.stop_recording()
        if os.path.exists(config.AUDIO_TEMP_FILE):
            try:
                os.remove(config.AUDIO_TEMP_FILE)
            except:
                pass
        release_single_instance()

    def run(self):
        try:
            self.ui.run()
        finally:
            self.cleanup()

if __name__ == "__main__":
    app = WinVoiceApp()
    app.run()

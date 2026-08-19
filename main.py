import threading
import queue
import time
import keyboard
import sys
import os

import config
from ui import WinVoiceUI
from audio_engine import AudioEngine
from llm_normalizer import LLMNormalizer
from typer import Typer

class WinVoiceApp:
    def __init__(self):
        self.q = queue.Queue()
        self.ui = WinVoiceUI(self.q, position=config.UI_POSITION)
        self.audio = AudioEngine()
        self.llm = LLMNormalizer()
        self.typer = Typer()
        
        self.is_recording = False
        self.is_processing = False
        self.lock = threading.Lock()
        
        keyboard.add_hotkey(config.HOTKEY, self.on_hotkey, suppress=True)
        print("Shockwave started. Press F12 to record.")

    def on_hotkey(self):
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
        self.q.put({"cmd": "show", "text": "🔴 Идет запись..."})
        self.audio.start_recording()

    def process_audio_thread(self):
        self.q.put({"cmd": "show", "text": "⚙️ Обработка..."})
        
        self.audio.stop_recording()
        raw_text = self.audio.transcribe()
        
        if raw_text:
            if self.ui.llm_enabled:
                self.q.put({"cmd": "show", "text": "🧠 Нормализация..."})
                print(f"Sending to LLM: {raw_text}")
                final_text = self.llm.normalize(raw_text)
            else:
                print(f"LLM disabled. Using raw text: {raw_text}")
                final_text = raw_text
                
            print(f"Final text: {final_text}")
            self.typer.type_text(final_text)
            self.q.put({"cmd": "fade_out", "text": "✅ Текст готов для вставки"})
        else:
            print("Warning: Transcription was empty or failed. Skipping.")
            self.q.put({"cmd": "hide"})
        
        with self.lock:
            self.is_processing = False
            self.is_recording = False

    def cleanup(self):
        self.audio.stop_recording()
        if os.path.exists(config.AUDIO_TEMP_FILE):
            try:
                os.remove(config.AUDIO_TEMP_FILE)
            except:
                pass

    def run(self):
        try:
            self.ui.run()
        finally:
            self.cleanup()

if __name__ == "__main__":
    app = WinVoiceApp()
    app.run()

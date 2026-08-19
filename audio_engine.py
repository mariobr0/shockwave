import os
import subprocess
import time
import config

class AudioEngine:
    def __init__(self):
        self.sox_process = None

    def start_recording(self):
        if self.sox_process:
            self.stop_recording()
        
        if os.path.exists(config.AUDIO_TEMP_FILE):
            os.remove(config.AUDIO_TEMP_FILE)
            
        print(f"Starting recording with SoX...")
        cmd = [
            config.SOX_PATH,
            "-d", 
            "-r", "16000",
            "-c", "1",
            "-b", "16",
            config.AUDIO_TEMP_FILE,
            "silence", "1", "0.1", "1%"
        ]
        
        self.sox_process = subprocess.Popen(cmd)

    def stop_recording(self):
        if self.sox_process:
            print("Stopping SoX...")
            self.sox_process.terminate()
            try:
                self.sox_process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.sox_process.kill()
            self.sox_process = None
            time.sleep(0.1)

    def transcribe(self):
        print(f"Checking WAV file: {config.AUDIO_TEMP_FILE}")
        if not os.path.exists(config.AUDIO_TEMP_FILE):
            print("Error: WAV file does not exist!")
            return ""
        
        size = os.path.getsize(config.AUDIO_TEMP_FILE)
        print(f"WAV size: {size} bytes")
        if size < 100:
            print("Error: WAV file is too small (empty)!")
            return ""

        print("Starting Whisper...")
        cmd = [
            config.WHISPER_PATH,
            "-m", config.MODEL_PATH,
            "-f", config.AUDIO_TEMP_FILE,
            "-l", "ru",
            "-otxt",
            "-np",
            "-nt"
        ]
        
        try:
            # We don't hide output so user can see it in console
            subprocess.run(cmd, timeout=30)
            
            possible_txt = [
                f"{config.AUDIO_TEMP_FILE}.txt",
                f"{config.TXT_OUTPUT_FILE}.txt",
                "temp_audio.txt"
            ]
            
            for path in possible_txt:
                if os.path.exists(path):
                    print(f"Found transcript file: {path}")
                    with open(path, "r", encoding="utf-8") as f:
                        text = f.read().strip()
                    os.remove(path)
                    print(f"Whisper transcribed: {text}")
                    return text
            
            print("Error: Whisper finished but NO .txt file was found!")
            return ""
        except Exception as e:
            print(f"Whisper Exception: {e}")
            return ""

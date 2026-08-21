import numpy as np
import sounddevice as sd
import soundfile as sf
import time
import os
import threading

import config

import importlib.metadata
_original_version = importlib.metadata.version
def _safe_version(pkg_name):
    if "onnx" in pkg_name or "asr" in pkg_name:
        return "0.12.0"
    try:
        return _original_version(pkg_name)
    except importlib.metadata.PackageNotFoundError:
        return "0.0.0"
importlib.metadata.version = _safe_version

class AudioEngine:
    def __init__(self):
        self.stream = None
        self.audio_data = []
        self.sample_rate = 16000
        self.is_recording = False
        
        self.engine_type = (os.getenv("STT_ENGINE") or config.STT_ENGINE).lower()
        self.model = None
        
        print(f"Initializing STT Engine ({self.engine_type})...")
        if self.engine_type == "gigaam":
            try:
                import onnx_asr
                model_name = config.GIGAAM_MODEL
                quant = config.GIGAAM_QUANTIZATION if config.GIGAAM_QUANTIZATION else None
                gigaam_path = config.GIGAAM_MODEL_PATH if config.GIGAAM_MODEL_PATH else config.GIGAAM_DIR
                
                print(f"Loading GigaAM model: {model_name} (quantization={quant}) ...")
                if os.path.exists(gigaam_path) and os.listdir(gigaam_path):
                    print(f"Loading from local path: {gigaam_path}")
                    self.model = onnx_asr.load_model(model_name, path=gigaam_path, quantization=quant)
                else:
                    self.model = onnx_asr.load_model(model_name, quantization=quant)
                print("GigaAM model loaded successfully.")
            except Exception as e:
                print(f"Error loading GigaAM: {e}")
        else:
            try:
                from faster_whisper import WhisperModel
                whisper_path = config.WHISPER_MODEL_PATH if config.WHISPER_MODEL_PATH else config.WHISPER_DIR
                
                if os.path.exists(whisper_path) and os.path.exists(os.path.join(whisper_path, "model.bin")):
                    print(f"Loading Whisper model from local path: {whisper_path} ...")
                    self.model = WhisperModel(whisper_path, device="cpu", compute_type="int8")
                else:
                    model_name = config.WHISPER_MODEL
                    print(f"Loading Whisper model by name: {model_name} ...")
                    self.model = WhisperModel(model_name, device="cpu", compute_type="int8", download_root=whisper_path)
                print("Whisper model loaded successfully.")
            except Exception as e:
                print(f"Error loading Whisper: {e}")
                
        print("STT Engine is ready.")

    def _audio_callback(self, indata, frames, time_info, status):
        """Called by sounddevice for each audio block."""
        if status:
            pass
        if self.is_recording:
            self.audio_data.append(indata.copy())

    def start_recording(self):
        self.audio_data = []
        self.is_recording = True
        print("Started recording...")
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype='float32',
            callback=self._audio_callback
        )
        self.stream.start()

    def stop_recording(self):
        if self.stream:
            print("Stopping recording...")
            self.is_recording = False
            self.stream.stop()
            self.stream.close()
            self.stream = None

    def transcribe(self) -> str:
        if not self.model:
            print("Error: No STT model loaded.")
            return ""
            
        if not self.audio_data:
            print("Error: No audio data recorded.")
            return ""
            
        # Concatenate audio chunks and flatten to 1D array
        audio_np = np.concatenate(self.audio_data, axis=0).flatten()
        duration = len(audio_np) / self.sample_rate
        
        if duration < 0.5:
            print("Error: Audio too short!")
            return ""
            
        print(f"Transcribing audio ({duration:.2f} seconds)...")
        
        try:
            if self.engine_type == "gigaam":
                # onnx_asr processing
                text = self.model.recognize(audio_np)
                if not isinstance(text, str):
                    text = str(text)
                
                print(f"GigaAM output: {text}")
                return text.strip()
                
            else:
                # faster-whisper processing
                whisper_lang = os.getenv("WHISPER_LANGUAGE", config.WHISPER_LANGUAGE)
                if whisper_lang:
                    whisper_lang = whisper_lang.strip().lower()
                    if whisper_lang in ["auto", "none", ""]:
                        whisper_lang = None
                else:
                    whisper_lang = None
                    
                segments, info = self.model.transcribe(audio_np, language=whisper_lang)
                text = " ".join([segment.text for segment in segments])
                print(f"Whisper output ({whisper_lang if whisper_lang else 'auto'}): {text}")
                return text.strip()
                
        except Exception as e:
            print(f"Transcription exception: {e}")
            return ""

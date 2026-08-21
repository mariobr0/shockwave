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
        
        self.engine_type = config.STT_ENGINE.lower()
        self.model = None
        
        print(f"Initializing STT Engine ({self.engine_type})...")
        if self.engine_type == "gigaam":
            try:
                import onnx_asr
                model_name = config.GIGAAM_MODEL_PATH if config.GIGAAM_MODEL_PATH else config.GIGAAM_MODEL
                quant = config.GIGAAM_QUANTIZATION if config.GIGAAM_QUANTIZATION else None
                print(f"Loading GigaAM model: {model_name} (quantization={quant}) ...")
                self.model = onnx_asr.load_model(model_name, quantization=quant)
            except Exception as e:
                print(f"Error loading GigaAM: {e}")
        else:
            try:
                from faster_whisper import WhisperModel
                model_name = config.WHISPER_MODEL_PATH if config.WHISPER_MODEL_PATH else config.WHISPER_MODEL
                print(f"Loading Faster-Whisper model: {model_name} ...")
                self.model = WhisperModel(model_name, device="cpu", compute_type="int8")
            except Exception as e:
                print(f"Error loading Whisper: {e}")
                
        print("STT Engine is ready.")

    def _audio_callback(self, indata, frames, time_info, status):
        """Called by sounddevice for each audio block."""
        if status:
            pass # ignore warnings
        if self.is_recording:
            # indata is shape (frames, channels) -> (frames, 1)
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
                segments, info = self.model.transcribe(audio_np, language="ru")
                text = " ".join([segment.text for segment in segments])
                print(f"Whisper output: {text}")
                return text.strip()
                
        except Exception as e:
            print(f"Transcription exception: {e}")
            return ""

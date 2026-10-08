"""
Speech Engine: Handles Text-to-Speech (TTS) and Speech-to-Text (STT).
"""
import subprocess
import platform
import logging
from config import Config

logger = logging.getLogger(__name__)

class SpeechEngine:
    def __init__(self):
        self.os_type = platform.system()
        self.engine = None
        self._init_pyttsx3()

    def _init_pyttsx3(self):
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', Config.VOICE_RATE)
            self.engine.setProperty('volume', Config.VOICE_VOLUME)
        except Exception as e:
            logger.warning(f"pyttsx3 initialization skipped/failed: {e}")
            self.engine = None

    def speak(self, text: str):
        """Speak text out loud using native OS voice or pyttsx3."""
        if not text:
            return
        
        # Native macOS say command for best natural voice on Mac
        if self.os_type == "Darwin":
            try:
                subprocess.Popen(["say", "-v", "Samantha", text])
                return
            except Exception:
                pass

        # Fallback to pyttsx3
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                logger.error(f"TTS error: {e}")

    def listen_mic(self) -> str:
        """Listen to system microphone and return transcribed text."""
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.8)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = recognizer.recognize_google(audio)
                return text
        except Exception as e:
            logger.debug(f"Speech recognition: {e}")
            return ""

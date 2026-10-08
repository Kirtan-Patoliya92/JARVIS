"""
Command Handler: Parses intents and orchestrates actions between all modules.
"""
import re
import logging
from config import Config
from speech_engine import SpeechEngine
from system_controls import SystemControls
from web_actions import WebActions
from ai_brain import AIBrain

logger = logging.getLogger(__name__)

class CommandHandler:
    def __init__(self):
        self.speech = SpeechEngine()
        self.system = SystemControls()
        self.web = WebActions()
        self.brain = AIBrain()

    def process_command(self, query: str, speak_output: bool = False) -> dict:
        """Process natural language command or user request and execute action."""
        if not query or not query.strip():
            return {
                "success": False,
                "message": "Empty query received.",
                "response": "I didn't catch that, Sir."
            }

        text = query.strip()
        lower_text = text.lower().strip()
        result = {
            "success": True,
            "query": text,
            "action": "chat",
            "response": "",
            "data": {}
        }

        # 1. Identity & Name questions
        if any(phrase in lower_text for phrase in [
            "your name", "who are you", "what are you", "who made you", 
            "who created you", "who is your developer", "who built you",
            "what is your name", "whats your name", "what's your name"
        ]):
            if any(p in lower_text for p in ["who made you", "who created you", "who is your developer", "who built you"]):
                resp = f"I was created and engineered by {Config.AUTHOR}."
            else:
                resp = f"I am {Config.ASSISTANT_NAME}, your personal AI assistant created and developed by {Config.AUTHOR}."
            result.update({"action": "identity", "response": resp})

        # 2. Time & Date
        elif any(phrase in lower_text for phrase in ["what time", "current time", "tell me time", "time please"]) or lower_text == "time":
            resp = self.system.get_time()
            result.update({"action": "time", "response": resp})

        elif any(phrase in lower_text for phrase in ["what date", "current date", "today's date", "what is today's date", "date please"]) or lower_text == "date":
            resp = self.system.get_date()
            result.update({"action": "date", "response": resp})

        # 3. System Diagnostics (CPU, RAM, Battery)
        elif any(k in lower_text for k in ["system status", "system diagnostics", "battery", "cpu usage", "ram usage", "memory status", "system info"]):
            stats = self.system.get_system_status()
            resp = f"System Diagnostics: CPU at {stats['cpu_percent']}, Memory at {stats['memory_percent']}, Battery at {stats['battery_percent']}."
            result.update({"action": "system_status", "response": resp, "data": stats})

        # 4. Volume Control
        elif "volume" in lower_text or "mute" in lower_text:
            match = re.search(r'(\d+)', lower_text)
            if match:
                vol = int(match.group(1))
                resp = self.system.set_volume(vol)
            elif "mute" in lower_text:
                resp = self.system.set_volume(0)
            elif "up" in lower_text or "increase" in lower_text:
                resp = self.system.set_volume(80)
            elif "down" in lower_text or "decrease" in lower_text:
                resp = self.system.set_volume(30)
            else:
                resp = "Please specify a volume level from 0 to 100."
            result.update({"action": "volume", "response": resp})

        # 5. Open Applications or Websites
        elif lower_text.startswith("open ") or lower_text.startswith("launch "):
            app_target = lower_text.replace("open ", "").replace("launch ", "").strip()
            if any(domain in app_target for domain in [".com", ".org", ".io", ".net", ".in"]):
                import webbrowser
                url = f"https://{app_target}" if not app_target.startswith("http") else app_target
                webbrowser.open(url)
                resp = f"Opening {app_target} in your browser."
            else:
                resp = self.system.open_application(app_target)
            result.update({"action": "open_app", "response": resp})

        # 6. YouTube Search / Play
        elif lower_text.startswith("play ") or "on youtube" in lower_text or lower_text.startswith("youtube "):
            clean_query = lower_text.replace("play ", "").replace("on youtube", "").replace("youtube ", "").replace("search ", "").strip()
            yt_res = self.web.youtube_search(clean_query)
            result.update({"action": "youtube", "response": yt_res["message"], "data": yt_res})

        # 7. Google Search
        elif lower_text.startswith("google ") or lower_text.startswith("search google for ") or "search on google" in lower_text:
            clean_query = lower_text.replace("search on google", "").replace("search google for ", "").replace("google ", "").strip()
            g_res = self.web.google_search(clean_query)
            result.update({"action": "google", "response": g_res["message"], "data": g_res})

        # 8. Wikipedia (Explicit query only)
        elif "wikipedia" in lower_text or lower_text.startswith("wiki "):
            clean_query = lower_text.replace("wikipedia ", "").replace("search wikipedia for ", "").replace("search on wikipedia ", "").replace("wiki ", "").strip()
            wiki_res = self.web.wikipedia_summary(clean_query)
            result.update({"action": "wikipedia", "response": wiki_res["message"], "data": wiki_res})

        # 9. Weather
        elif "weather" in lower_text or "temperature" in lower_text:
            city = "Surat"
            words = lower_text.split()
            if "in" in words:
                idx = words.index("in")
                if idx + 1 < len(words):
                    city = words[idx + 1].capitalize()
            weather_res = self.web.get_weather(city)
            result.update({"action": "weather", "response": weather_res["message"], "data": weather_res})

        # 10. AI Brain & General Conversational Reasoning (Gemini, OpenRouter, or Smart Brain)
        else:
            ai_resp = self.brain.generate_response(text)
            result.update({"action": "ai_chat", "response": ai_resp})

        if speak_output and result["response"]:
            self.speech.speak(result["response"])

        return result

"""
AI Brain: Conversational reasoning and natural language generation.
Supports OpenRouter / Router APIs (e.g. Llama-3, DeepSeek, Claude, Mistral), 
Gemini API, OpenAI API, and Offline fallback.
"""
import random
import logging
import requests
from config import Config

logger = logging.getLogger(__name__)

class AIBrain:
    def __init__(self):
        self.router_api_key = Config.ROUTER_API_KEY
        self.router_base_url = Config.ROUTER_BASE_URL.rstrip('/')
        self.router_model = Config.ROUTER_MODEL
        self.gemini_model = None
        self._init_gemini()

    def _init_gemini(self):
        if Config.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=f"You are JARVIS, an advanced, polite, witty AI assistant created by and serving {Config.AUTHOR} ({Config.USER_NAME}). Keep answers concise, helpful, and natural for speech."
                )
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini model: {e}")

    def _query_router_api(self, prompt: str) -> str:
        """Call OpenRouter or custom OpenAI-compatible router API."""
        try:
            endpoint = f"{self.router_base_url}/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.router_api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/patoliyakirtan/JARVIS",
                "X-Title": "JARVIS AI Assistant"
            }
            payload = {
                "model": self.router_model,
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are JARVIS, an ultra-smart, loyal, and witty AI voice assistant created and programmed by {Config.AUTHOR} for user {Config.USER_NAME}. Keep answers clear, direct, and conversational (1-3 sentences unless asked for details)."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 250,
                "temperature": 0.7
            }
            resp = requests.post(endpoint, headers=headers, json=payload, timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                if "choices" in data and len(data["choices"]) > 0:
                    reply = data["choices"][0].get("message", {}).get("content", "")
                    if reply:
                        return reply.strip()
            else:
                logger.warning(f"Router API error [{resp.status_code}]: {resp.text}")
        except Exception as e:
            logger.warning(f"Router API request failed: {e}")

        return ""

    def generate_response(self, prompt: str) -> str:
        """Generate response via Router API, Gemini, or Smart Offline fallback."""
        # 1. Try Router API (OpenRouter / custom router model)
        if self.router_api_key:
            router_reply = self._query_router_api(prompt)
            if router_reply:
                return router_reply

        # 2. Try Gemini if configured
        if self.gemini_model:
            try:
                res = self.gemini_model.generate_content(prompt)
                if res and res.text:
                    return res.text.strip()
            except Exception as e:
                logger.warning(f"Gemini generation error: {e}")

        # 3. Smart Offline Natural Language Fallback
        prompt_lower = prompt.lower().strip()
        
        greetings = ["hello", "hi", "hey", "jarvis", "namaste"]
        if any(w in prompt_lower for w in greetings):
            responses = [
                f"Hello {Config.USER_NAME}! How may I assist you today?",
                f"At your service, {Config.USER_NAME}. What can I do for you?",
                f"Online and ready, {Config.USER_NAME}."
            ]
            return random.choice(responses)

        if "who created you" in prompt_lower or "who is your developer" in prompt_lower or "who made you" in prompt_lower:
            return f"I was created and engineered by {Config.AUTHOR}."

        if "who are you" in prompt_lower or "what are you" in prompt_lower or "your name" in prompt_lower:
            return f"I am {Config.ASSISTANT_NAME}, your personal AI assistant built by {Config.AUTHOR}."

        if "how are you" in prompt_lower:
            return "All systems are running at 100% capacity, Sir. How can I help you today?"

        if "thank" in prompt_lower:
            return "You're most welcome, Sir! Always at your service."

        if "bye" in prompt_lower or "goodbye" in prompt_lower or "exit" in prompt_lower:
            return f"Goodbye {Config.USER_NAME}. Have a wonderful day!"

        return f"I have received your request: '{prompt}'. Configure your ROUTER_API_KEY in .env for full AI intelligence."

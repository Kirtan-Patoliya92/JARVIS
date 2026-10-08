# JARVIS AI Assistant Configuration
import os

# Safe .env loader without requiring external modules
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    os.environ.setdefault(key.strip(), val.strip())

class Config:
    AUTHOR = "Kirtan Patoliya"
    ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "JARVIS")
    USER_NAME = os.getenv("USER_NAME", "Kirtan")
    
    # Server settings (Port 8080 avoids Mac AirPlay conflict on 5000)
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 8080))
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    
    # OpenRouter / Custom Router API Settings (Primary AI Provider)
    ROUTER_API_KEY = os.getenv("ROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY", "")
    ROUTER_BASE_URL = os.getenv("ROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    ROUTER_MODEL = os.getenv("ROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free")
    
    # Optional direct API keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
    
    # Voice Settings
    VOICE_RATE = int(os.getenv("VOICE_RATE", 175))
    VOICE_VOLUME = float(os.getenv("VOICE_VOLUME", 1.0))

"""
Web Actions: Handles web searches, Wikipedia summaries, YouTube searches, Weather reports, and URL browsing.
"""
import urllib.parse
import webbrowser
import requests
import logging
from config import Config

logger = logging.getLogger(__name__)

class WebActions:
    def __init__(self):
        pass

    def google_search(self, query: str) -> dict:
        """Perform Google Search and return URL."""
        encoded = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={encoded}"
        webbrowser.open(url)
        return {
            "action": "google_search",
            "query": query,
            "url": url,
            "message": f"Searching Google for '{query}', Sir."
        }

    def youtube_search(self, query: str) -> dict:
        """Search or play on YouTube."""
        encoded = urllib.parse.quote_plus(query)
        url = f"https://www.youtube.com/results?search_query={encoded}"
        webbrowser.open(url)
        return {
            "action": "youtube_search",
            "query": query,
            "url": url,
            "message": f"Opening YouTube for '{query}'."
        }

    def wikipedia_summary(self, query: str) -> dict:
        """Fetch summary from Wikipedia API."""
        try:
            endpoint = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
            headers = {'User-Agent': 'JarvisAssistant/2.0 (assistant@jarvis.ai)'}
            response = requests.get(endpoint, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                extract = data.get("extract", "No summary found.")
                short_summary = " ".join(extract.split(". ")[:2]) + "."
                return {
                    "action": "wikipedia",
                    "title": data.get("title", query),
                    "summary": short_summary,
                    "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
                    "message": f"According to Wikipedia: {short_summary}"
                }
        except Exception as e:
            logger.warning(f"Wikipedia search error: {e}")
            
        return {
            "action": "wikipedia",
            "message": f"I couldn't find specific Wikipedia details for '{query}'."
        }

    def get_weather(self, city: str = "Surat") -> dict:
        """Fetch current weather for a city."""
        try:
            url = f"https://wttr.in/{urllib.parse.quote(city)}?format=%C+%t+%w"
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200 and resp.text.strip():
                weather_info = resp.text.strip()
                return {
                    "action": "weather",
                    "city": city,
                    "info": weather_info,
                    "message": f"Weather in {city}: {weather_info}"
                }
        except Exception as e:
            logger.warning(f"Weather error: {e}")

        return {
            "action": "weather",
            "city": city,
            "message": f"Unable to fetch weather data for {city} right now."
        }

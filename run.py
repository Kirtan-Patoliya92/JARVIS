#!/usr/bin/env python3
"""
JARVIS AI Voice Assistant
Created & Developed by: Kirtan Patoliya
"""
import sys
import os
import argparse
import logging
import threading
import time
import webbrowser
from config import Config
from app import run_server, HAS_FLASK
from command_handler import CommandHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("JARVIS-MAIN")

def open_browser(url: str):
    """Wait for server to bind and automatically open default browser."""
    time.sleep(1.2)
    try:
        webbrowser.open(url)
    except Exception as e:
        logger.warning(f"Could not auto-open browser: {e}")

def run_web():
    """Start the JARVIS Futuristic Web Interface."""
    url = f"http://127.0.0.1:{Config.PORT}"
    
    print(f"\n========================================================")
    print(f"             ⚡ {Config.ASSISTANT_NAME} AI ASSISTANT ⚡             ")
    print(f"         Created & Developed by: {Config.AUTHOR}        ")
    print(f"========================================================")
    print(f" 🌐 Web HUD URL : {url}")
    print(f" 🔗 Localhost   : http://localhost:{Config.PORT}")
    print(f" 👤 Active User : {Config.USER_NAME}")
    print(f" ⚙️ Engine Mode : {'Flask Server' if HAS_FLASK else 'Built-in Native Server'}")
    print(f" 🚀 Opening web browser automatically...")
    print(f" 🛑 Press Ctrl+C in this terminal to stop.")
    print(f"========================================================\n")
    
    threading.Thread(target=open_browser, args=(url,), daemon=True).start()
    run_server(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)

def run_cli():
    """Start interactive CLI/Terminal mode."""
    print(f"\n========================================================")
    print(f" ⚡ {Config.ASSISTANT_NAME} CLI Mode (Dev: {Config.AUTHOR}) ⚡")
    print(f"========================================================")
    print("Type your command or 'exit' to quit.\n")
    
    handler = CommandHandler()
    handler.speech.speak(f"Greetings {Config.USER_NAME}, JARVIS is online.")
    
    while True:
        try:
            query = input(f"\n[{Config.USER_NAME}] > ")
            if not query.strip():
                continue
            if query.lower() in ("exit", "quit", "bye"):
                print(f"[{Config.ASSISTANT_NAME}] Goodbye {Config.USER_NAME}.")
                handler.speech.speak(f"Goodbye {Config.USER_NAME}.")
                break
            
            res = handler.process_command(query, speak_output=True)
            print(f"[{Config.ASSISTANT_NAME}] {res.get('response')}")
        except (KeyboardInterrupt, EOFError):
            print("\nShutting down JARVIS.")
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="JARVIS AI Assistant")
    parser.add_argument('--cli', action='store_true', help="Run in Terminal / CLI mode")
    parser.add_argument('--port', type=int, default=Config.PORT, help="Port to run web server on")
    args = parser.parse_args()
    
    if args.port:
        Config.PORT = args.port

    if args.cli:
        run_cli()
    else:
        run_web()

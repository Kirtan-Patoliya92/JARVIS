"""
JARVIS Web Application (Dual Mode: Flask or Zero-Dependency Built-in HTTP Server)
Serves index.html, style.css, app.js and REST APIs directly from the root directory.
"""
import os
import json
import logging
from config import Config
from command_handler import CommandHandler

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
handler = CommandHandler()

# Try importing Flask, or fallback to zero-dependency Python http.server
try:
    from flask import Flask, render_template, request, jsonify, send_from_directory
    HAS_FLASK = True
    app = Flask(__name__, template_folder=BASE_DIR, static_folder=BASE_DIR)
    app.config.from_object(Config)

    @app.route('/')
    def index():
        return render_template('index.html', assistant_name=Config.ASSISTANT_NAME, user_name=Config.USER_NAME, author=Config.AUTHOR)

    @app.route('/style.css')
    def serve_css():
        return send_from_directory(BASE_DIR, 'style.css', mimetype='text/css')

    @app.route('/app.js')
    def serve_js():
        return send_from_directory(BASE_DIR, 'app.js', mimetype='application/javascript')

    @app.route('/api/process', methods=['POST'])
    def process():
        data = request.get_json() or {}
        query = data.get('query', '')
        speak = data.get('speak', False)
        result = handler.process_command(query, speak_output=speak)
        return jsonify(result)

    @app.route('/api/system-status', methods=['GET'])
    def system_status():
        status = handler.system.get_system_status()
        return jsonify({"status": "online", "data": status})

    @app.route('/api/listen-mic', methods=['POST'])
    def listen_mic():
        text = handler.speech.listen_mic()
        if text:
            result = handler.process_command(text, speak_output=False)
            return jsonify({"success": True, "text": text, "result": result})
        return jsonify({"success": False, "error": "No voice detected or microphone unavailable."})

    @app.route('/api/speak', methods=['POST'])
    def speak():
        data = request.get_json() or {}
        text = data.get('text', '')
        if text:
            handler.speech.speak(text)
            return jsonify({"success": True})
        return jsonify({"success": False, "error": "No text provided"}), 400

except ImportError:
    HAS_FLASK = False
    app = None
    logger.info("Flask not found. Using built-in Python Zero-Dependency Web Server.")

# Zero-dependency Built-in HTTP Server Fallback (Runs even without pip install)
from http.server import HTTPServer, BaseHTTPRequestHandler

class JarvisHTTPHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress noisy logs

    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path in ('/', '/index.html'):
            html_path = os.path.join(BASE_DIR, 'index.html')
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # Simple template replacement
            content = content.replace('{{ assistant_name }}', Config.ASSISTANT_NAME)
            content = content.replace('{{ user_name }}', Config.USER_NAME)
            content = content.replace('{{ author }}', Config.AUTHOR)
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))

        elif self.path == '/style.css':
            css_path = os.path.join(BASE_DIR, 'style.css')
            with open(css_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/css; charset=utf-8')
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))

        elif self.path == '/app.js':
            js_path = os.path.join(BASE_DIR, 'app.js')
            with open(js_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript; charset=utf-8')
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))

        elif self.path == '/api/system-status':
            status = handler.system.get_system_status()
            res_data = json.dumps({"status": "online", "data": status})
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(res_data.encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'
        
        try:
            data = json.loads(post_body) if post_body else {}
        except Exception:
            data = {}

        if self.path == '/api/process':
            query = data.get('query', '')
            speak_val = data.get('speak', False)
            result = handler.process_command(query, speak_output=speak_val)
            res_data = json.dumps(result)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(res_data.encode('utf-8'))

        elif self.path == '/api/listen-mic':
            text = handler.speech.listen_mic()
            if text:
                result = handler.process_command(text, speak_output=False)
                res_data = json.dumps({"success": True, "text": text, "result": result})
            else:
                res_data = json.dumps({"success": False, "error": "No speech detected."})
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(res_data.encode('utf-8'))

        elif self.path == '/api/speak':
            text = data.get('text', '')
            if text:
                handler.speech.speak(text)
                res_data = json.dumps({"success": True})
            else:
                res_data = json.dumps({"success": False, "error": "No text"})
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(res_data.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_server(host, port, debug=False):
    """Run Flask or built-in HTTP server."""
    if HAS_FLASK and app:
        app.run(host=host, port=port, debug=debug)
    else:
        server = HTTPServer((host, port), JarvisHTTPHandler)
        server.serve_forever()

if __name__ == '__main__':
    run_server(Config.HOST, Config.PORT, Config.DEBUG)

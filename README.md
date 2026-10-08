# ⚡ JARVIS AI - Single-Directory Modular Voice Assistant

![JARVIS Banner](https://img.shields.io/badge/JARVIS-v2.0-00f3ff?style=for-the-badge)
![Developer](https://img.shields.io/badge/Author-Kirtan%20Patoliya-ffbe0b?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Single%20Directory-black?style=for-the-badge&logo=flask)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

An advanced AI Voice Assistant with a Cyberpunk Iron Man Holographic HUD, OpenRouter AI integration, OS system control, and voice recognition — structured in a **clean single flat directory without nested subfolders**.

> **Project Creator & Lead Developer:** **Kirtan Patoliya**  
> **Repository:** [JARVIS](https://github.com/patoliyakirtan/JARVIS)

---

## 📁 Single-Directory Flat Structure (No Subfolders)

All files sit directly in one root directory:

```text
JARVIS/
├── index.html            # Futuristic HUD Web Interface
├── style.css             # Cyberpunk Glowing HUD Styles
├── app.js                # Frontend Controller & Speech Engine
├── app.py                # Flask Server & REST APIs (serves root files)
├── run.py                # Main Startup Script (Web UI & CLI mode)
├── config.py             # Configuration & Environment Loader
├── command_handler.py    # Intent Parsing & Task Orchestration
├── ai_brain.py           # OpenRouter AI, Gemini & Offline Brain
├── speech_engine.py      # TTS & Microphone Voice Engine
├── system_controls.py    # System Volume, Diagnostics, App Launcher
├── web_actions.py        # Google, YouTube, Wikipedia, Weather
├── requirements.txt      # Python Dependencies
├── .env                  # Active Environment Configuration
├── .env.example          # Environment Template
├── .gitignore            # Git Exclusions
├── LICENSE               # MIT License (Author: Kirtan Patoliya)
└── README.md             # Documentation
```

---

## 🚀 Quick Start Guide

### 1. Run the Web HUD (Auto-opens in browser)
```bash
cd /Users/patoliyakirtan/.gemini/antigravity/scratch/JARVIS
python run.py
```
> Your browser will open **`http://localhost:8080`** automatically!

### 2. Terminal CLI Mode
```bash
python run.py --cli
```

---

## 📤 How to Upload to GitHub

```bash
cd /Users/patoliyakirtan/.gemini/antigravity/scratch/JARVIS

git init
git add .
git commit -m "Initial commit: Single directory JARVIS Assistant by Kirtan Patoliya"
git branch -M main
git remote add origin https://github.com/patoliyakirtan/JARVIS.git
git push -u origin main
```

---

## 👨‍💻 Author & Credits
- **Creator & Developer:** [Kirtan Patoliya](https://github.com/patoliyakirtan)
- **License:** MIT License © 2026 **Kirtan Patoliya**

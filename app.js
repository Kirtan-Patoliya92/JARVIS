/**
 * JARVIS HUD Frontend Controller
 * Supports Voice Input (Web Speech API + Backend Mic Fallback), Audio Synthesis, and Quick Actions.
 */

document.addEventListener('DOMContentLoaded', () => {
    const micBtn = document.getElementById('mic-btn');
    const sendBtn = document.getElementById('send-btn');
    const queryInput = document.getElementById('query-input');
    const consoleLogs = document.getElementById('console-logs');
    const assistantStatus = document.getElementById('assistant-status');
    const waveContainer = document.getElementById('wave-container');
    const reactorCore = document.getElementById('reactor-core');
    const reactorWrapper = document.getElementById('reactor-wrapper');
    const quickActionBtns = document.querySelectorAll('.action-tag');

    const cpuStat = document.getElementById('cpu-stat');
    const ramStat = document.getElementById('ram-stat');
    const batteryStat = document.getElementById('battery-stat');
    const timeClock = document.getElementById('time-clock');

    let recognition = null;
    let isListening = false;
    let synth = window.speechSynthesis;

    // 1. Clock Update
    function updateClock() {
        const now = new Date();
        timeClock.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    }
    setInterval(updateClock, 1000);
    updateClock();

    // 2. Fetch System Metrics
    async function fetchMetrics() {
        try {
            const res = await fetch('/api/system-status');
            const data = await res.json();
            if (data && data.data) {
                cpuStat.textContent = data.data.cpu_percent || '0%';
                ramStat.textContent = data.data.memory_percent || '0%';
                batteryStat.textContent = data.data.battery_percent !== 'N/A' ? data.data.battery_percent : 'AC Power';
            }
        } catch (err) {
            console.warn('System status fetch:', err);
        }
    }
    setInterval(fetchMetrics, 3500);
    fetchMetrics();

    // 3. Log Appender
    function appendLog(sender, text) {
        const now = new Date();
        const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        const entry = document.createElement('div');
        entry.className = `log-entry ${sender.toLowerCase()}`;
        entry.innerHTML = `<span class="timestamp">[${timeStr}] ${sender.toUpperCase()}:</span> ${text}`;
        
        consoleLogs.appendChild(entry);
        consoleLogs.scrollTop = consoleLogs.scrollHeight;
    }

    // 4. Speech Synthesis (TTS in Browser)
    function speak(text) {
        if (!text) return;
        if (synth) {
            try {
                synth.cancel();
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 1.0;
                utterance.pitch = 0.95;

                const voices = synth.getVoices();
                const preferredVoice = voices.find(v => v.lang.includes('en') && (v.name.includes('Google') || v.name.includes('Natural') || v.name.includes('Samantha') || v.name.includes('Daniel')));
                if (preferredVoice) {
                    utterance.voice = preferredVoice;
                }

                utterance.onstart = () => {
                    waveContainer.classList.add('active');
                    assistantStatus.textContent = "JARVIS IS SPEAKING...";
                };

                utterance.onend = () => {
                    waveContainer.classList.remove('active');
                    assistantStatus.textContent = "SYSTEM READY // AWAITING COMMAND";
                };

                utterance.onerror = (e) => {
                    console.warn("TTS Error:", e);
                    waveContainer.classList.remove('active');
                    assistantStatus.textContent = "SYSTEM READY // AWAITING COMMAND";
                };

                synth.speak(utterance);
            } catch (e) {
                console.warn("Speech synthesis failed:", e);
            }
        }
    }

    // 5. Process Command via Backend API
    async function sendCommand(text) {
        if (!text || !text.trim()) return;

        appendLog('User', text);
        queryInput.value = '';
        assistantStatus.textContent = "PROCESSING COMMAND...";
        waveContainer.classList.add('active');

        try {
            const res = await fetch('/api/process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: text, speak: false })
            });
            const data = await res.json();
            
            const reply = data.response || "Task executed, Sir.";
            appendLog('JARVIS', reply);
            speak(reply);

        } catch (error) {
            console.error('Command execution failed:', error);
            const errMsg = "Error communicating with JARVIS Core.";
            appendLog('SYSTEM', errMsg);
            assistantStatus.textContent = "ERROR OCCURRED";
            waveContainer.classList.remove('active');
        }
    }

    // 6. Backend Mic Fallback
    async function listenViaBackend() {
        assistantStatus.textContent = "LISTENING VIA SYSTEM MIC...";
        micBtn.classList.add('listening');
        micBtn.querySelector('.mic-text').textContent = 'LISTENING...';
        waveContainer.classList.add('active');
        appendLog('SYSTEM', 'Listening through microphone... Speak now.');

        try {
            const res = await fetch('/api/listen-mic', { method: 'POST' });
            const data = await res.json();
            
            micBtn.classList.remove('listening');
            micBtn.querySelector('.mic-text').textContent = 'VOICE';

            if (data.success && data.text) {
                appendLog('User', data.text);
                const reply = data.result?.response || "Done, Sir.";
                appendLog('JARVIS', reply);
                speak(reply);
            } else {
                appendLog('SYSTEM', data.error || 'No speech detected.');
                assistantStatus.textContent = "SYSTEM READY // AWAITING COMMAND";
                waveContainer.classList.remove('active');
            }
        } catch (err) {
            console.error('Backend mic error:', err);
            micBtn.classList.remove('listening');
            micBtn.querySelector('.mic-text').textContent = 'VOICE';
            assistantStatus.textContent = "SYSTEM READY // AWAITING COMMAND";
            waveContainer.classList.remove('active');
        }
    }

    // 7. Web Speech API Setup (Chrome / Safari / Edge)
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            isListening = true;
            micBtn.classList.add('listening');
            micBtn.querySelector('.mic-text').textContent = 'LISTENING...';
            assistantStatus.textContent = "VOICE INPUT ACTIVE... SPEAK NOW";
            waveContainer.classList.add('active');
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            sendCommand(transcript);
        };

        recognition.onerror = (event) => {
            console.warn('Speech recognition error:', event.error);
            isListening = false;
            micBtn.classList.remove('listening');
            micBtn.querySelector('.mic-text').textContent = 'VOICE';
            
            if (event.error === 'not-allowed') {
                appendLog('SYSTEM', '⚠️ Microphone access was blocked by browser. Please click the Lock icon in your address bar and allow Microphone.');
            } else if (event.error === 'no-speech') {
                appendLog('SYSTEM', 'No speech was detected. Click VOICE and speak again.');
            } else {
                appendLog('SYSTEM', `Voice recognition error: ${event.error}. Switching to system mic...`);
                listenViaBackend();
            }
            assistantStatus.textContent = "SYSTEM READY // AWAITING COMMAND";
            waveContainer.classList.remove('active');
        };

        recognition.onend = () => {
            isListening = false;
            micBtn.classList.remove('listening');
            micBtn.querySelector('.mic-text').textContent = 'VOICE';
            if (assistantStatus.textContent.includes("VOICE INPUT ACTIVE")) {
                assistantStatus.textContent = "SYSTEM READY // AWAITING COMMAND";
                waveContainer.classList.remove('active');
            }
        };
    }

    function toggleListening() {
        if (recognition) {
            if (isListening) {
                recognition.stop();
            } else {
                try {
                    recognition.start();
                } catch (e) {
                    console.warn("Recognition restart error:", e);
                    listenViaBackend();
                }
            }
        } else {
            listenViaBackend();
        }
    }

    // Event Listeners
    micBtn.addEventListener('click', toggleListening);
    if (reactorWrapper) {
        reactorWrapper.addEventListener('click', toggleListening);
    } else if (reactorCore) {
        reactorCore.addEventListener('click', toggleListening);
    }

    sendBtn.addEventListener('click', () => {
        sendCommand(queryInput.value);
    });

    queryInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            sendCommand(queryInput.value);
        }
    });

    // Quick Action Tags click event
    quickActionBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const cmd = btn.getAttribute('data-cmd');
            if (cmd) {
                sendCommand(cmd);
            }
        });
    });

    // Warm up voices on first user click
    window.addEventListener('click', () => {
        if (synth && synth.getVoices().length === 0) {
            synth.getVoices();
        }
    }, { once: true });
});

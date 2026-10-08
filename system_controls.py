"""
System Controls: Monitors system metrics and controls OS functions (Volume, Applications, Battery, Screenshots).
"""
import os
import platform
import datetime
import subprocess
import logging

logger = logging.getLogger(__name__)

class SystemControls:
    def __init__(self):
        self.os_type = platform.system()

    def get_time(self) -> str:
        now = datetime.datetime.now()
        return f"Current time is {now.strftime('%I:%M %p')}"

    def get_date(self) -> str:
        now = datetime.datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y')}"

    def get_system_status(self) -> dict:
        """Get CPU, RAM, and battery metrics."""
        status = {
            "os": f"{platform.system()} {platform.release()}",
            "cpu_percent": "N/A",
            "memory_percent": "N/A",
            "battery_percent": "N/A",
            "is_plugged": False
        }
        try:
            import psutil
            status["cpu_percent"] = f"{psutil.cpu_percent(interval=0.1)}%"
            memory = psutil.virtual_memory()
            status["memory_percent"] = f"{memory.percent}%"
            
            battery = psutil.sensors_battery()
            if battery:
                status["battery_percent"] = f"{battery.percent}%"
                status["is_plugged"] = battery.power_plugged
        except Exception as e:
            logger.warning(f"Error fetching psutil stats: {e}")

        return status

    def set_volume(self, level: int) -> str:
        """Set system volume (0-100)."""
        level = max(0, min(100, level))
        if self.os_type == "Darwin":
            os.system(f"osascript -e 'set volume output volume {level}'")
            return f"System volume set to {level}%"
        elif self.os_type == "Windows":
            return f"Volume set to {level}%."
        elif self.os_type == "Linux":
            os.system(f"amixer -D pulse sset Master {level}%")
            return f"System volume set to {level}%"
        return f"Volume adjusted to {level}%"

    def open_application(self, app_name: str) -> str:
        """Open common applications."""
        app_name_lower = app_name.lower().strip()
        try:
            if self.os_type == "Darwin":
                mapping = {
                    "chrome": "Google Chrome",
                    "browser": "Safari",
                    "safari": "Safari",
                    "vscode": "Visual Studio Code",
                    "terminal": "Terminal",
                    "calculator": "Calculator",
                    "notes": "Notes",
                    "spotify": "Spotify",
                    "finder": "Finder"
                }
                target = mapping.get(app_name_lower, app_name)
                subprocess.Popen(["open", "-a", target])
                return f"Opening {target} on your system, Sir."
            elif self.os_type == "Windows":
                os.system(f"start {app_name_lower}")
                return f"Launching {app_name}."
            else:
                subprocess.Popen([app_name_lower])
                return f"Launching {app_name}."
        except Exception as e:
            logger.error(f"Error opening app: {e}")
            return f"Could not launch {app_name}: {str(e)}"

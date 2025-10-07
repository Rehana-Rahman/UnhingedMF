import json
from pathlib import Path
from typing import Any, Dict, List

APP_DIR = Path.home() / ".unhingedmf"
APP_DIR.mkdir(exist_ok=True)

HISTORY_FILE = APP_DIR / "history.json"
CONFIG_FILE = APP_DIR / "config.json"

DEFAULT_CONFIG = {
    "model": "gemini-1.5-flash",
    "persona": "unhinged",
    "temperature": 1.1
}

class HistoryManager:
    def __init__(self):
        self.file = HISTORY_FILE

    def load(self) -> List[Dict[str, Any]]:
        if not self.file.exists():
            return []
        
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def append(self, role: str, content: str):
        history = self.load()
        history.append({"role": role, "parts": content})
        self._save(history)

    def clear(self):
        self._save([])

    def _save(self, history: List[Dict[str, Any]]):
        try:
            with open(self.file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except IOError:
            pass

class ConfigManager:
    def __init__(self):
        self.file = CONFIG_FILE
        self.config = self._load()

    def _load(self) -> Dict[str, Any]:
        if not self.file.exists():
            self._save(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
        
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                config = DEFAULT_CONFIG.copy()
                config.update(loaded)
                return config
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONFIG.copy()

    def get(self, key: str, default=None) -> Any:
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        self.config[key] = value
        self._save(self.config)

    def _save(self, config: Dict[str, Any]):
        try:
            with open(self.file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except IOError:
            pass

import json, os, pathlib
from typing import List, Dict, Any

APP_DIR = pathlib.Path(os.path.expanduser("~")) / ".unhingedmf"
APP_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_FILE = APP_DIR / "history.json"
CONFIG_FILE = APP_DIR / "config.json"

def load_history() -> List[Dict[str, Any]]:
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []

def save_history(history: List[Dict[str, Any]]) -> None:
    try:
        HISTORY_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass

def load_config() -> Dict[str, Any]:
    default = {"personality": "unhinged", "model": "gemini-1.5-flash", "temperature": 1.1}
    if CONFIG_FILE.exists():
        try:
            cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            default.update(cfg or {})
        except Exception:
            pass
    return default

def save_config(cfg: Dict[str, Any]) -> None:
    CONFIG_FILE.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")

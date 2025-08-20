from typing import List, Dict, Any, Optional
import google.generativeai as genai

def start_chat(api_key: str, model_name: str, system_prompt: str, history: Optional[List[Dict[str, str]]] = None, temperature: float = 1.0):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name, system_instruction=system_prompt)
    chat = model.start_chat(history=history or [])
    chat._temperature = temperature  # stored value
    return chat

def send(chat, message: str) -> str:
    resp = chat.send_message(message)
    return getattr(resp, "text", "").strip() or "(no response)"

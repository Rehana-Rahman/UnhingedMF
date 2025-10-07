import os
import google.generativeai as genai
from personas import PERSONAS, build_system_prompt

class ChatSession:
    def __init__(self, model, persona, temperature, history=None):
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        self.model_name = model
        self.persona = persona
        self.temperature = temperature
        self.history = history or []
        
        self._initialize()

    def _initialize(self):
        genai.configure(api_key=self.api_key)
        system_prompt = build_system_prompt(self.persona)
        
        self.model = genai.GenerativeModel(
            self.model_name,
            system_instruction=system_prompt
        )
        
        self.chat = self.model.start_chat(history=self.history)

    def send(self, message):
        generation_config = genai.types.GenerationConfig(
            temperature=self.temperature
        )
        
        response = self.chat.send_message(
            message,
            generation_config=generation_config
        )
        
        return response.text.strip()

    def reset(self):
        self.history = []
        self._initialize()

    def change_persona(self, persona):
        self.persona = persona
        current_history = [
            {"role": msg["role"], "parts": msg["parts"]}
            for msg in self.chat.history
        ]
        self.history = current_history
        self._initialize()

    def change_model(self, model_name):
        self.model_name = model_name
        current_history = [
            {"role": msg["role"], "parts": msg["parts"]}
            for msg in self.chat.history
        ]
        self.history = current_history
        self._initialize()

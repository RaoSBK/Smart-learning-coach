import google.generativeai as genai

class ExplainerAgent:
    def __init__(self, memory):
        self.memory = memory
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def explain(self, topic):
        prompt = f"""
Explain the topic simply using JSON format.

Topic: {topic}

Respond ONLY in JSON:
{{
  "explanation": "",
  "steps": [],
  "examples": []
}}
"""
        response = self.model.generate_content(prompt)
        return response.text

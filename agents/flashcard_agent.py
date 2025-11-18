import google.generativeai as genai
import json

class FlashcardAgent:

    def __init__(self, memory, model="gemini-2.0-flash"):
        self.memory = memory
        self.model = genai.GenerativeModel(model)

    def generate_flashcards(self, summary_json: dict):
        """
        Generate flashcards from structured summary JSON.
        """

        prompt = f"""
You are an AI flashcard generator.
Create simple, clear flashcards based on this structured video summary:

SUMMARY JSON:
{json.dumps(summary_json, indent=2)}

Return ONLY JSON like this:

{{
  "flashcards": [
      {{"question": "...", "answer": "..."}},
      {{"question": "...", "answer": "..."}}
  ]
}}
"""

        response = self.model.generate_content(prompt)
        result_text = response.text.strip()

        result_text = result_text.replace("```json", "").replace("```", "")

        try:
            result_json = json.loads(result_text)
        except:
            result_json = {"error": "Failed to parse flashcard JSON", "raw": result_text}

        self.memory.set("last_flashcards", result_json)
        return result_json

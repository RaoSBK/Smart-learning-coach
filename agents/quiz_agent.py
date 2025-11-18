import google.generativeai as genai
import json

class QuizAgent:

    def __init__(self, memory, model="gemini-2.0-flash"):
        self.memory = memory
        self.model = genai.GenerativeModel(model)

    def generate_quiz(self, summary_json: dict, num_questions=5):
        """
        Generate MCQ quiz from summary data.
        """

        prompt = f"""
You are an AI quiz generator.

Create {num_questions} high-quality MCQs based ONLY on this video summary:

SUMMARY JSON:
{json.dumps(summary_json, indent=2)}

Return only JSON:

{{
  "quiz": [
     {{
       "question": "...",
       "options": ["A...", "B...", "C...", "D..."],
       "answer": "B",
       "explanation": "..."
     }}
  ]
}}
"""

        response = self.model.generate_content(prompt)
        result_text = response.text.strip()
        result_text = result_text.replace("```json", "").replace("```", "")

        try:
            result_json = json.loads(result_text)
        except:
            result_json = {"error": "Failed to parse quiz JSON", "raw": result_text}

        self.memory.set("last_quiz", result_json)
        return result_json

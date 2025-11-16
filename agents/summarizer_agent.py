import google.generativeai as genai
import json

class SummarizerAgent:

    def __init__(self, memory, model="gemini-2.0-flash"):
        self.memory = memory
        self.model = genai.GenerativeModel(model)

    def summarize(self, transcript_text: str, metadata: dict):
        """
        Takes transcript + metadata and returns structured JSON summary.
        """

        prompt = f"""
You are an AI YouTube video summarizer.
Summarize the video transcript in a structured JSON format.

VIDEO TITLE: {metadata.get("title", "Unknown Title")}
CHANNEL: {metadata.get("channel", "Unknown")}
PUBLISH DATE: {metadata.get("publish_date", "Unknown")}

TRANSCRIPT:
{transcript_text}

Return ONLY JSON like this:

{{
  "short_summary": "...",
  "detailed_summary": "...",
  "key_points": ["...", "..."],
  "study_notes": ["...", "..."],
  "chapters": ["...", "..."],
  "tags": ["...", "..."]
}}
"""

        response = self.model.generate_content(prompt)

        result_text = response.text.strip()

        # Remove markdown fences if Gemini includes them
        result_text = result_text.replace("```json", "").replace("```", "").strip()

        # Try converting to JSON
        try:
            result_json = json.loads(result_text)
        except Exception:
            result_json = {
                "error": "Could not parse JSON from model.",
                "raw_output": result_text
            }

        # Save memory
        self.memory.set("last_video_summary", result_json)

        return result_json

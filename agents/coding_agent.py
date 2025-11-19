# agents/coding_agent.py
import google.generativeai as genai
from typing import Optional

class CodingTutorAgent:
    """
    Simple coding tutor wrapper for Gemini (works with the MemoryBank pattern).
    Constructor signature accepts either a memory object (if your project's agents use memory)
    or a model string as second arg.
    """

    def __init__(self, memory: Optional[object] = None, model: str = "gemini-2.0-flash"):
        # memory is optional so this agent won't break if your project expects memory objects
        self.memory = memory
        self.model_name = model
        self.model = genai.GenerativeModel(model)

    def ask(self, user_prompt: str) -> str:
        """
        Generic ask method that forwards a coding-related prompt to Gemini and returns text.
        """
        prompt = f"""You are an expert coding tutor. Be concise, explain clearly and, when returning code,
return only code in a fenced block when asked to provide corrected or new code.

User request:
{user_prompt}
"""
        response = self.model.generate_content(prompt)
        return response.text

    def explain_code(self, code: str, language: str = "Python") -> str:
        prompt = f"Explain the following {language} code, line-by-line, in simple words. Show expected output if relevant.\n\n```\n{code}\n```"
        return self.ask(prompt)

    def fix_code(self, code: str, language: str = "Python") -> str:
        prompt = f"Find and fix bugs in this {language} code. Return the corrected code inside a single fenced code block and then give a 1-2 line explanation of the fix.\n\n```\n{code}\n```"
        return self.ask(prompt)

    def write_code(self, task: str, language: str = "Python") -> str:
        prompt = f"Write {language} code for this task. Provide the code inside a fenced code block, then provide brief step-by-step reasoning after the block.\n\nTASK:\n{task}"
        return self.ask(prompt)

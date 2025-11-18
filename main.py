from dotenv import load_dotenv
import google.generativeai as genai
import os

from agents.planner_agent import PlannerAgent
from agents.explainer_agent import ExplainerAgent
from agents.summarizer_agent import SummarizerAgent
from tools.youtube_tool import YouTubeTranscriptTool
from tools.pdf_exporter import PDFExporter
from memory.memory_bank import MemoryBank
from agents.flashcard_agent import FlashcardAgent
from agents.quiz_agent import QuizAgent



def main():
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    memory = MemoryBank()

    planner = PlannerAgent(memory)
    explainer = ExplainerAgent(memory)
    summarizer = SummarizerAgent(memory)

    # 1. Normal plan + explanation
    print("📘 Study Plan:")
    plan = planner.create_plan(["Digital Electronics", "C Programming", "Maths"], "2025-12-01", 3)
    print(plan)

    print("\n🧠 Explanation:")
    explanation = explainer.explain("JK Flip-Flop")
    print(explanation)

    #2. youtube summarizer
    print("\n🎥 YouTube Summary:")

    url = "https://www.youtube.com/watch?v=rfscVS0vtbw"

    metadata = YouTubeTranscriptTool.get_metadata(url)
    transcript = YouTubeTranscriptTool.get_transcript(url)

    summary = summarizer.summarize(transcript, metadata)

    print(summary)

    # Export PDF
    filename = PDFExporter.export_summary_to_pdf(summary, metadata, "youtube_summary.pdf")

    print(f"\n📄 PDF exported successfully: {filename}")


    # ======================
    # FLASHCARDS
    # ======================
    flashcards = FlashcardAgent(memory).generate_flashcards(summary)
    flashcard_pdf = PDFExporter.export_flashcards_to_pdf(flashcards, "flashcards.pdf")
    print(f"📘 Flashcards exported: {flashcard_pdf}")

    # ======================
    # QUIZ (MCQs)
    # ======================
    quiz = QuizAgent(memory).generate_quiz(summary, num_questions=5)
    quiz_pdf = PDFExporter.export_quiz_to_pdf(quiz, "quiz.pdf")
    print(f"📝 Quiz exported: {quiz_pdf}")





if __name__ == "__main__":
    main()

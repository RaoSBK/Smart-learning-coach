# app.py
import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
import json
from io import BytesIO

# Import your project agents/tools
from memory.memory_bank import MemoryBank
from agents.planner_agent import PlannerAgent
from agents.explainer_agent import ExplainerAgent
from agents.summarizer_agent import SummarizerAgent
from agents.flashcard_agent import FlashcardAgent
from agents.quiz_agent import QuizAgent
from agents.coding_agent import CodingTutorAgent
from tools.youtube_tool import YouTubeTranscriptTool
from tools.pdf_exporter import PDFExporter

# Load environment and configure Gemini
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Constants
MODEL = os.getenv("AGENT_MODEL", "gemini-2.0-flash")  # change if needed
SAMPLE_IMAGE_PATH = "bg.png"  # uploaded image path

# Initialize shared objects
@st.cache_resource
def init_agents():
    memory = MemoryBank()
    planner = PlannerAgent(memory)
    explainer = ExplainerAgent(memory)
    summarizer = SummarizerAgent(memory)
    flashcard_agent = FlashcardAgent(memory)
    quiz_agent = QuizAgent(memory)
    coding_tutor = CodingTutorAgent(memory, model=MODEL)
    pdf_exporter = PDFExporter()
    return {
        "memory": memory,
        "planner": planner,
        "explainer": explainer,
        "summarizer": summarizer,
        "flashcard_agent": flashcard_agent,
        "quiz_agent": quiz_agent,
        "coding_tutor": coding_tutor,
        "pdf": pdf_exporter,
    }

agents = init_agents()

st.set_page_config(page_title="Smart Learning Coach", layout="wide")
st.title(" Smart Learning Coach — Streamlit UI")

# Sidebar navigation
st.sidebar.header("Actions")
page = st.sidebar.selectbox(
    "Choose action",
    [
        "Study Planner",
        "Explain Concept",
        "YouTube Summarizer",
        "Flashcards & Quiz",
        "Coding Tutor",
        "Files & Downloads",
    ],
)

st.sidebar.markdown("---")
st.sidebar.image(SAMPLE_IMAGE_PATH, width=180)
st.sidebar.markdown("Built with Gemini + Streamlit")

# creating files for downloading
def get_file_download_link_bytes(filepath, download_name=None):
    if not os.path.exists(filepath):
        return None
    with open(filepath, "rb") as f:
        data = f.read()
    download_name = download_name or os.path.basename(filepath)
    return BytesIO(data), download_name

# PAGE: Study Planner
if page == "Study Planner":
    st.header("Study Planner")
    with st.form("planner_form"):
        subjects_text = st.text_area("Subjects (comma-separated)", value="Digital Electronics, C Programming, Maths")
        exam_date = st.text_input("Exam date (YYYY-MM-DD)", value="2025-12-01")
        hours_per_day = st.number_input("Hours per day", min_value=1, max_value=12, value=3)
        submit = st.form_submit_button("Generate Study Plan")
    if submit:
        subjects = [s.strip() for s in subjects_text.split(",") if s.strip()]
        plan = agents["planner"].create_plan(subjects, exam_date, hours_per_day)
        st.subheader("Generated Plan")
        st.json(plan)
        agents["memory"].set("last_plan", plan)

# PAGE: Explain Concept
elif page == "Explain Concept":
    st.header("Concept Explainer")
    topic = st.text_input("Enter topic (e.g., JK Flip-Flop)", value="JK Flip-Flop")
    level = st.selectbox("Level", ["simple", "medium", "deep"])
    if st.button("Explain"):
        with st.spinner("Generating explanation..."):
            try:
                result = agents["explainer"].explain(f"{topic} (level={level})")
            except Exception as e:
                st.error(f"Error calling explainer agent: {e}")
                result = str(e)
        st.subheader("Explanation")
        st.text(result)
        agents["memory"].set("last_explained_topic", topic)
        agents["memory"].set("last_explanation", result)

# PAGE: YouTube Summarizer
elif page == "YouTube Summarizer":
    st.header("YouTube Summarizer")
    url = st.text_input("YouTube URL", value="https://youtu.be/qYNweeDHiyU?si=TMilEAI2RsxxytLI")
    max_chars = st.slider("Max characters of transcript to send to model", 1000, 20000, 15000)
    if st.button("Fetch & Summarize"):
        with st.spinner("Fetching transcript..."):
            try:
                metadata = YouTubeTranscriptTool.get_metadata(url)
                transcript = YouTubeTranscriptTool.get_transcript(url)
            except Exception as e:
                st.error(f"Error fetching transcript/metadata: {e}")
                metadata, transcript = {"error": str(e)}, None

        if transcript is None:
            st.warning("Transcript not available; using metadata fallback.")
        st.subheader("Metadata")
        st.json(metadata)
        if transcript:
            st.subheader("Transcript (truncated)")
            st.text(transcript[:max_chars] + ("..." if len(transcript) > max_chars else ""))

        with st.spinner("Generating summary..."):
            try:
                summary = agents["summarizer"].summarize(transcript, metadata)
            except Exception as e:
                st.error(f"Error generating summary: {e}")
                summary = {"error": str(e)}

        st.subheader("Summary")
        st.json(summary)

        # Export summary PDF
        try:
            pdf_path = "youtube_summary.pdf"
            agents["pdf"].export_summary_to_pdf(summary, metadata, pdf_path)
            bio_bytes, dl_name = get_file_download_link_bytes(pdf_path)
            if bio_bytes:
                st.download_button("Download Summary PDF", data=bio_bytes, file_name=dl_name, mime="application/pdf")
        except Exception as e:
            st.error(f"PDF export failed: {e}")

# PAGE: Flashcards & Quiz
elif page == "Flashcards & Quiz":
    st.header("Flashcards & Quiz")
    if st.button("Generate Flashcards & Quiz from last summary"):
        last_summary = agents["memory"].get("last_video_summary") or agents["memory"].get("last_summary")
        if not last_summary:
            st.warning("No summary found in memory. Please run YouTube Summarizer first or paste a summary.")
        else:
            with st.spinner("Generating flashcards..."):
                try:
                    flashcards = agents["flashcard_agent"].generate_flashcards(last_summary)
                except Exception as e:
                    st.error(f"Error generating flashcards: {e}")
                    flashcards = {"error": str(e)}
            st.subheader("Flashcards")
            st.json(flashcards)

            # Export flashcards PDF
            try:
                flash_pdf_path = "flashcards.pdf"
                agents["pdf"].export_flashcards_to_pdf({"flashcards": flashcards}, flash_pdf_path)
                bio_bytes, dl_name = get_file_download_link_bytes(flash_pdf_path)
                if bio_bytes:
                    st.download_button("Download Flashcards PDF", data=bio_bytes, file_name=dl_name, mime="application/pdf")
            except Exception as e:
                st.error(f"Flashcard PDF export failed: {e}")

            # Generate quiz
            with st.spinner("Generating quiz..."):
                try:
                    quiz = agents["quiz_agent"].generate_quiz(last_summary)
                except Exception as e:
                    st.error(f"Error generating quiz: {e}")
                    quiz = {"quiz": []}
            st.subheader("Quiz (MCQs)")
            st.json(quiz)

            try:
                quiz_pdf_path = "quiz.pdf"
                agents["pdf"].export_quiz_to_pdf(quiz, quiz_pdf_path)
                bio_bytes, dl_name = get_file_download_link_bytes(quiz_pdf_path)
                if bio_bytes:
                    st.download_button("Download Quiz PDF", data=bio_bytes, file_name=dl_name, mime="application/pdf")
            except Exception as e:
                st.error(f"Quiz PDF export failed: {e}")

# PAGE: Coding Tutor
elif page == "Coding Tutor":
    st.header("Coding Tutor")
    mode = st.radio("Mode", ["Explain code", "Fix code", "Write code"])
    if mode == "Explain code":
        code_input = st.text_area("Paste code to explain", value="def add(a, b):\n    return a + b")
        if st.button("Explain Code"):
            with st.spinner("Explaining code..."):
                try:
                    out = agents["coding_tutor"].explain_code(code_input, language="Python")
                except Exception as e:
                    st.error(f"Error from coding tutor: {e}")
                    out = str(e)
            st.subheader("Explanation")
            st.text(out)

    elif mode == "Fix code":
        code_input = st.text_area("Paste buggy code", value="for i in range(5)\nprint(i)")
        if st.button("Fix Code"):
            with st.spinner("Fixing code..."):
                try:
                    out = agents["coding_tutor"].fix_code(code_input, language="Python")
                except Exception as e:
                    st.error(f"Error from coding tutor: {e}")
                    out = str(e)
            st.subheader("Fixed Code")
            st.text(out)

    else:  # Write code
        prompt_input = st.text_area("Describe the task", value="Write Python code to reverse a linked list.")
        if st.button("Generate Code"):
            with st.spinner("Generating code..."):
                try:
                    out = agents["coding_tutor"].write_code(prompt_input, language="Python")
                except Exception as e:
                    st.error(f"Error from coding tutor: {e}")
                    out = str(e)
            st.subheader("Generated Code + Reasoning")
            st.text(out)

# PAGE: Files & Downloads
elif page == "Files & Downloads":
    st.header("Files & Downloads")
    st.write("Generated files in the working directory (if present):")
    for fname in ["youtube_summary.pdf", "flashcards.pdf", "quiz.pdf"]:
        if os.path.exists(fname):
            st.write(f"- {fname}")
            bio_bytes, dl_name = get_file_download_link_bytes(fname)
            if bio_bytes:
                st.download_button(f"Download {fname}", data=bio_bytes, file_name=dl_name, mime="application/pdf")
        else:
            st.write(f"- {fname} (not found)")

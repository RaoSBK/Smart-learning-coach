# 📘 Smart Learning Coach — AI Study Assistant  
Built with **Gemini 2.0 Flash**, **Python**, and **Streamlit**

Smart Learning Coach is an AI-powered study assistant designed to help students learn efficiently using the power of Google's Gemini 2.0 models.  
It includes:

- 📚 Study Plan Generator  
- 🧠 Concept Explainer  
- 🎥 YouTube Video Summarizer  
- 📝 Flashcards + Quiz Generator  
- 💻 AI Coding Tutor  
- 📄 PDF Export (Summary, Flashcards, Quiz)  
- 🌐 Streamlit Web UI  

---

# 🚀 Features

### ✔ 1. **Study Planner**
Generates a personalized day-wise plan based on subjects, exam date, and daily study hours.

### ✔ 2. **Concept Explainer**
Explains any topic in simple, medium, or advanced levels.

### ✔ 3. **YouTube Summarizer**
Extracts transcript → generates summary, study notes, chapters, tags.

### ✔ 4. **Flashcards Generator**
Creates JSON-structured flashcards based on summaries.

### ✔ 5. **Quiz / MCQ Generator**
Creates exam-ready MCQs with answers & explanations.

### ✔ 6. **AI Coding Tutor**
- Explains code  
- Fixes debugging errors  
- Writes code with step-by-step reasoning  

### ✔ 7. **PDF Exporter**
Exports:
- YouTube summary → `youtube_summary.pdf`  
- Flashcards → `flashcards.pdf`  
- Quiz → `quiz.pdf`  

### ✔ 8. **Streamlit Web App**
Clean UI with dropdown-based navigation.

---

# 📁 Project Folder Structure

```txt
Smart-Learning-Coach/
│
├── agents/
│   ├── planner_agent.py
│   ├── explainer_agent.py
│   ├── summarizer_agent.py
│   ├── flashcard_agent.py
│   ├── quiz_agent.py
│   ├── coding_agent.py
│
├── tools/
│   ├── youtube_tool.py
│   ├── pdf_exporter.py
│
├── memory/
│   ├── memory_bank.py
│
├── app.py                # Streamlit UI
├── main.py               # CLI version
├── requirements.txt
├── .env                  # env file for API Key
├── README.md

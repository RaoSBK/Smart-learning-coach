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

---

# 🚀 Features

### 1. **Study Planner**
Generates a personalized day-wise plan based on subjects, exam date, and daily study hours.

### 2. **Concept Explainer**
Explains any topic in simple, medium, or advanced levels.

### 3. **YouTube Summarizer**
Extracts transcript → generates summary, study notes, chapters, tags.

### 4. **Flashcards Generator**
Creates JSON-structured flashcards based on summaries.

### 5. **Quiz / MCQ Generator**
Creates exam-ready MCQs with answers & explanations.

### 6. **AI Coding Tutor**
- Explains code  
- Fixes debugging errors  
- Writes code with step-by-step reasoning  

### 7. **PDF Exporter**
Exports:
- YouTube summary → `youtube_summary.pdf`  
- Flashcards → `flashcards.pdf`  
- Quiz → `quiz.pdf`  


---

#  Project Folder Structure

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
;
```

###  **Setting Up API Key**

    1. Go to https://aistudio.google.com

    2. Generate a Gemini API Key

    3.. Create a .env file: 
        GEMINI_API_KEY=YOUR_API_KEY_HERE

---

## Installation Guide
1. Clone the project
    git clone https://github.com/yourusername/smart-learning-coach.git
    cd smart-learning-coach

2. Create & activate virtual environment
    python -m venv venv
    venv\Scripts\activate        # Windows

3. Install dependencies
    pip install -r requirements.txt

4. Install dependencies 
    pip install youtube-transcript-api 

5.  Install dependencies 
    pip install yt-dlp  

6. Install dependencies 
    pip install reportlab 

7. Run Streamlit App 
    streamlit run app.py 

---

## User Interface
- **YouTube Link:** https://www.youtube.com/watch?v=O59yEL2BI-0 

---

## PDF Export — Examples
    1. youtube_summary.pdf
    2. quiz.pdf
    3. flshcard.pdf

---

# License

MIT License © 2025

---

# Future Improvements
- Text-to-Speech summary reading

- Audio-based learning

- Add NCERT / university syllabus packs

- Personalized learning analytics

- Deploy on cloud (Render / HuggingFace / GCP)

- Add interactive coding sandbox

- Add long-term learning memory system

---

# Credits

Made by Suraj Bhan  
Powered by:

- Gemini 2.0 Flash

- Streamlit    

-  Python

- ReportLab

- YouTube Transcript API

---

#  Contact

If you have any questions, suggestions, or would like to collaborate, feel free to reach out!

- **Developer:** Suraj  Bhan Kumar  
- **Project:** Smart Learning Coach – AI Study Assistant  

- **Email:** surajbhan20005@gmail.com  
- **GitHub:** https://github.com/RaoSBK   
- **LinkedIn:** https://www.linkedin.com/in/surajbhankumar/  
- **Kaggle:** https://www.kaggle.com/raosbk   
- **Youtube link:** https://www.youtube.com/watch?v=O59yEL2BI-0   

---
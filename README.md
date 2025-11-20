💼 AI Career Path Recommender

An intelligent career recommendation system powered by LangGraph, Gemini AI, FastAPI, and Streamlit

🚀 Overview

AI Career Path Recommender is an end-to-end AI system that analyzes a user’s degree, skills, and interests to generate:

A personalized career analysis

Top 3 recommended career paths

Skill gap visualizations

Job-fit insights and demand metrics

Resume ingestion (PDF)

User profile saving system

It combines LangGraph (Agent Workflow), Gemini AI (LLM), FastAPI (Backend), and Streamlit (UI) into one seamless career-guidance tool.

🧠 Features
✔️ AI-Powered Career Analysis

Processes your academic background, skills, and interests using Gemini Flash.

✔️ Intelligent Career Recommendations

Each career includes:

Why it fits you

Top 5 essential skills

Skill gap radar visualization

Learning resources

✔️ Skill Gap Visualization

Generated using Plotly Polar Charts.

✔️ Resume Parsing (PDF)

Extracts text from PDF resumes to supplement your profile.

✔️ Saves User Profiles

Stores past evaluations locally in user_history/.

✔️ Full Agent Workflow

LangGraph handles multi-step reasoning:

Background Analysis

Career Recommendations

✔️ FastAPI Backend

Provides clean REST API for the Streamlit frontend.

✔️ Modern UI

Built with Streamlit & custom CSS cards.

🏗️ Tech Stack
Layer	Technology
AI Model	Gemini 2.0 Flash
Agent Framework	LangGraph
Prompting	LangChain
Backend	FastAPI
Frontend	Streamlit
Charts	Plotly
Resume Parsing	PyPDF2
Storage	Local JSON history
📂 Project Structure
AI-Career-Path-Recommender/
│
├── graph_agent.py          # LangGraph agent pipeline
├── app.py                  # FastAPI backend
├── main.py                 # Streamlit frontend
├── user_history/           # Stored profiles
├── requirements.txt
└── README.md

⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/yourusername/ai-career-path-recommender.git
cd ai-career-path-recommender

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Add Environment Variables

Create a .env file:

GOOGLE_API_KEY=your_api_key_here

▶️ Running the Project
1️⃣ Start FastAPI Backend
uvicorn app:app --reload --port 9000

2️⃣ Start Streamlit Frontend
streamlit run main.py

The app will be live at:

👉 http://localhost:8501

FastAPI docs available at:
👉 http://localhost:9000/newdocs

📌 API Endpoint
POST /recommend-career

Request Body

{
  "degree": "BS Computer Science",
  "skills": "Python, SQL, Machine Learning",
  "interests": "AI, Data Science"
}


Response Example

{
  "analysis": "This person has strong analytical background...",
  "recommendations": [...]
}

🧩 LangGraph Workflow
[ analyze_background ] → [ recommend_paths ] → END


Node 1: Summarizes your background

Node 2: Generates structured JSON recommendations

📊 Visual Insights

The Insights tab provides:

Job fit score

Job demand score

Combined bar visualization

Skill-radar charts per role

🛠️ Requirements

Add this to requirements.txt:

langchain
langgraph
fastapi
uvicorn
python-dotenv
streamlit
requests
PyPDF2
plotly
pandas
langchain-google-genai

🤝 Contributing

Pull requests are welcome! Feel free to submit enhancements, bugs, or new features.

📜 License

This project is licensed under the MIT License.

⭐ Support

If this project helped you, consider giving it a GitHub Star ⭐ to support development!

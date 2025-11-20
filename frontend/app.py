import streamlit as st
import requests
import json
import matplotlib.pyplot as plt
import PyPDF2
import os
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import pandas as pd

# ------------------ CONFIG ------------------
st.set_page_config(page_title="💼 AI Career Path Recommender", page_icon="🤖", layout="wide")
FASTAPI_URL = "https://ai-career-path-1.onrender.com/"  # FastAPI URL

# ------------------ CUSTOM CSS ------------------
st.markdown(
    """
    <style>
    body, .stApp {
        font-family: "Poppins", sans-serif;
    }

    h1 {
        text-align: center;
        animation: fadeIn 1s ease-in-out;
    }

    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(-10px);}
        to   {opacity: 1; transform: translateY(0);}
    }

    /* Card used for each recommendation */
    .recommend-card {
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.18);
        transition: 0.3s;
        opacity: 1 !important;
        color: #000 !important;
        position: relative;
        z-index: 2;
    }

    .recommend-card:hover {
        transform: translateY(-5px);
        box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.25);
    }

    /* Ensure text inside card is not faded */
    .recommend-card * {
        opacity: 1 !important;
        color: inherit !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ------------------ LOAD SAVED PROFILES ------------------
st.sidebar.subheader("🗂️ Saved Profiles")
Path("user_history").mkdir(exist_ok=True)
profiles = [f for f in os.listdir("user_history") if f.endswith(".json")]

if profiles:
    selected_profile = st.sidebar.selectbox("Select a saved profile", profiles)
    if st.sidebar.button("Load Profile"):
        with open(f"user_history/{selected_profile}") as f:
            loaded = json.load(f)
        st.session_state["degree"] = loaded.get("degree", "")
        st.session_state["skills"] = loaded.get("skills", "")
        st.session_state["interests"] = loaded.get("interests", "")
        st.success(f"Loaded profile: {selected_profile}")
else:
    st.sidebar.info("No saved profiles yet.")

# ------------------ HEADER ------------------
st.title("💼 AI Career Path Recommender")
st.markdown("### 🚀 Discover your ideal AI career path based on your background, skills, and interests.")

# ------------------ TABS ------------------
tab1, tab2, tab3 = st.tabs(["🧾 Input & Resume", "🎯 Recommendations", "📊 Insights & Visuals"])

# ------------------ TAB 1: INPUT & RESUME ------------------
with tab1:
    uploaded_file = st.file_uploader("📄 Upload your Resume (PDF optional)", type=["pdf"])
    resume_text = ""
    if uploaded_file:
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            resume_text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
            st.success("✅ Resume successfully read!")
        except Exception as e:
            st.error(f"⚠️ Could not process resume: {e}")

    st.subheader("🎓 Tell us about your background")
    degree = st.text_input("🎓 Degree", st.session_state.get("degree", ""))
    skills = st.text_area("⚙️ Skills (comma-separated)", st.session_state.get("skills", ""))
    interests = st.text_area("❤️ Interests", st.session_state.get("interests", ""))

    if st.button("✨ Get AI Recommendations"):
        if not degree or not skills or not interests:
            st.warning("⚠️ Please fill out all fields before submitting.")
        else:
            with st.spinner("🔍 Analyzing your profile..."):
                try:
                    response = requests.post(f"{FASTAPI_URL}/recommend-career", json={
                        "degree": degree,
                        "skills": skills,
                        "interests": interests
                    })
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state["analysis"] = data.get("analysis", "")
                        st.session_state["recommendations_raw"] = data.get("recommendations", [])

                        st.success("✅ Analysis complete! Go to '🎯 Recommendations' tab.")
                        user_data = {
                            "degree": degree,
                            "skills": skills,
                            "interests": interests,
                            "recommendations": data
                        }
                        with open(f"user_history/{degree.replace(' ', '_')}_profile.json", "w") as f:
                            json.dump(user_data, f, indent=4)
                    else:
                        st.error(f"❌ API Error: {response.status_code}")
                except Exception as e:
                    st.error(f"⚠️ Something went wrong: {e}")

# ------------------ TAB 2: RECOMMENDATIONS & SKILL GAP ------------------
with tab2:
    recommendations = st.session_state.get("recommendations_raw", [])

    # Parse if string
    if isinstance(recommendations, str):
        try:
            cleaned = recommendations.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned.replace("```json", "").replace("```", "")
            recommendations = json.loads(cleaned)
        except Exception:
            st.warning("⚠️ Could not parse JSON — showing empty list.")
            recommendations = []

    if recommendations:
        st.subheader("🧠 Analysis")
        st.write(st.session_state.get("analysis", ""))

        user_skills_set = set([s.strip().lower() for s in skills.split(",")])

        for rec in recommendations:
            if not isinstance(rec, dict):
                continue
            title = rec.get("Career Title", "Unknown Role")
            why = rec.get("Why it fits them", "N/A")
            st.markdown(f"""
            <div class='recommend-card'>
                <h3>🎯 {title}</h3>
                <p><b>Why it fits you:</b> {why}</p>
            </div>
            """, unsafe_allow_html=True)

            top_skills = rec.get("Top 5 skills to learn", [])
            if top_skills:
                st.markdown("**🧩 Top 5 Skills to Learn for this Role:**")
                st.write(", ".join(top_skills))

                # Skill Gap Radar
                all_skills_set = set([s.strip().lower() for s in top_skills])
                current = [100 if s.strip().lower() in user_skills_set else 50 for s in top_skills]
                required = [100] * len(top_skills)
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(r=current, theta=top_skills, fill='toself', name='Your Skills'))
                fig.add_trace(go.Scatterpolar(r=required, theta=top_skills, fill='toself', name='Required Skills'))
                fig.update_layout(title=f"🧠 Skill Gap for {title}",
                                  polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True)
                st.plotly_chart(fig)

                for skill in top_skills:
                    if skill.strip().lower() in user_skills_set:
                        st.success(f"✅ You already have {skill}")
                    else:
                        st.warning(f"⚠️ You need to learn/improve: {skill}")
    else:
        st.info("👆 Please generate recommendations first in the Input tab.")

# ------------------ TAB 3: INSIGHTS & JOB DEMAND ------------------
with tab3:
    st.subheader("📊 Personalized Career Insights")
    recommendations = st.session_state.get("recommendations_raw", [])

    if isinstance(recommendations, str):
        try:
            cleaned = recommendations.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned.replace("```json", "").replace("```", "")
            recommendations = json.loads(cleaned)
        except Exception:
            recommendations = []

    if recommendations:
        user_skills_set = set([s.strip().lower() for s in skills.split(",")])
        insights = []

        for rec in recommendations:
            if not isinstance(rec, dict):
                continue
            title = rec.get("Career Title", "Unknown Role")
            top_skills = rec.get("Top 5 skills to learn", [])
            top_skills_set = set([s.strip().lower() for s in top_skills])
            fit_count = sum(1 for s in user_skills_set if s in top_skills_set)
            fit_score = int((fit_count / len(top_skills)) * 100) if top_skills else 0
            demand_score = rec.get("Demand", 80)
            insights.append({
                "Career": title,
                "Fit": fit_score,
                "Demand": demand_score
            })

        if insights:
            df = pd.DataFrame(insights).sort_values(by=["Fit", "Demand"], ascending=False)
            fig = px.bar(df, x="Career", y=["Fit", "Demand"], barmode="group",
                         title="🎯 Personalized Job Demand & Fit Based on Your Profile", text_auto=True)
            st.plotly_chart(fig)
        else:
            st.info("Generate recommendations first to see insights.")
    else:
        st.info("👆 Please generate recommendations first in the Input tab.")

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:gray;'>💡 Built with ❤️ using Streamlit | AI Career Path Recommender v2</p>",
    unsafe_allow_html=True)
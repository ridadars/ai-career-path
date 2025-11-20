from fastapi import FastAPI
from pydantic import BaseModel
from .graph_agent import career_agent

# -------------------------------
# FastAPI App with Custom Docs
# -------------------------------
app = FastAPI(
    title="AI Career Path Recommender",
    docs_url="/newdocs",        # Swagger UI at /new-docs
    redoc_url="/newredoc"       # ReDoc at /new-redoc
)

# -------------------------------
# Career Recommendation Endpoint
# -------------------------------
class CareerInput(BaseModel):
    degree: str
    skills: str
    interests: str

@app.post("/recommend-career")
async def recommend_career(data: CareerInput):
    # Prepare input state for the LangGraph agent
    state = {
        "degree": data.degree,
        "skills": data.skills,
        "interests": data.interests
    }

    # Run the AI agent
    result = career_agent.invoke(state)

    # Return structured output
    return {
        "analysis": result.get("analysis", "No analysis generated."),
        "recommendations": result.get("recommendations", "No recommendations found.")
    }


# -------------------------------
# Root Route
# -------------------------------
@app.get("/")
async def root():
    return {"message": "✅ AI Career Path Recommender API is running! Visit /newdocs for Swagger UI."}
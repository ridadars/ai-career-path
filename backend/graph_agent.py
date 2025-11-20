from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from typing import TypedDict, List
import os
from dotenv import load_dotenv

load_dotenv()

# Define the state (data that flows through the graph)
class CareerState(TypedDict):
    degree: str
    skills: str
    interests: str
    analysis: str
    recommendations: List[str]

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key= os.getenv("GOOGLE_API_KEY"), temperature=0.7)

# Step 1: Analyze background
def analyze_background(state: CareerState):
    prompt = ChatPromptTemplate.from_template("""
    You are a career analyst. Given this user profile:
    Degree: {degree}
    Skills: {skills}
    Interests: {interests}
    Write a short analysis summarizing their background and potential strengths.
    """)
    chain = prompt | llm
    response = chain.invoke(state)
    state["analysis"] = response.content
    return state

# Step 2: Recommend career paths
def recommend_paths(state: CareerState):
    prompt = ChatPromptTemplate.from_template("""
    Based on this analysis: {analysis}
    Suggest 3 ideal career paths for this person.
    For each path, include:
    - Career Title
    - Why it fits them
    - Top 5 skills to learn
    - 3 free learning resources (like YouTube, Coursera, or Kaggle)
    Return in JSON format.
    """)
    chain = prompt | llm
    response = chain.invoke(state)
    state["recommendations"] = response.content
    return state

# Build the LangGraph
graph = StateGraph(CareerState)

# Add reasoning steps
graph.add_node("analyze_background", analyze_background)
graph.add_node("recommend_paths", recommend_paths)

# Define order of steps
graph.add_edge("analyze_background", "recommend_paths")
graph.add_edge("recommend_paths", END)

# Entry point
graph.set_entry_point("analyze_background")

# Compile final agent
career_agent = graph.compile()
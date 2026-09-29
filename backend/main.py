from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

import models
from database import engine
from routers import auth, resumes, jobs, advisor
from agents.advisor_agent import init_knowledge_base

models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Loaded once when the server starts (RAG requirement)
    try:
        init_knowledge_base()
    except Exception as e:
        print(f"Warning: failed to load the knowledge base ({e}). Make sure GEMINI_API_KEY is set.")
    yield


app = FastAPI(title="AI Resume Analyzer API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # fine for development; lock this down in production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(resumes.router, prefix="/resumes", tags=["Resumes"])
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
app.include_router(advisor.router, prefix="/advisor", tags=["Career Advisor"])

# Lets you open the frontend directly from the same server, with no CORS issues:
# http://127.0.0.1:8000/app/login.html
app.mount("/app", StaticFiles(directory="../frontend", html=True), name="frontend")


@app.get("/")
def root():
    return {"message": "AI Resume Analyzer API is running. Open /docs or /app/login.html"}

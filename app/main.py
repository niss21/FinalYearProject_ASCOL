# from fastapi import FastAPI, Depends, HTTPException, Query
# from sqlalchemy.orm import Session
# from typing import List, Optional
# import math

# from .database import get_db, engine
# from . import models, schemas
# from .recommender import recommend_treks

# # create tables if not exist
# models.Base = models.__class__ if False else None  # no-op to keep linter happy
# from .database import Base
# Base.metadata.create_all(bind=engine)

# app = FastAPI(title="Treks API")


# @app.get('/treks', response_model=List[schemas.Trek])
# def list_treks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     treks = db.query(models.Trek).offset(skip).limit(limit).all()
#     return treks

# @app.get("/treks/recommended")
# def get_recommended_treks(cost: float, duration: int, month: str, difficulty: str):
#     from app.recommender import recommend_treks
#     recommendations = recommend_treks(cost, duration, month, difficulty)
#     return recommendations


# @app.get('/treks/{trek_id}', response_model=schemas.Trek)
# def get_trek(trek_id: int, db: Session = Depends(get_db)):
#     trek = db.query(models.Trek).filter(models.Trek.id == trek_id).first()
#     if not trek:
#         raise HTTPException(status_code=404, detail='Trek not found')
#     return trek


from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from jinja2 import Environment, FileSystemLoader
import asyncio

from .database import get_db, engine, Base
from . import models, schemas
from .recommender import recommend_treks
from rag_pipeline import create_qa_chain  # ✅ import from your RAG project

# -----------------------------
# Initialize app and middleware
# -----------------------------
app = FastAPI(title="Treks + RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://wk4pq8nr-8000.asse.devtunnels.ms/"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# -----------------------------
# Setup DB
# -----------------------------
Base.metadata.create_all(bind=engine)

# -----------------------------
# Setup Jinja2 for HTML (RAG frontend)
# -----------------------------
env = Environment(loader=FileSystemLoader("templates"))

# -----------------------------
# Initialize RAG chain (only once)
# -----------------------------
qa_chain = create_qa_chain()

# =====================================================
# 🏔️ Trek-related Endpoints
# =====================================================

@app.get("/treks/recommended")
def get_recommended_treks(
    cost: float,
    duration: int,
    month: str,
    difficulty: str
):
    recommendations = recommend_treks(cost, duration, month, difficulty)
    return recommendations

@app.get("/treks/{part}", response_model=List[schemas.Trek])
def list_treks(
    part: int,
    db: Session = Depends(get_db)
):
    treks = db.query(models.Trek).all()
    total = len(treks)
    half = total // 2

    if part == 1:
        return treks[:half]
    elif part == 2:
        return treks
    else:
        raise HTTPException(status_code=400, detail="Invalid part number. Use /treks/1 or /treks/2")


@app.get("/trek/{trek_id}", response_model=schemas.Trek)
def get_trek(trek_id: int, db: Session = Depends(get_db)):
    trek = db.query(models.Trek).filter(models.Trek.id == trek_id).first()
    if not trek:
        raise HTTPException(status_code=404, detail="Trek not found")
    return trek

# =====================================================
# 🧠 RAG Chat Endpoints
# =====================================================

@app.get("/", response_class=HTMLResponse)
async def index():
    """Serves the RAG web interface (index.html)."""
    template = env.get_template("index.html")
    return template.render()


# Initialize your RAG chain once (outside endpoint)
qa_chain = create_qa_chain(debug=False)

@app.post("/chat")
async def chat(request: Request):
    """Handle user chat queries through RAG."""
    data = await request.json()
    question = data.get("question", "").strip()

    if not question:
        return JSONResponse({"error": "No question provided."}, status_code=400)

    # Run blocking LLM call in a background thread to avoid blocking FastAPI event loop
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, lambda: qa_chain.invoke({"query": question}))

    # Handle both possible return types (dict with "result" or raw string)
    if isinstance(result, dict):
        answer = result.get("result", "")
    else:
        answer = result

    # Optional: include retrieved docs if debugging is enabled
    response = {"answer": answer}
    if isinstance(result, dict) and "source_documents" in result:
        response["sources"] = [doc.page_content[:500] for doc in result["source_documents"]]

    return JSONResponse(response)

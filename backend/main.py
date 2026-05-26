from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from typing import List, Dict, Any
from contextlib import asynccontextmanager
from services.db_manager import db
from services.llm_engine import generate_guide_manual
import io

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load DB on startup
    db.load_data()
    yield
    # Clean up on shutdown

app = FastAPI(title="BA Scouta API", lifespan=lifespan)

# Allow CORS for local Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GuideRequest(BaseModel):
    opponent_ids: list[int]
    my_ids: list[int]

class DeckSlot(BaseModel):
    student: dict | None = None
    level: int
    star: int
    ue: int

class PredictManualRequest(BaseModel):
    my_deck: List[Dict[str, Any]]
    opp_deck: List[Dict[str, Any]]

@app.get("/")
def read_root():
    return {"status": "ok", "message": "BA Scouta API is running."}

@app.get("/api/students")
def get_students():
    # Return all students as a list
    return {"students": list(db.students.values())}





@app.post("/api/predict_manual")
async def predict_manual(req: PredictManualRequest):
    guide = generate_guide_manual(req.my_deck, req.opp_deck)
    return {"guide": guide}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

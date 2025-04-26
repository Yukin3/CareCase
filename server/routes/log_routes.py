from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any
from services.log_service import save_interaction_log

router = APIRouter()

class Turn(BaseModel):
    ai_line: str
    user_input: str
    timestamp: float
    emotion: Optional[str] = "neutral"

class InteractionLog(BaseModel):
    scenario_id: str
    role: str
    session_id: str
    start_time: float
    turns: List[Turn]

@router.post("/logs/upload")
def upload_interaction_log(log: InteractionLog):
    log_dict = log.dict()
    inserted_id = save_interaction_log(log_dict)
    if not inserted_id:
        raise HTTPException(status_code=500, detail="Failed to save interaction log.")
    return { "message": "Log saved", "id": inserted_id }

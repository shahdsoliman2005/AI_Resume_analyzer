from fastapi import APIRouter, Depends, HTTPException

import models
import schemas
from auth_utils import get_current_user
from agents.advisor_agent import career_advice

router = APIRouter()


@router.post("/ask", response_model=schemas.AdviceResponse)
def ask_advisor(
    request: schemas.AdviceRequest,
    current_user: models.User = Depends(get_current_user),
):
  
    try:
        answer = career_advice(request.question)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to get advice: {str(e)}")
    return {"answer": answer}

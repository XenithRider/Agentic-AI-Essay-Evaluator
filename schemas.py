from pydantic import BaseModel, Field
from typing import List

class EssayRequest(BaseModel):
    essay: str = Field(..., description="The text of the essay to evaluate")

class EvaluationResponse(BaseModel):
    language_feedback: str
    analysis_feedback: str
    clarity_feedback: str
    overall_feedback: str
    individual_scores: List[int]
    avg_score: float
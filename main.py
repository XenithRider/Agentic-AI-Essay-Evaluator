from fastapi import FastAPI, HTTPException
from schemas import EssayRequest, EvaluationResponse
from workflow import build_workflow

app = FastAPI(title="AI Essay Evaluator API")
workflow = build_workflow()

@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate(request: EssayRequest):
    try:
        initial_state = {"essay": request.essay, "individual_score": []}
        result = workflow.invoke(initial_state)
        
        return EvaluationResponse(
            language_feedback=result.get("language_feedback", ""),
            analysis_feedback=result.get("analysis_feedback", ""),
            clarity_feedback=result.get("clarity_feedback", ""),
            overall_feedback=result.get("overall_feedback", ""),
            individual_scores=result.get("individual_score", []),
            avg_score=result.get("avg_score", 0.0)
        )
    except Exception as e:
        # This will catch rate limits or general errors gracefully
        raise HTTPException(status_code=500, detail=str(e))
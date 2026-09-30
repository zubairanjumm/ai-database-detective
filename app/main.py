from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.database import Database
from app.graph import build_graph


app = FastAPI(
    title="AI Database Detective",
    description="Investigates business questions against a SQL database.",
    version="1.0.0",
)


class InvestigationRequest(BaseModel):
    question: str = Field(min_length=1)


class InvestigationResponse(BaseModel):
    question: str
    report: str


database = Database("sqlite:///samples/business.db")
graph = build_graph(database)


@app.get("/")
def root():
    return {
        "message": "AI Database Detective is running."
    }


@app.post(
    "/investigate",
    response_model=InvestigationResponse,
)
def investigate(request: InvestigationRequest):
    try:
        result = graph.invoke(
            {
                "question": request.question,
                "schema": {},
                "queries": [],
                "results": [],
                "findings": [],
                "current_step": 0,
                "max_steps": 2,
                "needs_more_evidence": False,
                "final_report": None,
            }
        )

        return InvestigationResponse(
            question=request.question,
            report=result["final_report"],
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Investigation failed.",
        ) from error
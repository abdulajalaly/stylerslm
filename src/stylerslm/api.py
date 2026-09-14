"""FastAPI application for outfit scoring."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .predict import predict_outfit

app = FastAPI(title="StylerSLM API", version="0.1.0")


class OutfitRequest(BaseModel):
    shirt: str
    pants: str
    shoes: str
    style: str
    shirt_subtype: str
    pants_subtype: str
    shoes_subtype: str
    fit: str = "regular"
    temperature: str = "mild"
    occasion: str = "business"
    outerwear: str = "none"


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "stylerslm"}


@app.post("/rate")
def rate_outfit(request: OutfitRequest):
    try:
        score = predict_outfit(**request.model_dump())
    except (FileNotFoundError, ValueError) as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    return {"score": round(score, 4), "percentage": f"{int(score * 100)}%"}
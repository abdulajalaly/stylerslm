import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from predict import predict_outfit
from ontology import SUBTYPES, COLORS, STYLES

app = FastAPI(title="StylerSLM API", version="2026.1")

# 1. Define the Data Model (Input Validation)
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

# 2. The Prediction Endpoint
@app.post("/rate")
def rate_outfit(req: OutfitRequest):
    """
    Returns a 0-100 score for a given outfit combination.
    """
    try:
        # Call your existing logic
        score = predict_outfit(
            req.shirt, req.pants, req.shoes, req.style,
            req.shirt_subtype, req.pants_subtype, req.shoes_subtype,
            req.fit, req.temperature, req.occasion, req.outerwear
        )
        
        # Return JSON response
        return {
            "score": round(score, 4),
            "percentage": f"{int(score * 100)}%",
            "verdict": "Fire fit! 🔥" if score > 0.85 else "Needs work 🧐"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. Health Check (Good for AWS/Cloud)
@app.get("/health")
def health_check():
    return {"status": "active", "model": "StylerSLM-2026"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

from .accessdata.dataaccess import DataAccessor

from fastapi import FastAPI
from typing import Optional


app = FastAPI()
data_accessor = DataAccessor()

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "This is the Outfox Health coding exercise."}


@app.get("/providers", tags=["health"])
async def get_providers(drg_desc: Optional[str], zipcode: str, radius: float) -> dict:
    """Get healthcare providers based on zip code and DRG code or description."""

    if not drg_desc:
        return {"error": "'drg_desc' must be provided."}

    if not zipcode:
        return {"error": "Zip code must be provided."}

    if drg_desc:
        results = data_accessor.get_closest_providers_for_drg_desc(drg_desc, zipcode, radius)

    return {"providers": [provider.to_dict() for provider in results]}


@app.post("/ask", tags=["health"])
async def ask_question(question: str) -> dict:
    """Endpoint to handle questions about healthcare providers."""

    if not question:
        return {"error": "Question must be provided."}

    results = data_accessor.execute_natural_language_query(question)
    return {"results": [result.to_dict() for result in results]}

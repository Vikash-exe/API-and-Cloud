from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Dict,  List, Literal, Annotated


class prediction_response(BaseModel):
    risk_category: str = Field(..., description="The predicted health risk category")
    confidence_score: float = Field(..., description="The confidence score for the predicted category")
    probabilities: Dict[str, float] = Field(..., description="The probabilities for each health risk category")
from typing import Any, List, Optional

from pydantic import BaseModel
from model.processing.validation import DataInputSchema

# Esquema de los resultados de predicción
class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    predictions: Optional[List[float]]

# Esquema para inputs múltiples
class MultipleDataInputs(BaseModel):
    inputs: List[DataInputSchema]

    class Config:
        schema_extra = {
            "example": {
                "inputs": [
                    {
                        "HighBP": 1,
                        "HighChol": 1,
                        "BMI": 28,
                        "HeartDiseaseorAttack": 0,
                        "GenHlth": 2,
                        "Age": 3,
                    }
                ]
            }
        }

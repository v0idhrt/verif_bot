from pydantic import BaseModel
from typing import Literal

class VerificationRequest(BaseModel):
    user_id: int
    verifier_id: int
    gender: Literal["male", "female"]
    timestamp: float

class VerificationResult(BaseModel):
    user_id: int
    success: bool
    reason: str

from pydantic import BaseModel
from typing import Optional

class TTSRequest(BaseModel):
    text: str
    voice_id: Optional[str] = None

    class Config:
        # Add validation for text length
        schema_extra = {
            "example": {
                "text": "Hello, this is a sample text to convert to speech.",
                "voice_id": "21m00Tcm4TlvDq8ikWAM"
            }
        }
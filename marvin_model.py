import openai
openai.api_base = "http://127.0.0.1:8080/v1"

from marvin import ai_model
from pydantic import BaseModel, Field


@ai_model
class Location(BaseModel):
    city: str
    state_abbreviation: str = Field(..., description="The two-letter state or province abbreviation")
    country: str


loc = Location("The birthplace of Maurice 'The Rocket' Richard.")

print(loc)
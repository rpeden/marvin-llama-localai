import openai
openai.api_base = "http://127.0.0.1:8080/v1"

from marvin import ai_fn
from pydantic import BaseModel, Field


class SuperHero(BaseModel):
    """
    A class representing a superhero.
    """
    name: str = Field(description="A hilarious superhero name.")
    abilities: list[str] = Field(description="A list 5 of the superhero's abilities.")
    backstory: str = Field(description="A funny paragraph telling the hero's origin story'.")


@ai_fn 
def generate_superhero(description: str) -> SuperHero:
    """
    Generate a superhero who fits the given description.
    """

hero = generate_superhero("A superhero who fights evil using nothing but rusty sporks.")

print(hero)

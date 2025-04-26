from pydantic import BaseModel
from typing import List, Optional

class Location(BaseModel):
    setting: str
    city: str
    country: str

class Scenario(BaseModel):
    id: str
    title: str
    description: str
    category: str
    time_of_day: str
    location: Location
    symptoms: List[str]
    environmental_context: str

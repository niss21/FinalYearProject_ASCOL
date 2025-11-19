from pydantic import BaseModel
from typing import Optional, List

class TrekBase(BaseModel):
    name: str
    images: Optional[str] = None
    region: Optional[str] = None
    duration_days: Optional[int] = None
    difficulty: Optional[str] = None
    permitRequired: Optional[bool] = False
    cost_usd: Optional[float] = None
    information: Optional[str] = None
    keyPoints: Optional[str] = None
    tourHighlights: Optional[str] = None
    bestTimeToTravel: Optional[str] = None
    detailedItinerary: Optional[str] = None

class TrekCreate(TrekBase):
    pass

class Trek(TrekBase):
    id: int
    class Config:
        orm_mode = True
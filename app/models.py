from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from .database import Base

class Trek(Base):
    __tablename__ = "treks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    images = Column(Text)  # store as pipe-separated URLs or filenames
    region = Column(String, index=True)
    duration_days = Column(Integer)
    difficulty = Column(String)
    permitRequired = Column(Boolean, default=False)
    cost_usd = Column(Float)
    information = Column(Text)
    keyPoints = Column(Text)
    tourHighlights = Column(Text)
    bestTimeToTravel = Column(String)  # store as comma-separated months or ranges
    detailedItinerary = Column(String)
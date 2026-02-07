from database import Base
from sqlalchemy import Column, Integer, String, Text, Float

average_score = Column(Float)
scores = Column(String(255))



class Debate(Base):
    __tablename__ = "debates"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    topic = Column(String(255), nullable=False)
    side = Column(String(50), nullable=False)
    argument = Column(Text, nullable=False)

    ai_counter = Column(Text)
    ai_feedback = Column(String(255))
    rating = Column(Integer)

    user_counter = Column(Text)
    ai_reply = Column(Text)
    ai_counter_rating = Column(Integer)

    scores = Column(String(255))
    average_score = Column(Float)
    # ss

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text

from src.db import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    in_stock = Column(Boolean, default=True, nullable=False)

from datetime import timezone, datetime
from sqlalchemy import Integer, String, Column, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc),
                        nullable=False)


class User(BaseModel):
    pass


class Link(BaseModel):
    pass

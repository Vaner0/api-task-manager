from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id           = Column(Integer, primary_key=True, index=True)
    nom          = Column(String, nullable=False)
    email        = Column(String, unique=True, index=True, nullable=False)
    mot_de_passe = Column(String, nullable=False)  # Toujours haché, jamais en clair !
    created_at   = Column(DateTime(timezone=True), server_default=func.now())

    tasks = relationship("Task", back_populates="owner", cascade="all, delete")
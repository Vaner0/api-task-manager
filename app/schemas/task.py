from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    titre: str
    description: Optional[str] = None
    statut: Optional[str] = "todo"       
    priorite: Optional[str] = "normale"  


class TaskUpdate(BaseModel):
    titre: Optional[str] = None
    description: Optional[str] = None
    statut: Optional[str] = None
    priorite: Optional[str] = None
    terminee: Optional[bool] = None


class TaskResponse(BaseModel):
    id: int
    titre: str
    description: Optional[str]
    statut: str
    priorite: str
    terminee: bool
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.auth import get_utilisateur_connecte
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.services import creer_tache, lister_taches, obtenir_tache, modifier_tache, supprimer_tache

router = APIRouter(prefix="/tasks", tags=["Tâches"])


@router.post("/", response_model=TaskResponse, status_code=201)
def creer(task_data: TaskCreate, db: Session = Depends(get_db), user=Depends(get_utilisateur_connecte)):
    return creer_tache(task_data, user.id, db)


@router.get("/", response_model=List[TaskResponse])
def lister(
    statut: Optional[str] = Query(None),
    priorite: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user=Depends(get_utilisateur_connecte)
):
    return lister_taches(user.id, db, statut, priorite)


@router.get("/{task_id}", response_model=TaskResponse)
def obtenir(task_id: int, db: Session = Depends(get_db), user=Depends(get_utilisateur_connecte)):
    return obtenir_tache(task_id, user.id, db)


@router.put("/{task_id}", response_model=TaskResponse)
def modifier(task_id: int, modifications: TaskUpdate, db: Session = Depends(get_db), user=Depends(get_utilisateur_connecte)):
    return modifier_tache(task_id, modifications, user.id, db)


@router.delete("/{task_id}", status_code=204)
def supprimer(task_id: int, db: Session = Depends(get_db), user=Depends(get_utilisateur_connecte)):
    return supprimer_tache(task_id, user.id, db)
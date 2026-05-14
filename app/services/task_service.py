"""
services/task_service.py
Contient toute la logique métier liée aux tâches.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional

from app.models import Task
from app.schemas import TaskCreate, TaskUpdate


def creer_tache(task_data: TaskCreate, user_id: int, db: Session) -> Task:

    nouvelle_tache = Task(
        titre=task_data.titre,
        description=task_data.description,
        statut=task_data.statut,
        priorite=task_data.priorite,
        user_id=user_id
    )

    db.add(nouvelle_tache)
    db.commit()
    db.refresh(nouvelle_tache)

    return nouvelle_tache


def lister_taches(
    user_id: int,
    db: Session,
    statut: Optional[str] = None,
    priorite: Optional[str] = None
) -> List[Task]:
    requete = db.query(Task).filter(Task.user_id == user_id)

    if statut:
        requete = requete.filter(Task.statut == statut)
    if priorite:
        requete = requete.filter(Task.priorite == priorite)

    return requete.all()


def obtenir_tache(task_id: int, user_id: int, db: Session) -> Task:

    tache = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()

    if not tache:
        raise HTTPException(status_code=404, detail="Tâche introuvable.")

    return tache


def modifier_tache(task_id: int, modifications: TaskUpdate, user_id: int, db: Session) -> Task:

    tache = obtenir_tache(task_id, user_id, db)

    for champ, valeur in modifications.model_dump(exclude_unset=True).items():
        setattr(tache, champ, valeur)

    db.commit()
    db.refresh(tache)

    return tache


def supprimer_tache(task_id: int, user_id: int, db: Session) -> None:

    tache = obtenir_tache(task_id, user_id, db)

    db.delete(tache)
    db.commit()
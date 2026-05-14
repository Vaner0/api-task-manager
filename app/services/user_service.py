from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import User
from app.schemas import UserCreate
from app.auth import hasher_mot_de_passe, verifier_mot_de_passe, creer_token


def creer_utilisateur(user_data: UserCreate, db: Session) -> User:

    existe = db.query(User).filter(User.email == user_data.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé.")

    nouvel_user = User(
        nom=user_data.nom,
        email=user_data.email,
        mot_de_passe=hasher_mot_de_passe(user_data.mot_de_passe)
    )

    db.add(nouvel_user)
    db.commit()
    db.refresh(nouvel_user)

    return nouvel_user


def connecter_utilisateur(email: str, mot_de_passe: str, db: Session) -> dict:

    utilisateur = db.query(User).filter(User.email == email).first()

    if not utilisateur or not verifier_mot_de_passe(mot_de_passe, utilisateur.mot_de_passe):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect.")

    token = creer_token(data={"sub": utilisateur.email})

    return {"access_token": token, "token_type": "bearer"}
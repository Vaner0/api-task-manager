import os
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.database import get_db
from app.models import User

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM  = os.getenv("ALGORITHM", "HS256")
EXPIRE_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))


def hasher_mot_de_passe(mot_de_passe: str) -> str:
    return pwd_context.hash(mot_de_passe)


def verifier_mot_de_passe(mot_de_passe_clair: str, mot_de_passe_hache: str) -> bool:
    return pwd_context.verify(mot_de_passe_clair, mot_de_passe_hache)


def creer_token(data: dict) -> str:
    donnees = data.copy()
    expiration = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MIN)
    donnees.update({"exp": expiration})
    return jwt.encode(donnees, SECRET_KEY, algorithm=ALGORITHM)


def get_utilisateur_connecte(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    erreur_401 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide ou expiré. Reconnecte-toi.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise erreur_401
    except JWTError:
        raise erreur_401

    utilisateur = db.query(User).filter(User.email == email).first()
    if utilisateur is None:
        raise erreur_401

    return utilisateur
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_utilisateur_connecte
from app.schemas import UserCreate, UserResponse, LoginRequest, TokenResponse
from app.services import creer_utilisateur, connecter_utilisateur

router = APIRouter(prefix="/users", tags=["Utilisateurs"])


@router.post("/inscription", response_model=UserResponse, status_code=201)
def inscription(user_data: UserCreate, db: Session = Depends(get_db)):
    return creer_utilisateur(user_data, db)


@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    return connecter_utilisateur(credentials.email, credentials.mot_de_passe, db)


@router.get("/moi", response_model=UserResponse)
def mon_profil(utilisateur_connecte=Depends(get_utilisateur_connecte)):
    return utilisateur_connecte
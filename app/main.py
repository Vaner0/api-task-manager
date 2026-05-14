from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import users_router, tasks_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="API de gestion de tâches",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(tasks_router)


@app.get("/", tags=["Accueil"])
def accueil():
    return {
        "message": "Bienvenue sur l'API Task Manager !",
        "documentation": "/docs"
    }
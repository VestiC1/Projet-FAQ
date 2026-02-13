from fastapi import FastAPI
from .routes import router
import json
from fastapi.middleware.cors import CORSMiddleware
from config import FRONTEND_HOST

app = FastAPI(
    title="Assistant FAQ Intelligent pour Collectivité Territoriale",
    description="API d'assistance FAQ intégrant un RAG pour obtenir une réponse rigoureuse.",
    version="1.0.0"
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://{FRONTEND_HOST}", f"https://{FRONTEND_HOST}"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
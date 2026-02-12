from fastapi import FastAPI
from .routes import router
import json
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Assistant FAQ Intelligent pour Collectivité Territoriale",
    description="AConcevoir, développer et déployer une API d'assistance FAQ intégrant un LLM, en suivant une démarche rigoureuse de benchmark pour sélectionner la meilleure approche technique.",
    version="1.0.0"
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
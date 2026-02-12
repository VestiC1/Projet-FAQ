from fastapi import FastAPI
from .routes import router
import json


app = FastAPI(
    title="Assistant FAQ Intelligent pour Collectivité Territoriale",
    description="AConcevoir, développer et déployer une API d'assistance FAQ intégrant un LLM, en suivant une démarche rigoureuse de benchmark pour sélectionner la meilleure approche technique.",
    version="1.0.0"
)

app.include_router(router)

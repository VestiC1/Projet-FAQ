from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from src.api.services import get_faq, get_document
from .dependencies import get_supabase, get_rag
from supabase import Client
from pydantic import BaseModel

class Query(BaseModel):
    question: str


router = APIRouter()

@router.get("/", tags=["Home"], response_class=JSONResponse)
async def home(request: Request):
    """
    Point d'entrée principal
    
    Retourne un message de bienvenue pour l'API.
    """
    return JSONResponse(content={"message":"home"})

@router.get("/healthcheck", tags=["Health"], response_class=JSONResponse)
async def health(request: Request):
    """
    Vérification de l'état de santé
    
    Retourne l'état de santé de l'API.
    """
    return JSONResponse(content={"status":"OK"})

@router.post("/answer", tags=["RAG"], response_class=JSONResponse)
async def answer(request: Request, query:Query, rag=Depends(get_rag)):
    """
    Obtenir une réponse à une question
    
    Utilise le système RAG (Retrieval-Augmented Generation) pour générer une réponse
    à la question posée.
    
    Args:
        query: Objet contenant la question à poser
        
    Returns:
        Réponse générée par le système RAG
    """
    answer = rag.answer(question=query.question, stream=False)
    return JSONResponse(content={"answer":answer})

@router.post("/answer/stream", tags=["RAG"], response_class=StreamingResponse)
async def answer_stream(request: Request, query: Query, rag=Depends(get_rag)):
    """
    Obtenir une réponse en streaming
    
    Utilise le système RAG pour générer une réponse en streaming à la question posée.
    
    Args:
        query: Objet contenant la question à poser
        
    Returns:
        Stream de la réponse générée par le système RAG
    """
    return StreamingResponse(
        rag.answer(question=query.question, stream=True),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )

@router.get("/FAQ", tags=["FAQ"], response_class=JSONResponse)
async def faq(request: Request, sb: Client= Depends(get_supabase)):
    """
    Obtenir la liste des FAQ
    
    Récupère la liste complète des questions fréquemment posées depuis la base de données.
    
    Returns:
        Liste des FAQ au format JSON
    """
    return JSONResponse(content={"faq": get_faq(sb=sb)})

@router.get("/documents/{id}", tags=["Documents"], response_class=JSONResponse)
async def docs(request: Request, id, sb: Client= Depends(get_supabase)):
    """
    Obtenir un document spécifique
    
    Récupère un document spécifique à partir de son identifiant.
    
    Args:
        id: Identifiant du document à récupérer
        
    Returns:
        Document au format JSON
    """
    return JSONResponse(content={
        "document": get_document(sb=sb, id=id)
    })
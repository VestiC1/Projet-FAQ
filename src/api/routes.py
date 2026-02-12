from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from src.api.services import get_faq, get_document
from .dependencies import get_supabase, get_rag
from supabase import Client
from pydantic import BaseModel

class Query(BaseModel):
    question: str


router = APIRouter()

@router.get("/", tags=["Home"], response_class=JSONResponse)
async def home(request: Request):
    return JSONResponse(content={"message":"home"})

@router.get("/healthcheck", tags=["Health"], response_class=JSONResponse)
async def health(request: Request):
    return JSONResponse(content={"status":"OK"})

@router.post("/answer", tags=[""], response_class=JSONResponse)
async def answer(request: Request, query:Query, rag=Depends(get_rag)):
    answer = rag.answer(question=query.question, stream=False)
    return JSONResponse(content={"answer":answer})

@router.get("/FAQ", tags=[""], response_class=JSONResponse)
async def faq(request: Request, sb: Client= Depends(get_supabase)):
    return JSONResponse(content={"faq": get_faq(sb=sb)})

@router.get("/documents/{id}", tags=[""], response_class=JSONResponse)
async def docs(request: Request, id, sb: Client= Depends(get_supabase)):
    return JSONResponse(content={
        "document": get_document(sb=sb, id=id)
    })
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from src.app.db.load import load_faq, get_document
from src.app.models import RAG
from config import FAQ_PATH
from config import embd_model_name, RAG_K, system_prompt_template, LLMNAME, HF_TOKEN, FAQ_VEC

from pydantic import BaseModel

class Query(BaseModel):
    question: str

faq_json=load_faq(faq_path=FAQ_PATH)

rag = RAG(
        hf_token=HF_TOKEN,
        model_name=LLMNAME,
        system_prompt=system_prompt_template['B'],
        max_tokens=200,
        corpus=FAQ_VEC,
        vec_name=embd_model_name,
        top_k=RAG_K
    )

router = APIRouter()

@router.get("/", tags=["Home"], response_class=JSONResponse)
async def home(request: Request):
    return JSONResponse(content={"message":"home"})

@router.get("/healthcheck", tags=["Health"], response_class=JSONResponse)
async def health(request: Request):
    return JSONResponse(content={"status":"OK"})

@router.post("/answer", tags=[""], response_class=JSONResponse)
async def answer(request: Request, query:Query):
    answer, _ = rag.answer(question=query.question)
    return JSONResponse(content={"answer":answer})

@router.get("/FAQ", tags=[""], response_class=JSONResponse)
async def faq(request: Request):
    return JSONResponse(content={"faq":faq_json["faq"]})

@router.get("/documents/{id}", tags=[""], response_class=JSONResponse)
async def docs(request: Request, id):
    return JSONResponse(content={
        "document": get_document(faq_json=faq_json, id=id)
    })
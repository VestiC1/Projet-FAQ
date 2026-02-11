from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from src.app.db.load import load_faq, get_document
from config import FAQ_PATH


faq_json=load_faq(faq_path=FAQ_PATH)

router = APIRouter()

@router.get("/", tags=["Home"], response_class=JSONResponse)
async def home(request: Request):
    return JSONResponse(content={"message":"home"})

@router.get("/healthcheck", tags=["Health"], response_class=JSONResponse)
async def health(request: Request):
    return JSONResponse(content={"status":"OK"})

@router.get("/answer", tags=[""], response_class=JSONResponse)
async def answer(request: Request):
    return JSONResponse(content={"status":"OK"})

@router.get("/FAQ", tags=[""], response_class=JSONResponse)
async def faq(request: Request):
    return JSONResponse(content={"faq":faq_json["faq"]})

@router.get("/documents/{id}", tags=[""], response_class=JSONResponse)
async def docs(request: Request, id):
    return JSONResponse(content={
        "document": get_document(faq_json=faq_json, id=id)
    })
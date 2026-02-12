from supabase import create_client, Client
from config import supabase_rest, SUPABASE_TOKEN
from config import RAG_K, system_prompt_template, HF_TOKEN, MODAL_ENDPOINT, LLMNAME

from src.api.models.strategy import RAG

def get_supabase() -> Client:
    
    return create_client(
        supabase_rest,
        SUPABASE_TOKEN,
    )

def get_rag() :
    return RAG(
        hf_token=HF_TOKEN,
        model_name=LLMNAME,
        system_prompt=system_prompt_template['B'],
        max_tokens=200,
        endpoint=MODAL_ENDPOINT,
        top_k=RAG_K
    )
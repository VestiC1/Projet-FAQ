import json
from pathlib import Path
from config import GOLDEN_PATH, FAQ_PATH

def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_faq():
    return load_json(FAQ_PATH)

def load_golden():
    return load_json(GOLDEN_PATH)

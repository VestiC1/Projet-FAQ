import json
from pathlib import Path
from pprint import pprint

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"

faq    = DATA / "faq-base-6964b97cf0c25947575840.json"
golden = DATA / "golden-set-6964b9874cff1935078155.json"

def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_faq():
    return load_json(faq)

def load_golden():
    return load_json(golden)

def main():
    faq_data = load_faq()
    golden_data = load_golden()

if __name__ == "__main__":
    main()
from dotenv import load_dotenv
from pathlib import Path

# Project root directory
ROOT = Path(__file__).parent

# Secrets loading
load_dotenv( dotenv_path=ROOT / ".env", override=True )

# Data directory
DATA_DIR = ROOT / "data"

# Data file paths
FAQ_PATH    = DATA_DIR / "faq-base-6964b97cf0c25947575840.json"
GOLDEN_PATH = DATA_DIR / "golden-set-6964b9874cff1935078155.json"
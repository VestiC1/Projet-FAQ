import sys
from pathlib import Path
import uvicorn
from config import API_CONFIG

# Ajouter le répertoire racine au path
#ROOT_DIR = Path(__file__).parent.parent
#sys.path.insert(0, str(ROOT_DIR))

if __name__ == "__main__":

    
    print("Lancement de Projet FAQ")
    print(f"URL: http://{API_CONFIG['host']}:{API_CONFIG['port']}")
    print(f"Docs: http://{API_CONFIG['host']}:{API_CONFIG['port']}/docs")
    
    uvicorn.run(
        "src.api.main:app",
        host=API_CONFIG["host"],
        port=API_CONFIG["port"],
        reload=True # en dev
    )
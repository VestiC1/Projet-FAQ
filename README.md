# Assistant FAQ Intelligent

Cet assistant IA a été conçu pour la **Communauté de Communes Val de Loire Numérique** afin d'automatiser les réponses aux questions des citoyens concernant les démarches administratives (état civil, urbanisme, transports, etc.).

Liens : 
* [front](https://projet-faq.vercel.app/)
* [api](https://api-projet-faq.vercel.app/docs)

---

## 🚀 Fonctionnement de l'Application

L'application repose sur une architecture **RAG (Retrieval-Augmented Generation)**, sélectionnée après un benchmark rigoureux de trois stratégies.

### Flux de traitement :
1. **Requête Utilisateur** : Le citoyen pose une question via l'interface Next.js.
2. **Recherche Sémantique (Retrieval)** : L'API convertit la question en vecteur (embedding) via le modèle `multilingual-e5-small` et interroge une base de données Postgres (Supabase) équipée de l'extension `pgvector` pour trouver les documents FAQ les plus pertinents.
3. **Génération Contextuelle** : Les documents trouvés sont injectés dans un prompt système. Le LLM `Mistral-7B-Instruct-v0.2` génère ensuite une réponse précise, basée uniquement sur ce contexte pour éviter les hallucinations.
4. **Streaming** : La réponse est renvoyée en temps réel à l'utilisateur via un flux de données (streaming) pour une meilleure expérience utilisateur.

![Architecture de l'Assistant FAQ Intelligent : Le Flux RAG](docs/infographieREADME.png)


---

## 🏗️ Architecture Technique

Le projet utilise une approche **Serverless "Scale-to-Zero"**, garantissant un coût nul au repos et une montée en charge automatique.

- **Frontend** : Next.js hébergé sur Vercel.
- **Backend** : API FastAPI hébergée sur Vercel.
- **Infrastructure IA** :
  - Modal : Pour le service de recherche et de vectorisation serverless.
  - Hugging Face Inference API : Pour l'exécution du modèle Mistral 7B.
- **Base de données** : Supabase (Postgres).

---

## 🛠️ Stack Technologique

- **Langage** : Python 3.12+.
- **Gestionnaire de paquets** : `uv`.
- **Modèles** :
  - LLM : `Mistral-7B-Instruct-v0.2`.
  - Embeddings : `intfloat/multilingual-e5-small`.
- **Tests** : `Pytest` pour les tests unitaires et d'intégration.
- **CI/CD** : GitHub Actions pour le déploiement automatique sur Vercel et Modal.

---

## 📦 Installation et Utilisation

### Prérequis
- Python 3.12 et l'outil `uv`.
- Des comptes Hugging Face, Vercel, Modal et Supabase.

### Quick Start

```bash
# 1. Clonage du repo
git clone https://github.com/VestiC1/Projet-FAQ.git

# 2. Configuration : Créer un fichier .env (cf .env.template)
cp .env.template .env
# Remplir les variables d'environnement

# 3. Initialisation
uv sync --all-extras

# 4. Lancement API
make app

# 5. Lancement Front
cd src/frontend
npm run dev
```
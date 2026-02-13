# Projet FAQ Intelligent

Assistant IA pour la Communauté de Communes Val de Loire Numérique, permettant de répondre automatiquement aux questions des citoyens sur les démarches administratives.

![Comparatif des Stratégies](../Infographie-Projet-FAQ.png)

## À propos

Ce projet compare trois stratégies de Question-Answering pour déterminer la meilleure approche technique :

- **Stratégie A** : LLM seul avec prompt engineering (simplicité maximale)
- **Stratégie B** : Recherche sémantique (RAG) + LLM génératif (réduction des hallucinations)
- **Stratégie C** : Recherche sémantique + Q&A extractif (réponses brutes extraites)

### Critères d'évaluation

| Critère | Description | Poids |
|---------|-------------|-------|
| **Exactitude** | % de réponses correctes sur le golden set | 30% |
| **Pertinence** | Score 0-2 sur la qualité de la réponse | 20% |
| **Hallucinations** | % de réponses contenant des informations inventées | 20% |
| **Latence** | Temps de réponse moyen (secondes) | 15% |
| **Complexité** | Difficulté de maintenance et évolution | 15% |

## Installation

### Prérequis

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) pour la gestion des dépendances

### Configuration

1. **Cloner le repository** :
```bash
git clone https://github.com/VestiC1/Projet-FAQ.git
cd Projet-FAQ
```

2. **Installer les dépendances avec uv** :
```bash
uv sync
```

3. **Créer un fichier `.env` à la racine** :
```bash
HF_TOKEN=votre_token_huggingface
```

4. **Générer les embeddings FAQ** :
```bash
python -m scripts.compute_embeding
```

## Utilisation

### Tester les stratégies

Testez les trois stratégies sur une question exemple :

```bash
python -m scripts.test_strategies
```

### Lancer le benchmark complet

Évalue toutes les stratégies sur le golden set (30 questions) :

```bash
python -m scripts.benchmark
```

⚠️ **Note** : Le benchmark prend environ 5-10 minutes avec des pauses entre requêtes pour respecter les rate limits de l'API HuggingFace.

### Analyser les résultats

Lance l'interface d'analyse interactive avec Marimo :

```bash
marimo edit notebooks/benchmark_analysis.py
```

Ou pour l'annotation manuelle :

```bash
marimo edit notebooks/annotations.py
```

## Structure du projet

```
vestic1-projet-faq/
├── data/                      # Données FAQ et résultats
│   ├── faq-base-*.json       # Base de connaissances (60-80 Q&A)
│   ├── golden-set-*.json     # Jeu de test (30 questions)
│   ├── faq_embeddings.parquet # Vecteurs pré-calculés
│   ├── benchmark_results.parquet # Résultats du benchmark
│   └── annotation_*.csv      # Annotations manuelles
├── docs/                      # Documentation projet
│   ├── 1-BRIEF_PROJET.md     # Cahier des charges
│   ├── 3-NOTE_CADRAGE.md     # Note de cadrage technique
│   └── Rapport_veille.md     # Veille technologique
├── notebooks/                 # Notebooks d'analyse (Marimo)
│   ├── benchmark_analysis.py # Visualisation des résultats
│   └── annotations.py        # Interface d'annotation
├── scripts/                   # Scripts d'exécution
│   ├── benchmark.py          # Lance le benchmark complet
│   ├── compute_embeding.py   # Génère les embeddings
│   └── test_strategies.py    # Teste les stratégies
└── src/
    ├── models/               # Modèles IA
    │   ├── llm.py           # LLM Chat Completion
    │   ├── rag.py           # TinyRag (recherche sémantique)
    │   └── qna.py           # Q&A Extractif
    └── strategies/           # Implémentation des 3 stratégies
        ├── strategya.py      # Stratégie A (LLM seul)
        ├── strategyb.py      # Stratégie B (RAG)
        └── strategyc.py      # Stratégie C (Q&A extractif)
```

## Technologies

### Stack Technique

- **Langage** : Python 3.10+
- **Gestion de dépendances** : uv
- **LLM** : Mistral-7B-Instruct-v0.2 (via HuggingFace Inference API)
- **Embeddings** : Sentence Transformers (all-MiniLM-L6-v2)
- **Q&A Extractif** : mdeberta-v3-base-squad2
- **Notebooks** : Marimo
- **Data** : Pandas, PyArrow

### Pourquoi ces choix ?

- **Open Source** : Tous les composants sont open source pour un hébergement en interne
- **Performance** : Mistral-7B offre un excellent rapport qualité/latence
- **Légèreté** : Embeddings compacts (384 dimensions) adaptés au périmètre restreint
- **Gratuit** : Utilisation de l'API gratuite HuggingFace Inference

## Commandes Make disponibles

```bash
# Charger les données
make loaddata

# Générer les embeddings
make embeddings

# Tester les stratégies
make strats

# Lancer le benchmark complet
make benchmmark_strats
```

## Résultats

Les résultats du benchmark sont sauvegardés dans `data/benchmark_results.parquet` et incluent :

- Réponses générées par chaque stratégie
- Temps d'inférence pour chaque question
- Références FAQ attendues
- Mots-clés de validation

### Métriques mesurées

- **Exactitude** : % de réponses correctes (évaluation manuelle)
- **Pertinence** : Score 0-2 sur la qualité de la réponse
- **Hallucinations** : % de réponses contenant des informations inventées
- **Latence** : Temps de réponse moyen (P50, P75, P95)
- **Complexité** : Facilité de maintenance et évolution

## Cas d'usage

Le système répond aux questions sur :

- État civil (actes de naissance, mariage, etc.)
- Urbanisme (permis de construire, etc.)
- Déchets et environnement
- Transports
- Petite enfance
- Social et solidarité
- Vie associative
- Élections
- Logement
- Culture et sport
- Fiscalité
- Eau et assainissement

## Limitations connues

- **Rate Limits** : L'API HuggingFace gratuite impose des limites (pauses nécessaires)
- **Périmètre** : Le système refuse les questions hors périmètre
- **Langue** : Optimisé pour le français uniquement
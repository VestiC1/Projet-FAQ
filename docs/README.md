# Documentation du Benchmark et Évaluation des Stratégies

Ce répertoire contient l'ensemble des protocoles, des données de test et des outils d'analyse ayant permis de comparer et de sélectionner la meilleure architecture technique pour l'assistant FAQ de la **Communauté de Communes Val de Loire Numérique**.

![Description strategie evaluation](InfographieBENCHMARK.png)
---

## 📊 Objectif de l'Évaluation

L'objectif est de comparer objectivement trois approches de **Question-Answering** pour automatiser les réponses administratives, tout en garantissant la fiabilité des informations fournies aux citoyens.

---

## 🔍 Stratégies Comparées

- **Stratégie A (LLM Seul)** : Utilisation directe de Mistral 7B v0.2 Instruct avec un prompt système.
- **Stratégie B (RAG - Recherche + Génération)** : Recherche sémantique dans la base FAQ suivie d'une génération contextuelle par le LLM. **Solution retenue**.
- **Stratégie C (Q&A Extractif)** : Recherche sémantique couplée à un modèle extractif (CamemBERT) qui isole la réponse exacte dans le texte.

---

## 📏 Métriques et Pondération

Chaque stratégie a été évaluée selon cinq critères critiques, agrégés dans un score global pondéré :

| Critère          | Description                                                                 | Poids |
|------------------|-----------------------------------------------------------------------------|-------|
| Exactitude       | Pourcentage de réponses correctes par rapport aux faits réels.              | 30%   |
| Pertinence       | Qualité et adéquation de la réponse à la question posée.                   | 20%   |
| Fidélité         | Absence d'informations inventées ou erronées (non-hallucination).           | 20%   |
| Latence          | Temps de réponse moyen (cible < 2 secondes).                                | 15%   |
| Complexité       | Facilité de maintenance et évolutivité de la solution.                      | 15%   |

---

## 🧪 Protocole d'Évaluation

1. **Golden Set** : Un jeu de test de 30 questions représentatives des thématiques citoyennes (état civil, urbanisme, etc.) a été constitué.
2. **Évaluation Automatisée** : Utilisation du framework **RAGAS** (LLM-as-a-judge) pour mesurer la fidélité et la pertinence de manière industrielle.

---

## 📈 Résultats et Analyse

Les analyses montrent que la **Stratégie B (RAG)** offre le meilleur équilibre :
- **Exactitude excellente** : Utilise la base FAQ comme source unique de vérité.
- **Hallucinations quasi nulles** : Le LLM est contraint par le contexte fourni.
- **Performance globale** : Elle obtient le score pondéré le plus élevé lors des tests comparatifs.

À l'inverse :
- La **Stratégie A** est écartée en raison de son taux élevé d'hallucinations.
- La **Stratégie C** est rejetée pour son manque de fluidité conversationnelle.

---

## 🛠️ Outils d'Analyse

Pour reproduire ou visualiser ces résultats, plusieurs notebooks **Marimo** sont disponibles :
- [`notebooks/automated_benchmark.py`](./notebooks/automated_benchmark.py) : Génération des graphiques radar et comparaison des métriques RAGAS.

> **Note** : Les résultats détaillés sont stockés au format Parquet.

# Rapport Veille

## Ressources consultées

### 1/ FastAPI

#### 1. Documentation officielle FastAPI
Lien : 
https://fastapi.tiangolo.com
​

Ce site décrit FastAPI comme un framework high-performance, basé sur Starlette (async) et Pydantic pour la définition de schémas et la validation des données, ce qui répond à la fois au besoin de performance et de schéma de validation.
​

La doc explique aussi que FastAPI est conçu pour être « ready for production » et met en avant des usages en production par différentes entreprises, ce qui répond au critère de qualité industrielle.
​

#### 2. Article technique sur performance et production
Lien : 
https://www.blueshoe.io/blog/fastapi-in-production/
Auteur :
Korbinian Habereder
​

L’article détaille la mise en production de FastAPI (reverse proxy, sécurité, scalabilité), montrant que le framework est adapté à des environnements de production exigeants.
​

Il insiste sur la performance, l’architecture moderne (async, uvicorn, etc.) et les bonnes pratiques d’exploitation, ce qui renforce les points « framework léger et performant » et « production ready ».
​

#### 3. Monitoring Prometheus + intégration DB (SQLModel/ORM)
Lien Prometheus / monitoring : Tutoriel « Monitor Python FastAPI in Real-Time with Prometheus & Grafana » (Prometheus + prometheus-fastapi-instrumentator) : 
https://www.youtube.com/watch?v=tskCWURmPDo
​

Ce tutoriel montre comment exposer des métriques depuis FastAPI, configurer Prometheus pour les scraper et construire des dashboards Grafana, ce qui illustre un monitoring applicatif simple avec connecteur Prometheus.
​

Lien ORM / interface DB : « Connecting FastAPI to a Database with SQLModel » : 
https://davidmuraya.com/blog/connecting-fastapi-to-database-with-sqlmodel/
​

Ce guide explique comment utiliser SQLModel (ORM basé sur SQLAlchemy et Pydantic) avec FastAPI pour définir des modèles, sessions et CRUD, montrant que l’intégration base de données via un ORM est simple et idiomatique.
​

### 2/ API type Huggingface

#### 1. API universelle & changement de provider/modèle sans changer le code
Lien : 
https://github.com/huggingface/hub-docs/blob/main/docs/inference-providers/index.md
​

Inference Providers fournit une API unique qui agit comme un proxy vers plusieurs providers, avec « Unified Authentication & Billing » et une interface cohérente via les client libraries (même format de requête pour différents providers).
​

Le paramètre provider="auto" permet une sélection automatique de provider sans changer le code métier, ce qui permet de changer de provider ou de modèle en ne modifiant que la configuration.
​

API « universelle » d’agrégation de providers.
​

Capacité à changer de choix de modèle/provider sans toucher au code de base (changement de provider/model ID côté config).
​

#### 2. Coûts d’infra faibles, scalabilité et prévisibilité budgétaire
Lien : 
https://huggingface.co/docs/inference-endpoints/en/pricing
​

Les Inference Endpoints proposent des instances dédiées avec autoscaling configurable (min/max de réplicas) ce qui permet de scaler facilement pour des trafics modérés tout en gardant une architecture simple.
​

Les coûts sont clairs et publiés (tarif horaire par type d’instance, calcul explicite du coût mensuel), ce qui permet d’avoir une bonne prévisibilité budgétaire pour la consommation d’infrastructure.
​

Coût d’infrastructure bas pour des besoins modérés (choix de petites instances CPU / petites GPU).
​

Scalabilité simple via autoscaling des endpoints géré par Hugging Face, plutôt que monter sa propre infra.
​

#### 3. DPA & conformité RGPD (templates)
Lien : 
https://cdn-media.huggingface.co/landing/assets/Data+Processing+Agreement.pdf
​

Hugging Face fournit un Data Processing Agreement (DPA) standard que le client peut intégrer à son contrat, avec les rôles « Controller »/« Processor » clairement définis.
​

Le DPA inclut les clauses contractuelles types UE (EU SCCs) et précise que Hugging Face peut fournir une copie signée sur demande, ce qui facilite la documentation de conformité RGPD.
​

Existence d’un DPA fourni par Hugging Face, donc obtention de DPA facilitée.
​

Support de la conformité RGPD via SCCs et documentation standardisée, réutilisable comme template dans le dossier de conformité.
​

### 3/ Coût de l'open source

#### 1. Leaderboard LLM open source francophones
Leaderboard généraliste avec un focus sur Llama 3, Mistral et autres modèles open source, incluant des infos de coût et de cas d’usage, mis à jour régulièrement :
https://www.ia-insights.fr/classement-des-meilleurs-llm/

​
Utile pour situer par exemple Mistral (Mixtral, Mistral 7B, etc.) et Llama 3 comme meilleurs candidats multilingues dont le français, avec un angle coût/usage intensif.
​

#### 2. Benchmarks d’inférence locale (CPU / GPU)
Article de benchmark de Mistral 7B en local sur différentes cartes GPU, avec mesures de throughput (tokens/s) et temps d’exécution, plus réflexion coût/perf :
https://blog.budecosystem.com/case-study/benchmarking-mistral-7b-inference-performance-on-gpus/

​
Donne des chiffres concrets de latence et de débit pour un modèle Mistral 7B avec plusieurs runtimes (vLLM, TGI, etc.), ce qui est exploitable pour comparer un déploiement local vs hébergé.
​

#### 3. Latence API vs local (inclut métriques de TTFT)
Analyse détaillée « on-prem LLMs vs cloud APIs » avec une section dédiée à la latence (time-to-first-token, tokens/s), y compris impact du réseau et de la mise à l’échelle :
https://www.unifiedaihub.com/blog/on-premise-llms-vs-cloud-apis-when-to-run-your-ai-models-on-premise

​
Explique pourquoi les APIs cloud ajoutent systématiquement une latence réseau et donne des ordres de grandeur de débit possibles pour des LLM open source bien optimisés on-prem (50–100 tokens/s selon le matériel).
​

Si tu veux, le prochain pas peut être de construire à partir de ces trois sources un petit tableau comparatif coût/latence local vs API pour 1–2 modèles (par ex. Mistral 7B et un modèle plus petit).
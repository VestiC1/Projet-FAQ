loaddata:
	python -m scripts.data_loader

embeddings:
	python -m scripts.compute_embeding

mistral:
	python -m scripts.mistral_ex

providers:
	python -m scripts.providers_mistral

rag:
	python -m src.rag

strata:
	python -m src.strategies.strategya

stratb:
	python -m src.strategies.strategyb

stratc:
	python -m src.strategies.strategyc

benchmmark_strats:
	python -m scripts.benchmark
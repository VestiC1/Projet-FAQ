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
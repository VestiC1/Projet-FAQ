loaddata:
	python -m scripts.data_loader

embeddings:
	python -m scripts.compute_embeding

mistral:
	python -m scripts.hf_utils.mistral_ex

providers:
	python -m scripts.hf_utils.providers_mistral

strats:
	python -m scripts.test_strategies

benchmmark_strats:
	python -m scripts.benchmark

token:
	python -m scripts.test_system_prompt

evaluate:
	python -m scripts.evaluate

app:
	python -m scripts.run_api

deploy:
	modal deploy -m src.infra.app

requirements.txt:
	uv export --only-group api --no-hashes --no-annotate -o requirements.txt
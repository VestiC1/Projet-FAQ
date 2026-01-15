from huggingface_hub import model_info

# Récupère les informations sur le modèle
info = model_info("mistralai/Mistral-7B-Instruct-v0.2", expand="inferenceProviderMapping")

# Affiche les informations sur les fournisseurs d'inférence
print(info.inference_provider_mapping)

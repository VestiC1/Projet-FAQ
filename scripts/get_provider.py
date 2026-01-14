from huggingface_hub import model_info

model_name = "mistralai/Mistral-7B-Instruct-v0.3"

info = model_info(model_name, expand="inferenceProviderMapping")
print(info.inference_provider_mapping)

info = model_info(model_name, expand="inference")
print(info.inference)
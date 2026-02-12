from abc import ABC, abstractmethod

class Model(ABC):
    
    def __init__(self, model_name: str, *args, **kwargs):
        self.model_name = model_name

    @abstractmethod
    def predict(self, *args, **kwargs) -> str:
        raise NotImplementedError("Subclasses must implement this method.")
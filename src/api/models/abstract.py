import time
from abc import ABC, abstractmethod

class Strategy(ABC):
    
    def __init__(self, strategy_name: str, *args, **kwargs):
        self.strategy_name = strategy_name
        self.last_ellapsed_time = None
    
    def answer(self, question: str, *args, **kwargs) -> str:
        start = time.perf_counter()
        result = self._answer(question, *args, **kwargs)
        self.last_ellapsed_time = time.perf_counter() - start
        return result

    @abstractmethod
    def _answer(self, question: str, *args, **kwargs) -> str:
        raise NotImplementedError("Subclasses must implement this method.")
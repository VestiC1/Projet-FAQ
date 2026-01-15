class StrategyAbstract:
    
    def __init__(self, *args, **kwargs):
        pass

    def answer(self, question: str) -> str:
        raise NotImplementedError("Subclasses must implement this method.")
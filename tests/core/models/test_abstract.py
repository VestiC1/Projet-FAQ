import pytest
from src.core.models.abstract import Model


def test_model_abstract_instantiation():
    """Test that Model abstract class cannot be instantiated directly."""
    with pytest.raises(TypeError):
        model = Model(model_name="test_model")


def test_model_abstract_predict_method():
    """Test that predict method must be implemented by subclasses."""
    class ConcreteModel(Model):
        def __init__(self):
            super().__init__(model_name="concrete")
        
        def predict(self, *args, **kwargs) -> str:
            return "implemented"
    
    concrete_model = ConcreteModel()
    
    # This should not raise NotImplementedError since we implemented the method
    result = concrete_model.predict()
    assert result == "implemented"
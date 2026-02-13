import pytest
from unittest.mock import patch, MagicMock
from src.core.strategies.strategya import StrategyA


def test_strategy_a_initialization():
    """Test StrategyA initialization."""
    with patch('src.core.models.llm.InferenceClient') as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        
        strategy = StrategyA(
            hf_token="test_token",
            model_name="test_model",
            system_prompt="test_prompt",
            max_tokens=100
        )
        
        assert strategy.strategy_name == "Strategy_A"
        assert strategy.llm.model_name == "test_model"
        assert strategy.llm.client == mock_instance
        mock_client.assert_called_once_with(model="test_model", token="test_token")


def test_strategy_a_answer():
    """Test StrategyA answer method."""
    with patch('src.core.models.llm.InferenceClient') as mock_client:
        mock_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = {'content': 'test answer'}
        mock_instance.chat_completion.return_value = mock_response
        mock_client.return_value = mock_instance
        
        strategy = StrategyA(
            hf_token="test_token",
            model_name="test_model",
            system_prompt="test_prompt",
            max_tokens=100
        )
        
        question = "What is the capital of France?"
        result = strategy._answer(question)
        
        # The predict method returns a tuple (answer, context)
        assert result == ("test answer", "test_prompt")
        mock_instance.chat_completion.assert_called_once()
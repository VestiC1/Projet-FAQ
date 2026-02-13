import pytest
from unittest.mock import patch, MagicMock
from src.api.models.steps.generation import LLMChatCompletion


def test_llm_chat_completion_initialization():
    """Test LLMChatCompletion initialization."""
    with patch('src.api.models.steps.generation.InferenceClient') as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        
        llm = LLMChatCompletion(
            hf_token="test_token",
            model_name="test_model",
            prompt_template="{context}{query}",
            max_tokens=100
        )
        
        assert llm.model_name == "test_model"
        assert llm.client == mock_instance
        assert llm.max_tokens == 100
        assert llm.prompt_template == "{context}{query}"
        mock_client.assert_called_once_with(model="test_model", token="test_token")


def test_llm_chat_completion_predict():
    """Test LLMChatCompletion predict method."""
    with patch('src.api.models.steps.generation.InferenceClient') as mock_client:
        mock_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = {'content': 'test response'}
        mock_instance.chat_completion.return_value = mock_response
        mock_client.return_value = mock_instance
        
        llm = LLMChatCompletion(
            hf_token="test_token",
            model_name="test_model",
            prompt_template="{context}{query}",
            max_tokens=100
        )
        
        query = "What is the capital of France?"
        context = "France is a country in Europe."
        
        result = llm.predict(query, context)
        
        assert result == "test response"
        mock_instance.chat_completion.assert_called_once()


def test_llm_chat_completion_predict_stream():
    """Test LLMChatCompletion predict method with stream."""
    with patch('src.api.models.steps.generation.InferenceClient') as mock_client:
        mock_instance = MagicMock()
        
        # Create a mock stream with multiple chunks
        mock_chunk1 = MagicMock()
        mock_chunk1.choices = [MagicMock()]
        mock_chunk1.choices[0].delta.content = "test "
        
        mock_chunk2 = MagicMock()
        mock_chunk2.choices = [MagicMock()]
        mock_chunk2.choices[0].delta.content = "response"
        
        mock_stream = [mock_chunk1, mock_chunk2]
        mock_instance.chat_completion.return_value = mock_stream
        mock_client.return_value = mock_instance
        
        llm = LLMChatCompletion(
            hf_token="test_token",
            model_name="test_model",
            prompt_template="{context}{query}",
            max_tokens=100
        )
        
        query = "What is the capital of France?"
        context = "France is a country in Europe."
        
        generator = llm.predict(query, context, stream=True)
        result = list(generator)
        
        assert result == ["test ", "response"]
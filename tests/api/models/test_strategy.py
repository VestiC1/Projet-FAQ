import pytest
from unittest.mock import patch, MagicMock, ANY
from src.api.models.strategy import RAG


def test_rag_initialization():
    """Test RAG initialization."""
    with patch('src.api.models.strategy.LLMChatCompletion') as mock_llm, \
         patch('src.api.models.strategy.RetreivalService') as mock_rag:
        
        mock_llm_instance = MagicMock()
        mock_llm.return_value = mock_llm_instance
        
        mock_rag_instance = MagicMock()
        mock_rag.return_value = mock_rag_instance
        
        strategy = RAG(
            hf_token="test_token",
            model_name="test_model",
            system_prompt="test_prompt",
            max_tokens=100,
            endpoint="test_endpoint",
            top_k=5
        )
        
        assert strategy.strategy_name == "RAG"
        assert strategy.llm == mock_llm_instance
        assert strategy.rag == mock_rag_instance
        
        mock_llm.assert_called_once_with(
            hf_token="test_token",
            model_name="test_model",
            prompt_template="test_prompt",
            max_tokens=100
        )
        
        mock_rag.assert_called_once_with(
            endpoint="test_endpoint",
            k=5
        )


def test_rag_build_context():
    """Test RAG _build_context method."""
    with patch('src.api.models.strategy.LLMChatCompletion'), \
         patch('src.api.models.strategy.RetreivalService'):
        
        strategy = RAG(
            hf_token="test_token",
            model_name="test_model",
            system_prompt="test_prompt",
            max_tokens=100,
            endpoint="test_endpoint",
            top_k=5
        )
        
        # Create mock documents
        mock_documents = [
            {'id': 1, 'answer': 'answer1', 'keywords': 'k1'},
            {'id': 2, 'answer': 'answer2', 'keywords': 'k2'}
        ]
        
        result = strategy._build_context(mock_documents)
        
        assert "Document [1]" in result
        assert "answer1" in result
        assert "k1" in result
        assert "Document [2]" in result
        assert "answer2" in result
        assert "k2" in result
        assert "----------" in result


def test_rag_answer():
    """Test RAG answer method."""
    with patch('src.api.models.strategy.LLMChatCompletion') as mock_llm, \
         patch('src.api.models.strategy.RetreivalService') as mock_rag:
        
        mock_llm_instance = MagicMock()
        mock_llm_instance.predict.return_value = "test answer"
        mock_llm.return_value = mock_llm_instance
        
        mock_rag_instance = MagicMock()
        mock_documents = [
            {'id': 1, 'answer': 'answer1', 'keywords': 'k1'}
        ]
        mock_rag_instance.search.return_value = mock_documents
        mock_rag.return_value = mock_rag_instance
        
        strategy = RAG(
            hf_token="test_token",
            model_name="test_model",
            system_prompt="test_prompt",
            max_tokens=100,
            endpoint="test_endpoint",
            top_k=5
        )
        
        question = "What is the capital of France?"
        result = strategy._answer(question, stream=False)
        
        assert result == "test answer"
        mock_rag_instance.search.assert_called_once_with(text=question)
        mock_llm_instance.predict.assert_called_once()


def test_rag_answer_stream():
    """Test RAG answer method with stream."""
    with patch('src.api.models.strategy.LLMChatCompletion') as mock_llm, \
         patch('src.api.models.strategy.RetreivalService') as mock_rag:
        
        mock_llm_instance = MagicMock()
        mock_llm_instance.predict.return_value = "test stream"
        mock_llm.return_value = mock_llm_instance
        
        mock_rag_instance = MagicMock()
        mock_documents = [
            {'id': 1, 'answer': 'answer1', 'keywords': 'k1'}
        ]
        mock_rag_instance.search.return_value = mock_documents
        mock_rag.return_value = mock_rag_instance
        
        strategy = RAG(
            hf_token="test_token",
            model_name="test_model",
            system_prompt="test_prompt",
            max_tokens=100,
            endpoint="test_endpoint",
            top_k=5
        )
        
        question = "What is the capital of France?"
        result = strategy._answer(question, stream=True)
        
        assert result == "test stream"
        mock_rag_instance.search.assert_called_once_with(text=question)
        mock_llm_instance.predict.assert_called_once_with(query=question, context=ANY, stream=True)
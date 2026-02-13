import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import pandas as pd
from src.core.strategies.strategyb import StrategyB


def test_strategy_b_initialization():
    """Test StrategyB initialization."""
    with patch('src.core.models.llm.InferenceClient') as mock_llm_client, \
         patch('src.core.models.rag.SentenceTransformer') as mock_st, \
         patch('src.core.models.rag.TinyRag.load_embeddings') as mock_load:
        
        # Mock LLM client
        mock_llm_instance = MagicMock()
        mock_llm_client.return_value = mock_llm_instance
        
        # Mock SentenceTransformer
        mock_st_instance = MagicMock()
        mock_st.return_value = mock_st_instance
        
        # Mock load_embeddings
        mock_df = pd.DataFrame({
            'id': [1, 2],
            'question': ['q1', 'q2'],
            'answer': ['answer1', 'answer2'],
            'keywords': ['k1', 'k2'],
            'embedding': [[0.1, 0.2], [0.3, 0.4]]
        })
        mock_load.return_value = mock_df
        
        strategy = StrategyB(
            hf_token="test_token",
            model_name="test_model",
            system_prompt="test_prompt",
            max_tokens=100,
            corpus=Path("/fake/path"),
            vec_name="test_vec",
            top_k=5
        )
        
        assert strategy.strategy_name == "Strategy_B"
        assert strategy.llm.model_name == "test_model"
        assert strategy.rag.model_name == "test_vec"
        
        mock_llm_client.assert_called_once_with(model="test_model", token="test_token")
        mock_st.assert_called_once_with("test_vec")
        mock_load.assert_called_once_with(Path("/fake/path"))


def test_strategy_b_build_context():
    """Test StrategyB _build_context method."""
    with patch('src.core.models.llm.InferenceClient'), \
         patch('src.core.models.rag.SentenceTransformer'), \
         patch('src.core.models.rag.TinyRag.load_embeddings'):
        
        strategy = StrategyB(
            hf_token="test_token",
            model_name="test_model",
            system_prompt="test_prompt",
            max_tokens=100,
            corpus=Path("/fake/path"),
            vec_name="test_vec",
            top_k=5
        )
        
        # Create mock documents
        mock_df = pd.DataFrame({
            'id': [1, 2],
            'question': ['q1', 'q2'],
            'answer': ['answer1', 'answer2'],
            'keywords': ['k1', 'k2']
        })
        
        result = strategy._build_context(mock_df)
        
        assert "Document [1]" in result
        assert "answer1" in result
        assert "k1" in result
        assert "Document [2]" in result
        assert "answer2" in result
        assert "k2" in result
        assert "----------" in result


def test_strategy_b_answer():
    """Test StrategyB answer method."""
    with patch('src.core.models.llm.InferenceClient') as mock_llm_client, \
         patch('src.core.models.rag.SentenceTransformer') as mock_st, \
         patch('src.core.models.rag.TinyRag.load_embeddings') as mock_load, \
         patch('src.core.models.rag.compute_embeddings') as mock_compute:
        
        # Mock LLM client
        mock_llm_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = {'content': 'test answer'}
        mock_llm_instance.chat_completion.return_value = mock_response
        mock_llm_client.return_value = mock_llm_instance
        
        # Mock SentenceTransformer
        mock_st_instance = MagicMock()
        mock_st_instance.encode.return_value = [[0.5, 0.5]]
        mock_st.return_value = mock_st_instance
        
        # Mock load_embeddings
        mock_df = pd.DataFrame({
            'id': [1],
            'question': ['q1'],
            'answer': ['answer1'],
            'keywords': ['k1'],
            'embedding': [[0.1, 0.2]]
        })
        mock_load.return_value = mock_df
        
        # Mock compute_embeddings
        mock_vector = MagicMock()
        mock_vector.T = [0.5, 0.5]
        mock_compute.return_value = [mock_vector]
        
        strategy = StrategyB(
            hf_token="test_token",
            model_name="test_model",
            system_prompt="test_prompt",
            max_tokens=100,
            corpus=Path("/fake/path"),
            vec_name="test_vec",
            top_k=5
        )
        
        # Mock search to return the mock_df
        with patch.object(strategy.rag, 'search', return_value=mock_df):
            question = "What is the capital of France?"
            result = strategy._answer(question)
            
            # The predict method returns a tuple (answer, context)
            # For StrategyB, context is the built context from documents
            assert result[0] == "test answer"
            assert isinstance(result[1], str)
            assert "Document [1]" in result[1]
            assert "answer1" in result[1]
            mock_llm_instance.chat_completion.assert_called_once()
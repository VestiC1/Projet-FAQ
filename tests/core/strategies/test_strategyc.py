import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import pandas as pd
from src.core.strategies.strategyc import StrategyC


def test_strategy_c_initialization():
    """Test StrategyC initialization."""
    with patch('src.core.models.rag.SentenceTransformer') as mock_st, \
         patch('src.core.models.rag.TinyRag.load_embeddings') as mock_load, \
         patch('src.core.models.qna.pipeline') as mock_pipeline:
        
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
        
        # Mock QnA pipeline
        mock_pipeline_instance = MagicMock()
        mock_pipeline.return_value = mock_pipeline_instance
        
        strategy = StrategyC(
            corpus=Path("/fake/path"),
            vec_model_name="test_vec",
            top_k=5,
            qna_model_name="test_qna"
        )
        
        assert strategy.strategy_name == "Strategy_C"
        assert strategy.rag.model_name == "test_vec"
        assert strategy.qna.model_name == "test_qna"
        
        mock_st.assert_called_once_with("test_vec")
        mock_load.assert_called_once_with(Path("/fake/path"))
        mock_pipeline.assert_called_once_with(task="question-answering", model="test_qna")


def test_strategy_c_build_context():
    """Test StrategyC _build_context method."""
    with patch('src.core.models.rag.SentenceTransformer'), \
         patch('src.core.models.rag.TinyRag.load_embeddings'), \
         patch('src.core.models.qna.pipeline'):
        
        strategy = StrategyC(
            corpus=Path("/fake/path"),
            vec_model_name="test_vec",
            top_k=5,
            qna_model_name="test_qna"
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


def test_strategy_c_answer():
    """Test StrategyC answer method."""
    with patch('src.core.models.rag.SentenceTransformer') as mock_st, \
         patch('src.core.models.rag.TinyRag.load_embeddings') as mock_load, \
         patch('src.core.models.qna.pipeline') as mock_pipeline, \
         patch('src.core.models.rag.compute_embeddings') as mock_compute:
        
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
        
        # Mock QnA pipeline
        mock_pipeline_instance = MagicMock()
        mock_pipeline_instance.return_value = {"answer": "test answer", "score": 0.9}
        mock_pipeline.return_value = mock_pipeline_instance
        
        # Mock compute_embeddings
        mock_vector = MagicMock()
        mock_vector.T = [0.5, 0.5]
        mock_compute.return_value = [mock_vector]
        
        strategy = StrategyC(
            corpus=Path("/fake/path"),
            vec_model_name="test_vec",
            top_k=5,
            qna_model_name="test_qna"
        )
        
        # Mock search to return the mock_df
        with patch.object(strategy.rag, 'search', return_value=mock_df):
            question = "What is the capital of France?"
            result, context = strategy._answer(question)
            
            assert result == "test answer"
            assert isinstance(context, str)
            mock_pipeline_instance.assert_called_once()
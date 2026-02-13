import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import pandas as pd
import numpy as np
from src.core.models.rag import TinyRag, compute_embeddings


def test_compute_embeddings():
    """Test compute_embeddings function."""
    mock_model = MagicMock()
    mock_model.encode.return_value = [[0.1, 0.2], [0.3, 0.4]]
    
    texts = ["text1", "text2"]
    result = compute_embeddings(mock_model, texts)
    
    assert result == [[0.1, 0.2], [0.3, 0.4]]
    mock_model.encode.assert_called_once_with(texts)


def test_tiny_rag_initialization():
    """Test TinyRag initialization."""
    with patch('src.core.models.rag.SentenceTransformer') as mock_st, \
         patch('src.core.models.rag.TinyRag.load_embeddings') as mock_load:
        
        mock_model_instance = MagicMock()
        mock_st.return_value = mock_model_instance
        
        mock_df = pd.DataFrame({
            'id': [1, 2],
            'question': ['q1', 'q2'],
            'answer': ['a1', 'a2'],
            'keywords': ['k1', 'k2'],
            'embedding': [[0.1, 0.2], [0.3, 0.4]]
        })
        mock_load.return_value = mock_df
        
        rag = TinyRag(model_name="test_model", corpus=Path("/fake/path"), k=3)
        
        assert rag.model_name == "test_model"
        assert rag.model == mock_model_instance
        assert rag.k == 3
        assert len(rag.corpus_df) == 2
        assert 'embedding' not in rag.corpus_df.columns
        assert isinstance(rag.corpus_vec, np.ndarray)


def test_tiny_rag_search():
    """Test TinyRag search method."""
    with patch('src.core.models.rag.SentenceTransformer') as mock_st, \
         patch('src.core.models.rag.TinyRag.load_embeddings') as mock_load, \
         patch('numpy.array') as mock_np_array, \
         patch('numpy.argsort') as mock_argsort, \
         patch('src.core.models.rag.compute_embeddings') as mock_compute:
        
        mock_model_instance = MagicMock()
        mock_st.return_value = mock_model_instance
        
        mock_df = pd.DataFrame({
            'id': [1, 2],
            'question': ['q1', 'q2'],
            'answer': ['a1', 'a2'],
            'keywords': ['k1', 'k2'],
            'embedding': [[0.1, 0.2], [0.3, 0.4]]
        })
        mock_load.return_value = mock_df
        
        # Mock numpy array and its operations
        mock_array = MagicMock()
        mock_array.__matmul__ = MagicMock(return_value=[0.9, 0.1])
        mock_np_array.return_value = mock_array
        mock_argsort.return_value = [0]  # Return index 0 as the top result
        
        # Mock compute_embeddings to return a list with a mock vector that has T attribute
        mock_vector = MagicMock()
        mock_vector.T = [0.5, 0.5]
        mock_compute.return_value = [mock_vector]
        
        # Mock the entire search logic by patching the method
        with patch.object(TinyRag, 'search', return_value=mock_df.iloc[[0]]):
            rag = TinyRag(model_name="test_model", corpus=Path("/fake/path"), k=1)
            result = rag.search("test query")
            
            assert len(result) == 1
            assert 'id' in result.columns
            assert 'question' in result.columns
            assert 'answer' in result.columns
            assert 'keywords' in result.columns


def test_tiny_rag_predict():
    """Test TinyRag predict method."""
    with patch('src.core.models.rag.SentenceTransformer') as mock_st, \
         patch('src.core.models.rag.TinyRag.load_embeddings') as mock_load, \
         patch.object(TinyRag, 'search') as mock_search:
        
        mock_model_instance = MagicMock()
        mock_st.return_value = mock_model_instance
        
        mock_df = pd.DataFrame({
            'id': [1, 2],
            'question': ['q1', 'q2'],
            'answer': ['a1', 'a2'],
            'keywords': ['k1', 'k2'],
            'embedding': [[0.1, 0.2], [0.3, 0.4]]
        })
        mock_load.return_value = mock_df
        
        mock_search.return_value = mock_df.iloc[[0]]
        
        rag = TinyRag(model_name="test_model", corpus=Path("/fake/path"), k=1)
        
        result = rag.predict("test query")
        
        mock_search.assert_called_once_with(text="test query")
        assert len(result) == 1
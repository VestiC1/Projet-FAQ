import pytest
from unittest.mock import patch, MagicMock
from src.api.dependencies import get_supabase, get_rag


def test_get_supabase():
    """Test get_supabase function."""
    with patch('src.api.dependencies.create_client') as mock_create_client:
        mock_client = MagicMock()
        mock_create_client.return_value = mock_client
        
        result = get_supabase()
        
        assert result == mock_client
        mock_create_client.assert_called_once()


def test_get_rag():
    """Test get_rag function."""
    with patch('src.api.dependencies.RAG') as mock_rag:
        mock_instance = MagicMock()
        mock_rag.return_value = mock_instance
        
        result = get_rag()
        
        assert result == mock_instance
        mock_rag.assert_called_once()
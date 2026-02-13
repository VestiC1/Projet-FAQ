import pytest
from unittest.mock import patch, MagicMock
from src.api.models.steps.retrieval import RetreivalService


def test_retrieval_service_initialization():
    """Test RetreivalService initialization."""
    service = RetreivalService(endpoint="test_endpoint", k=5, threshold=0.5)
    
    assert service.model_name == "modal"
    assert service._endpoint == "test_endpoint"
    assert service._k == 5
    assert service._threshold == 0.5


def test_retrieval_service_search():
    """Test RetreivalService search method."""
    with patch('src.api.models.steps.retrieval.requests.post') as mock_post:
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'results': [
                {'content': '{"id": 1, "answer": "answer1", "keywords": "k1"}'},
                {'content': '{"id": 2, "answer": "answer2", "keywords": "k2"}'}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        service = RetreivalService(endpoint="test_endpoint", k=5)
        
        result = service.search("test query")
        
        assert len(result) == 2
        assert result[0]['id'] == 1
        assert result[0]['answer'] == "answer1"
        assert result[0]['keywords'] == "k1"
        assert result[1]['id'] == 2
        assert result[1]['answer'] == "answer2"
        assert result[1]['keywords'] == "k2"
        
        mock_post.assert_called_once_with(
            "test_endpoint",
            json={"query": "query : test query", "top_k": 10, "threshold": 0.0}
        )


def test_retrieval_service_predict():
    """Test RetreivalService predict method."""
    with patch('src.api.models.steps.retrieval.requests.post') as mock_post:
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'results': [
                {'content': '{"id": 1, "answer": "answer1", "keywords": "k1"}'}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        service = RetreivalService(endpoint="test_endpoint", k=5)
        
        result = service.predict("test query")
        
        assert len(result) == 1
        assert result[0]['id'] == 1
        
        mock_post.assert_called_once()
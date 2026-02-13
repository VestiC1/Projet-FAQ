import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.api.main import app
from src.api.routes import Query


def test_answer_endpoint():
    """Test the answer endpoint."""
    client = TestClient(app)
    
    # Test data
    test_data = {"question": "What is the capital of France?"}
    
    response = client.post("/answer", json=test_data)
    
    assert response.status_code == 200
    # Just check that we get a response, the actual answer will depend on the real RAG implementation
    assert "answer" in response.json()


def test_answer_stream_endpoint():
    """Test the answer stream endpoint."""
    client = TestClient(app)
    
    # Test data
    test_data = {"question": "What is the capital of France?"}
    
    response = client.post("/answer/stream", json=test_data)
    
    assert response.status_code == 200
    # For streaming responses, we can check the content type
    assert "text/event-stream" in response.headers['content-type']


def test_faq_endpoint():
    """Test the FAQ endpoint."""
    client = TestClient(app)
    
    # Mock the get_supabase dependency
    with patch('src.api.routes.get_supabase') as mock_get_supabase:
        mock_sb = MagicMock()
        mock_get_supabase.return_value = mock_sb
        
        # Mock the get_faq function
        with patch('src.api.routes.get_faq') as mock_get_faq:
            mock_get_faq.return_value = ["question1", "question2"]
            
            response = client.get("/FAQ")
            
            assert response.status_code == 200
            assert response.json() == {"faq": ["question1", "question2"]}
            mock_get_faq.assert_called_once()


def test_documents_endpoint():
    """Test the documents endpoint."""
    client = TestClient(app)
    
    # Mock the get_supabase dependency
    with patch('src.api.routes.get_supabase') as mock_get_supabase:
        mock_sb = MagicMock()
        mock_get_supabase.return_value = mock_sb
        
        # Mock the get_document function
        with patch('src.api.routes.get_document') as mock_get_document:
            mock_get_document.return_value = "test document content"
            
            response = client.get("/documents/123")
            
            assert response.status_code == 200
            assert response.json() == {"document": "test document content"}
            mock_get_document.assert_called_once()


def test_query_model():
    """Test the Query Pydantic model."""
    # Test valid data
    query = Query(question="What is the capital of France?")
    assert query.question == "What is the capital of France?"
    
    # Test with empty string (should be valid)
    query_empty = Query(question="")
    assert query_empty.question == ""
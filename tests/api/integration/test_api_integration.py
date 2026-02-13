"""
Integration tests for the API using a fake client.
These tests simulate real API calls without mocking the internal components.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.api.main import app


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


def test_full_api_flow(client):
    """Test the full API flow from request to response."""
    # Test data
    test_question = "What is the capital of France?"
    
    # Test the answer endpoint
    response = client.post("/answer", json={"question": test_question})
    
    assert response.status_code == 200
    assert "answer" in response.json()
    assert isinstance(response.json()["answer"], str)


def test_streaming_api_flow(client):
    """Test the streaming API flow."""
    test_question = "What is the capital of France?"
    
    # Test the streaming answer endpoint
    response = client.post("/answer/stream", json={"question": test_question})
    
    assert response.status_code == 200
    assert "text/event-stream" in response.headers['content-type']


def test_faq_endpoint_integration(client):
    """Test the FAQ endpoint with real service calls."""
    # Mock the supabase client to avoid real database calls
    with patch('src.api.routes.get_supabase') as mock_get_supabase:
        mock_sb = MagicMock()
        mock_get_supabase.return_value = mock_sb
        
        # Mock the database response
        mock_table = MagicMock()
        mock_sb.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        
        mock_result = MagicMock()
        mock_result.data = [
            {"content": '{"id": 1, "question": "Q1", "answer": "A1"}'},
            {"content": '{"id": 2, "question": "Q2", "answer": "A2"}'}
        ]
        mock_table.execute.return_value = mock_result
        
        response = client.get("/FAQ")
        
        assert response.status_code == 200
        assert "faq" in response.json()
        assert isinstance(response.json()["faq"], list)


def test_documents_endpoint_integration(client):
    """Test the documents endpoint with real service calls."""
    # Mock the supabase client to avoid real database calls
    with patch('src.api.routes.get_supabase') as mock_get_supabase:
        mock_sb = MagicMock()
        mock_get_supabase.return_value = mock_sb
        
        # Mock the table methods to return a proper result based on the FAQ structure
        mock_table = MagicMock()
        mock_sb.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.maybe_single.return_value = mock_table
        
        # Mock the execute method to return a proper result object matching the FAQ structure
        # Based on the FAQ data structure from data/faq-base-6964b97cf0c25947575840.json
        mock_result = MagicMock()
        mock_result.data = {
            "content": {
                "id": "EC001",
                "category": "etat_civil",
                "question": "Comment obtenir un acte de naissance ?",
                "answer": "Pour obtenir un acte de naissance, vous pouvez faire la demande en ligne sur le site service-public.fr, par courrier à la mairie du lieu de naissance, ou directement au guichet. La demande est gratuite. Munissez-vous d'une pièce d'identité. Le délai de délivrance est de 3 à 10 jours ouvrés selon le mode de demande.",
                "keywords": ["naissance", "acte", "extrait", "certificat", "état civil"]
            }
        }
        mock_table.execute.return_value = mock_result
        
        response = client.get("/documents/EC001")  # Using the actual ID from the FAQ
        
        assert response.status_code == 200
        assert "document" in response.json()
        
        # Verify the document structure matches the FAQ structure
        document = response.json()["document"]
        assert isinstance(document, dict)
        assert "id" in document
        assert "category" in document
        assert "question" in document
        assert "answer" in document
        assert "keywords" in document
        
        # Verify the content matches our mock data
        assert document["id"] == "EC001"
        assert document["category"] == "etat_civil"
        assert "acte de naissance" in document["answer"]


def test_healthcheck_endpoint_integration(client):
    """Test the healthcheck endpoint."""
    response = client.get("/healthcheck")
    
    assert response.status_code == 200
    assert response.json()["status"] == "OK"


def test_home_endpoint_integration(client):
    """Test the home endpoint."""
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json()["message"] == "home"


def test_invalid_endpoint(client):
    """Test that invalid endpoints return proper error responses."""
    response = client.get("/invalid-endpoint")
    
    assert response.status_code == 404


def test_invalid_method(client):
    """Test that invalid methods return proper error responses."""
    response = client.put("/answer")
    
    assert response.status_code == 405


def test_malformed_json(client):
    """Test that malformed JSON returns proper error responses."""
    response = client.post("/answer", data="not valid json", headers={"Content-Type": "application/json"})
    
    assert response.status_code == 422  # Unprocessable Entity


def test_empty_question(client):
    """Test that empty questions are handled properly."""
    response = client.post("/answer", json={"question": ""})
    
    assert response.status_code == 200
    assert "answer" in response.json()


def test_long_question(client):
    """Test that long questions are handled properly."""
    long_question = "A" * 1000  # Very long question
    response = client.post("/answer", json={"question": long_question})
    
    assert response.status_code == 200
    assert "answer" in response.json()


def test_special_characters_in_question(client):
    """Test that special characters in questions are handled properly."""
    special_question = "What is the capital of France? !@#$%^&*()_+"
    response = client.post("/answer", json={"question": special_question})
    
    assert response.status_code == 200
    assert "answer" in response.json()


def test_unicode_in_question(client):
    """Test that unicode characters in questions are handled properly."""
    unicode_question = "Quelle est la capitale de la France? 🇫🇷"
    response = client.post("/answer", json={"question": unicode_question})
    
    assert response.status_code == 200
    assert "answer" in response.json()
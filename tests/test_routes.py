from fastapi.testclient import TestClient
from src.app.main import app
from unittest.mock import patch


client = TestClient(app)

def test_home():
    """Teste la route /."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "home"}

def test_health():
    """Teste la route /healthcheck."""
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_faq():
    """Teste la route /FAQ."""
    mock_faq = {"faq": [{"id": 1, "question": "Test?"}]}
    with patch("src.app.routes.faq_json", mock_faq):
        response = client.get("/FAQ")
        assert response.status_code == 200
        assert response.json() == {"faq": [{"id": 1, "question": "Test?"}]}

def test_documents_found():
    """Teste la route /documents/{id} avec un document existant."""
    mock_faq = {"faq": [{"id": 1, "question": "Test?"}]}
    with patch("src.app.routes.faq_json", mock_faq):
        response = client.get("/documents/1")
        assert response.status_code == 200
        assert response.json() == {"document": [{"id": 1, "question": "Test?"}]}

def test_documents_not_found():
    """Teste la route /documents/{id} avec un document inexistant."""
    mock_faq = {"faq": [{"id": 1, "question": "Test?"}]}
    with patch("src.app.routes.faq_json", mock_faq):
        response = client.get("/documents/99")
        assert response.status_code == 200
        assert response.json() == {"document": []}

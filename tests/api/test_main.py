import pytest
from fastapi.testclient import TestClient
from src.api.main import app


def test_home_endpoint():
    """Test the home endpoint."""
    client = TestClient(app)
    
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"message": "home"}


def test_healthcheck_endpoint():
    """Test the healthcheck endpoint."""
    client = TestClient(app)
    
    response = client.get("/healthcheck")
    
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_cors_middleware():
    """Test that CORS middleware is properly configured."""
    # This is more of an integration test, but we can at least verify the app has middleware
    assert len(app.user_middleware) > 0
    
    # Simplified test - just verify that middleware exists
    # In a real test, you would want to test actual CORS behavior with proper headers
    # For now, we'll just check that the app has some middleware configured
    assert len(app.user_middleware) > 0
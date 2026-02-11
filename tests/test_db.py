import pytest
from unittest.mock import mock_open, patch
from pathlib import Path
from src.app.db.load import load_faq, get_document
import json


def test_load_faq_success():
    """Teste le chargement réussi d'un fichier FAQ."""
    mock_json = {"faq": [{"id": 1, "question": "Test?"}]}

    # Mock de Path.exists() pour retourner True
    with patch.object(Path, 'exists', return_value=True), \
         patch("builtins.open", mock_open(read_data=json.dumps(mock_json))):
        result = load_faq(Path("dummy_path"))
        assert result == mock_json

def test_load_faq_file_not_found():
    """Teste le cas où le fichier FAQ est introuvable."""
    with patch("pathlib.Path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            load_faq(Path("dummy_path"))

def test_get_document_found():
    """Teste la récupération d'un document existant."""
    mock_faq = {"faq": [{"id": "1", "question": "Test?"}]}
    result = get_document(mock_faq, "1")
    assert result == [{"id": "1", "question": "Test?"}]

def test_get_document_not_found():
    """Teste la récupération d'un document inexistant."""
    mock_faq = {"faq": [{"id": "1", "question": "Test?"}]}
    result = get_document(mock_faq, 99)
    assert result == []

import pytest
from unittest.mock import patch, mock_open
from pathlib import Path
import json
from src.core.utils.data_loader import load_json, load_faq, load_golden


def test_load_json_success():
    """Test load_json function with valid JSON file."""
    mock_data = {"key": "value"}
    
    with patch('builtins.open', mock_open(read_data=json.dumps(mock_data))), \
         patch('pathlib.Path.exists', return_value=True):
        result = load_json(Path("/fake/path.json"))
        assert result == mock_data


def test_load_json_file_not_found():
    """Test load_json function with non-existent file."""
    mock_path = Path("/non/existent/path.json")
    
    with patch('pathlib.Path.exists', return_value=False):
        with pytest.raises(FileNotFoundError) as excinfo:
            load_json(mock_path)
        
        assert "File not found" in str(excinfo.value)


def test_load_faq():
    """Test load_faq function."""
    mock_data = [{"question": "q1", "answer": "a1"}]
    
    with patch('src.core.utils.data_loader.load_json') as mock_load:
        mock_load.return_value = mock_data
        result = load_faq()
        assert result == mock_data
        mock_load.assert_called_once()


def test_load_golden():
    """Test load_golden function."""
    mock_data = [{"question": "q1", "answer": "a1"}]
    
    with patch('src.core.utils.data_loader.load_json') as mock_load:
        mock_load.return_value = mock_data
        result = load_golden()
        assert result == mock_data
        mock_load.assert_called_once()
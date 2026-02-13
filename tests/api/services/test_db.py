import pytest
from unittest.mock import MagicMock
from src.api.services.db import get_faq, get_document


def test_get_faq():
    """Test get_faq function."""
    # Create a mock supabase client
    mock_sb = MagicMock()
    
    # Mock the table and select methods
    mock_table = MagicMock()
    mock_sb.table.return_value = mock_table
    mock_table.select.return_value = mock_table
    
    # Mock the execute method to return test data
    mock_result = MagicMock()
    mock_result.data = [
        {"content": "question1"},
        {"content": "question2"}
    ]
    mock_table.execute.return_value = mock_result
    
    # Call the function
    result = get_faq(mock_sb)
    
    # Assertions
    assert result == ["question1", "question2"]
    mock_sb.table.assert_called_once_with("documents")
    mock_table.select.assert_called_once_with("content")


def test_get_document():
    """Test get_document function."""
    # Create a mock supabase client
    mock_sb = MagicMock()
    
    # Mock the table and select methods
    mock_table = MagicMock()
    mock_sb.table.return_value = mock_table
    mock_table.select.return_value = mock_table
    mock_table.eq.return_value = mock_table
    
    # Mock the maybe_single and execute methods
    mock_maybe_single = MagicMock()
    mock_table.maybe_single.return_value = mock_maybe_single
    
    mock_result = MagicMock()
    mock_result.data = {"content": "test document content"}
    mock_maybe_single.execute.return_value = mock_result
    
    # Call the function
    result = get_document(mock_sb, "test_id")
    
    # Assertions
    assert result == "test document content"
    mock_sb.table.assert_called_once_with("documents")
    mock_table.select.assert_called_once_with("content")
    mock_table.eq.assert_called_once_with("content->>id", "test_id")


def test_get_document_not_found():
    """Test get_document function when document is not found."""
    # Create a mock supabase client
    mock_sb = MagicMock()
    
    # Mock the table and select methods
    mock_table = MagicMock()
    mock_sb.table.return_value = mock_table
    mock_table.select.return_value = mock_table
    mock_table.eq.return_value = mock_table
    
    # Mock the maybe_single and execute methods to return None
    mock_maybe_single = MagicMock()
    mock_table.maybe_single.return_value = mock_maybe_single
    
    mock_result = MagicMock()
    mock_result.data = None
    mock_maybe_single.execute.return_value = mock_result
    
    # Call the function
    result = get_document(mock_sb, "non_existent_id")
    
    # Assertions
    assert result is None
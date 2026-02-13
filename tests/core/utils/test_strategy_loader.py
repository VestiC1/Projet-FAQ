import pytest
from unittest.mock import patch, MagicMock
from src.core.utils.strategy_loader import make_strategy_a, make_strategy_b, make_strategy_c


def test_make_strategy_a():
    """Test make_strategy_a function."""
    with patch('src.strategies.StrategyA') as mock_strategy:
        mock_instance = MagicMock()
        mock_strategy.return_value = mock_instance
        
        result = make_strategy_a()
        
        assert result == mock_instance
        mock_strategy.assert_called_once()


def test_make_strategy_b():
    """Test make_strategy_b function."""
    with patch('src.strategies.StrategyB') as mock_strategy:
        mock_instance = MagicMock()
        mock_strategy.return_value = mock_instance
        
        result = make_strategy_b()
        
        assert result == mock_instance
        mock_strategy.assert_called_once()


def test_make_strategy_c():
    """Test make_strategy_c function."""
    with patch('src.strategies.StrategyC') as mock_strategy:
        mock_instance = MagicMock()
        mock_strategy.return_value = mock_instance
        
        result = make_strategy_c()
        
        assert result == mock_instance
        mock_strategy.assert_called_once()
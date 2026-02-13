import pytest
from unittest.mock import patch, MagicMock
from src.core.models.qna import QnAExtractor


def test_qna_extractor_initialization():
    """Test QnAExtractor initialization."""
    with patch('src.core.models.qna.pipeline') as mock_pipeline:
        mock_instance = MagicMock()
        mock_pipeline.return_value = mock_instance
        
        qna = QnAExtractor(model_name="test_model")
        
        assert qna.model_name == "test_model"
        assert qna.model == mock_instance
        mock_pipeline.assert_called_once_with(task="question-answering", model="test_model")


def test_qna_extractor_predict():
    """Test QnAExtractor predict method."""
    with patch('src.core.models.qna.pipeline') as mock_pipeline:
        mock_instance = MagicMock()
        mock_instance.return_value = {"answer": "test answer", "score": 0.9}
        mock_pipeline.return_value = mock_instance
        
        qna = QnAExtractor(model_name="test_model")
        
        question = "What is the capital of France?"
        context = "France is a country in Europe."
        
        result, returned_context = qna.predict(question, context)
        
        assert result == {"answer": "test answer", "score": 0.9}
        assert returned_context == context
        mock_instance.assert_called_once_with(question=question, context=context)
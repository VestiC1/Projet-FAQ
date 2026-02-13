"""
Test suite for config.py to ensure all exported variables are properly defined and not None.
"""
import pytest
import sys
import os

# Add the project root to Python path to import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_config_variables_not_none():
    """Test that all critical variables exported from config.py are not None."""
    # Import config module
    import config
    
    # Get all variables that don't start with underscore (private)
    config_vars = [name for name in dir(config) if not name.startswith('_')]
    
    # Variables that can be None (optional environment variables)
    optional_vars = ['FRONTEND_HOST', 'MODAL_ENDPOINT', 'GEMINI_TOKEN', 'CHAT_TOKEN']  # Add other optional vars here
    
    # Check each variable
    for var_name in config_vars:
        var_value = getattr(config, var_name)
        
        # Skip modules and functions
        if callable(var_value) or var_name in ['os', 'Path']:
            continue
            
        # Skip optional variables
        if var_name in optional_vars:
            continue
            
        # Assert the variable is not None
        assert var_value is not None, f"Config variable '{var_name}' is None"
        
        # For string variables, assert they are not empty
        if isinstance(var_value, str):
            assert len(var_value) > 0, f"Config variable '{var_name}' is an empty string"
            
        # For list/dict variables, assert they are not empty
        elif isinstance(var_value, (list, dict)):
            assert len(var_value) > 0, f"Config variable '{var_name}' is an empty {type(var_value).__name__}"


def test_specific_critical_config_variables():
    """Test specific critical configuration variables that are essential for the application."""
    import config
    
    # Test critical variables that should have specific types/values
    critical_vars = {
        'HF_TOKEN': str,
        'LLMNAME': str,
        'embd_model_name': str,
        'RAG_K': int,
        'FAQ_VEC': config.Path,  # Should be a Path object
        'qna_model_name': str,
        'system_prompt_template': dict,
    }
    
    for var_name, expected_type in critical_vars.items():
        assert hasattr(config, var_name), f"Missing critical config variable: {var_name}"
        
        var_value = getattr(config, var_name)
        assert var_value is not None, f"Critical config variable '{var_name}' is None"
        
        if expected_type is not dict or not isinstance(var_value, dict):
            assert isinstance(var_value, expected_type), \
                f"Config variable '{var_name}' should be {expected_type.__name__}, got {type(var_value).__name__}"
        
        # Additional specific checks
        if var_name == 'system_prompt_template':
            # Should be a dict with keys A, B, C
            assert isinstance(var_value, dict), "system_prompt_template should be a dict"
            assert 'A' in var_value, "system_prompt_template should have key 'A'"
            assert 'B' in var_value, "system_prompt_template should have key 'B'"
            assert 'C' in var_value, "system_prompt_template should have key 'C'"
            
            # Each prompt should be a non-empty string
            for key, prompt in var_value.items():
                assert isinstance(prompt, str), f"system_prompt_template['{key}'] should be a string"
                assert len(prompt) > 0, f"system_prompt_template['{key}'] should not be empty"
                
                # Check for required placeholders based on strategy type
                if key == 'A':
                    # Strategy A: direct LLM approach, only needs {query}
                    assert '{query}' in prompt, f"system_prompt_template['{key}'] should contain {{query}} placeholder"
                elif key == 'B':
                    # Strategy B: RAG approach, needs both {query} and {context}
                    assert '{query}' in prompt, f"system_prompt_template['{key}'] should contain {{query}} placeholder"
                    assert '{context}' in prompt, f"system_prompt_template['{key}'] should contain {{context}} placeholder"
                elif key == 'C':
                    # Strategy C: uses only {context} placeholder (context contains the answer)
                    assert '{context}' in prompt, f"system_prompt_template['{key}'] should contain {{context}} placeholder"
        
        elif var_name == 'RAG_K':
            # RAG_K should be a positive integer
            assert var_value > 0, "RAG_K should be a positive integer"
        
        elif var_name == 'FAQ_VEC':
            # FAQ_VEC should be a Path object pointing to a file
            assert var_value.exists() or str(var_value).endswith('.json'), \
                f"FAQ_VEC should point to a valid file path: {var_value}"


@pytest.mark.skipif(not os.path.exists('config.py'), reason="config.py not found")
def test_config_file_exists_and_readable():
    """Test that config.py file exists and is readable."""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.py')
    
    assert os.path.exists(config_path), "config.py file does not exist"
    assert os.path.isfile(config_path), "config.py is not a regular file"
    assert os.access(config_path, os.R_OK), "config.py is not readable"
    
    # Try to read the file
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
        assert len(content) > 0, "config.py is empty"


def test_config_environment_variables():
    """Test that environment variables used in config are properly set or have defaults."""
    import config
    
    # Check if any environment variables are used in config
    # This is a basic check - you might want to extend this based on your actual config implementation
    env_vars_in_config = ['HF_TOKEN']  # Add other env vars used in your config
    
    for env_var in env_vars_in_config:
        if hasattr(config, env_var):
            value = getattr(config, env_var)
            assert value is not None, f"Environment variable {env_var} is None"
            if isinstance(value, str):
                assert len(value) > 0, f"Environment variable {env_var} is empty"


def test_config_consistency():
    """Test that config variables are consistent with each other."""
    import config
    
    # Example: If you have related variables that should be consistent
    # Add your specific consistency checks here
    
    # For example, if you have model names, they should be non-empty strings
    model_vars = ['LLMNAME', 'embd_model_name', 'qna_model_name']
    for var_name in model_vars:
        if hasattr(config, var_name):
            value = getattr(config, var_name)
            assert isinstance(value, str), f"{var_name} should be a string"
            assert len(value) > 0, f"{var_name} should not be empty"
            # Could add more specific checks like model name format
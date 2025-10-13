"""Pytest configuration and fixtures for cvasl-gui tests."""

import pytest
import os
import tempfile
import shutil


@pytest.fixture(scope="session")
def temp_working_dir():
    """Create a temporary working directory for tests"""
    temp_dir = tempfile.mkdtemp(prefix="cvasl_test_")
    
    # Create subdirectories
    os.makedirs(os.path.join(temp_dir, 'data'), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, 'jobs'), exist_ok=True)
    
    # Set environment variable
    original_dir = os.getenv("CVASL_WORKING_DIRECTORY")
    os.environ["CVASL_WORKING_DIRECTORY"] = temp_dir
    
    yield temp_dir
    
    # Cleanup
    if original_dir:
        os.environ["CVASL_WORKING_DIRECTORY"] = original_dir
    else:
        os.environ.pop("CVASL_WORKING_DIRECTORY", None)
    
    # Remove temp directory
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def dash_app():
    """Get the Dash app instance"""
    from cvasl_gui.app import app
    return app


@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    import pandas as pd
    
    data = pd.DataFrame({
        'participant_id': ['P001', 'P002', 'P003', 'P004'],
        'Site': ['Site1', 'Site1', 'Site2', 'Site2'],
        'Age': [25, 30, 35, 40],
        'Sex': ['M', 'F', 'M', 'F'],
        'feature1': [1.0, 2.0, 3.0, 4.0],
        'feature2': [5.0, 6.0, 7.0, 8.0],
    })
    
    return data

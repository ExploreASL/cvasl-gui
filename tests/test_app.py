import pytest
import os


def test_app_imports():
    """Test that the app can be imported without errors"""
    from cvasl_gui import app as app_module
    assert app_module.app is not None


def test_app_has_server():
    """Test that the app has a Flask server"""
    from cvasl_gui.app import app
    assert hasattr(app, 'server')
    assert app.server is not None


def test_index_imports():
    """Test that the index module can be imported"""
    from cvasl_gui import index
    assert index is not None


def test_app_layout_exists():
    """Test that the app has a layout defined"""
    from cvasl_gui.app import app
    assert app.layout is not None


def test_tabs_import():
    """Test that all tab modules can be imported"""
    from cvasl_gui.tabs import harmonization
    from cvasl_gui.tabs import prediction
    from cvasl_gui.tabs import parameters
    
    assert harmonization is not None
    assert prediction is not None
    assert parameters is not None


def test_components_import():
    """Test that component modules can be imported"""
    from cvasl_gui.components import data_table
    from cvasl_gui.components import directory_input
    from cvasl_gui.tabs import job_list
    
    assert data_table is not None
    assert directory_input is not None
    assert job_list is not None


@pytest.mark.parametrize("algorithm", [
    "neurocombat",
    "neuroharmonize",
    "covbat",
    "nestedcombat",
    "autocombat",
    "relief"
])
def test_algorithm_params_defined(algorithm):
    """Test that all algorithms have their parameters defined"""
    from cvasl_gui.tabs.harmonization import ALGORITHM_PARAMS
    
    assert algorithm in ALGORITHM_PARAMS
    assert "label" in ALGORITHM_PARAMS[algorithm]
    assert "parameters" in ALGORITHM_PARAMS[algorithm]
    assert isinstance(ALGORITHM_PARAMS[algorithm]["parameters"], list)


def test_parameters_structure():
    """Test that parameters dict has correct structure"""
    from cvasl_gui.tabs.parameters import parameters
    
    assert isinstance(parameters, dict)
    assert len(parameters) > 0
    
    for param_id, param_config in parameters.items():
        assert "type" in param_config, f"Parameter {param_id} missing 'type'"
        assert "label" in param_config, f"Parameter {param_id} missing 'label'"
        assert "description" in param_config, f"Parameter {param_id} missing 'description'"


def test_working_directory_setup():
    """Test that working directory is properly configured"""
    import os
    from cvasl_gui.tabs.harmonization import WORKING_DIR, INPUT_DIR, JOBS_DIR
    
    assert WORKING_DIR is not None
    assert INPUT_DIR is not None
    assert JOBS_DIR is not None
    
    # Check that paths are properly constructed
    assert INPUT_DIR == os.path.join(WORKING_DIR, 'data')
    assert JOBS_DIR == os.path.join(WORKING_DIR, 'jobs')

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pytest",
#     "click",
#     "rich",
# ]
# ///

"""Tests for update-layer-credentials.py, focusing on safety checks"""

import os
from pathlib import Path
import pytest
from save_layers_my_credentials import is_same_directory, process_layer_file

def create_test_file(path, content='{"test": true}'):
    """Create a test file with given content"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

def test_is_same_directory():
    """Test directory comparison function"""
    # Test regular paths
    assert is_same_directory('c:/temp', 'c:/temp')
    assert is_same_directory('c:/temp/', 'c:/temp')
    assert not is_same_directory('c:/temp', 'c:/temp/subdir')
    
    # Test case insensitivity
    assert is_same_directory('C:/Temp', 'c:/temp')
    assert is_same_directory('c:\\Temp', 'c:/temp')
    
    # Test UNC paths
    assert is_same_directory('\\\\server\\share', '\\\\server\\share')
    assert is_same_directory('\\\\SERVER\\share', '\\\\server\\SHARE')
    assert not is_same_directory('\\\\server1\\share', '\\\\server2\\share')
    
    # Test mixed slashes
    assert is_same_directory('c:/temp/path', 'c:\\temp\\path')
    assert is_same_directory('\\\\server/share', '\\\\server\\share')

def test_safety_checks(tmp_path):
    """Test safety checks in process_layer_file"""
    # Create test directories
    input_dir = tmp_path / 'input'
    output_dir = tmp_path / 'output'
    input_subdir = input_dir / 'subdir'
    output_subdir = output_dir / 'subdir'
    
    # Create test layer file
    layer_content = '''{
        "layerDefinitions": [{
            "featureTable": {
                "dataConnection": {
                    "type": "CIMStandardDataConnection",
                    "workspaceConnectionString": "SERVER=test;INSTANCE=test;AUTHENTICATION_MODE=DBMS"
                }
            }
        }]
    }'''
    test_file = input_dir / 'test.lyrx'
    create_test_file(test_file, layer_content)
    
    # Test 1: Same input/output directory
    success, error = process_layer_file(test_file, input_dir, input_dir, 'user', 'pass')
    assert not success
    assert "Output directory cannot be the same as input directory" in error
    
    # Test 2: Output is parent of input
    success, error = process_layer_file(test_file, input_subdir, input_dir, 'user', 'pass')
    assert not success
    assert "Output directory cannot be a parent of input directory" in error
    
    # Test 3: Input is parent of output
    success, error = process_layer_file(test_file, input_dir, input_subdir, 'user', 'pass')
    assert not success
    assert "Input directory cannot be a parent of output directory" in error
    
    # Test 4: Valid separate directories
    success, error = process_layer_file(test_file, input_dir, output_dir, 'user', 'pass')
    assert success
    assert error is None
    
    # Test 5: Flattened output
    success, error = process_layer_file(test_file, input_dir, output_dir, 'user', 'pass', flatten=True)
    assert success
    assert error is None

def test_unc_paths(tmp_path):
    """Test handling of UNC paths"""
    # Mock UNC paths using regular paths for testing
    unc_input = tmp_path / 'server' / 'share' / 'input'
    unc_output = tmp_path / 'server' / 'share' / 'output'
    
    # Create test layer file
    layer_content = '''{
        "layerDefinitions": [{
            "featureTable": {
                "dataConnection": {
                    "type": "CIMStandardDataConnection",
                    "workspaceConnectionString": "SERVER=test;INSTANCE=test;AUTHENTICATION_MODE=DBMS"
                }
            }
        }]
    }'''
    test_file = unc_input / 'test.lyrx'
    create_test_file(test_file, layer_content)
    
    # Convert paths to UNC-style strings
    unc_input_str = f'\\\\server\\share\\input'
    unc_output_str = f'\\\\server\\share\\output'
    
    # Test UNC path handling
    success, error = process_layer_file(test_file, unc_input, unc_output, 'user', 'pass')
    assert success
    assert error is None

def test_auth_modes(tmp_path):
    """Test handling of different authentication modes"""
    input_dir = tmp_path / 'input'
    output_dir = tmp_path / 'output'
    
    # Test DBMS authentication
    dbms_content = '''{
        "layerDefinitions": [{
            "featureTable": {
                "dataConnection": {
                    "type": "CIMStandardDataConnection",
                    "workspaceConnectionString": "SERVER=test;INSTANCE=test;AUTHENTICATION_MODE=DBMS"
                }
            }
        }]
    }'''
    dbms_file = input_dir / 'dbms.lyrx'
    create_test_file(dbms_file, dbms_content)
    
    # Test OSA authentication
    osa_content = '''{
        "layerDefinitions": [{
            "featureTable": {
                "dataConnection": {
                    "type": "CIMStandardDataConnection",
                    "workspaceConnectionString": "SERVER=test;INSTANCE=test;AUTHENTICATION_MODE=OSA"
                }
            }
        }]
    }'''
    osa_file = input_dir / 'osa.lyrx'
    create_test_file(osa_file, osa_content)
    
    # Test no authentication
    no_auth_content = '''{
        "layerDefinitions": [{
            "featureTable": {
                "dataConnection": {
                    "type": "CIMStandardDataConnection",
                    "workspaceConnectionString": "SERVER=test;INSTANCE=test"
                }
            }
        }]
    }'''
    no_auth_file = input_dir / 'no_auth.lyrx'
    create_test_file(no_auth_file, no_auth_content)
    
    # Test DBMS file
    success, error = process_layer_file(dbms_file, input_dir, output_dir, 'user', 'pass')
    assert success
    assert error is None
    
    # Test OSA file
    success, error = process_layer_file(osa_file, input_dir, output_dir, 'user', 'pass')
    assert not success
    assert "Layer uses OSA authentication (not DBMS)" in error
    
    # Test no auth file
    success, error = process_layer_file(no_auth_file, input_dir, output_dir, 'user', 'pass')
    assert not success
    assert "We only change database connections that use DBMS authentication" in error

if __name__ == '__main__':
    pytest.main([__file__, '-v'])

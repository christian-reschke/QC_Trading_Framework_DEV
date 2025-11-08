"""
Version control for strategy deployment verification
"""
import os
import re
import sys
from datetime import datetime
from utils import print_error, print_success

def get_next_version(current_version):
    """Auto-increment patch version (e.g., v2.1.0 -> v2.1.1)"""
    try:
        # Extract version numbers from string like "v2.1.0"
        version_part = current_version.replace('v', '')
        major, minor, patch = map(int, version_part.split('.'))
        
        # Increment patch version
        new_patch = patch + 1
        return f"v{major}.{minor}.{new_patch}"
    except:
        # Fallback if parsing fails
        return f"v2.1.{int(datetime.now().timestamp()) % 1000}"

def update_version():
    """Update version in strategy_config.py"""
    config_file = "strategy_config.py"
    
    # Read current config file
    with open(config_file, 'r') as f:
        content = f.read()
    
    # Extract current version
    version_match = re.search(r'STRATEGY_VERSION = "([^"]*)"', content)
    if not version_match:
        return "ERROR: Could not find STRATEGY_VERSION in strategy_config.py"
    
    current_version = version_match.group(1)
    next_version = get_next_version(current_version)
    
    # Replace version line
    updated_content = re.sub(
        r'STRATEGY_VERSION = "[^"]*"',
        f'STRATEGY_VERSION = "{next_version}"',
        content
    )
    
    # Write back to config file
    with open(config_file, 'w') as f:
        f.write(updated_content)
    
    return next_version

def update_version_with_validation():
    """Update version and validate it worked - clean output"""
    from strategy_config import STRATEGY_VERSION
    original_version = STRATEGY_VERSION
    
    # Update the version
    new_version = update_version()
    
    # Reload to check if it actually changed
    import importlib
    import strategy_config
    importlib.reload(strategy_config)
    actual_version = strategy_config.STRATEGY_VERSION
    
    if original_version == actual_version:
        print_error(f"Version update failed! Version remained unchanged at {original_version}")
        sys.exit(1)  # Clean exit with error code
    
    print_success(f"Version in DEV dir updated: {original_version} -> {actual_version}")
    return actual_version
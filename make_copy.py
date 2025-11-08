"""
Copy files from DEV to DEPLOY directory with version validation
"""
import os
import sys
import shutil
from pathlib import Path
from utils import print_error, print_success, print_warning

def get_deploy_path():
    """Get the DEPLOY directory path"""
    current_dir = Path.cwd()
    parent_dir = current_dir.parent
    return parent_dir / "QC_Trading_Framework_DEPLOY"

def get_version_from_dir(directory):
    """Get version from strategy_config.py in specified directory"""
    try:
        # Save original working directory and sys.path
        original_cwd = os.getcwd()
        original_path = sys.path.copy()
        
        # Change to directory and add to sys.path
        abs_directory = os.path.abspath(directory)
        os.chdir(abs_directory)
        sys.path.insert(0, abs_directory)
        
        # Clear any cached modules
        modules_to_clear = [mod for mod in sys.modules.keys() if mod.startswith('strategy_config')]
        for mod in modules_to_clear:
            del sys.modules[mod]
        
        import strategy_config
        version = strategy_config.STRATEGY_VERSION
        
        # Restore original state
        os.chdir(original_cwd)
        sys.path[:] = original_path
        
        # Clear the module again
        if 'strategy_config' in sys.modules:
            del sys.modules['strategy_config']
            
        return version
    except Exception as e:
        # Restore original state on error
        os.chdir(original_cwd)
        sys.path[:] = original_path
        print_error(f"Failed to get version from {directory}: {e}")
        sys.exit(1)

def copy_files_to_deploy():
    """Copy all necessary files to DEPLOY directory"""
    deploy_path = get_deploy_path()
    
    # Create DEPLOY directory if it doesn't exist
    deploy_path.mkdir(exist_ok=True)
    
    # Files to copy
    files_to_copy = [
        'main.py',
        'active_strategy.py', 
        'strategy_config.py',
        'version_control.py',
        'config.json'
    ]
    
    # Copy individual files
    for file_name in files_to_copy:
        src = Path(file_name)
        if src.exists():
            shutil.copy2(src, deploy_path / file_name)
    
    # Copy framework directory
    framework_src = Path('framework')
    framework_dest = deploy_path / 'framework'
    
    if framework_dest.exists():
        shutil.rmtree(framework_dest)
    if framework_src.exists():
        shutil.copytree(framework_src, framework_dest)
    
    # Copy research.ipynb if it exists
    research_src = Path('research.ipynb')
    if research_src.exists():
        shutil.copy2(research_src, deploy_path / 'research.ipynb')

def validate_version_sync():
    """Validate that DEV and DEPLOY versions match after copy"""
    deploy_path = get_deploy_path()
    
    # Get versions
    dev_version = get_version_from_dir('.')
    deploy_version = get_version_from_dir(str(deploy_path))
    
    if dev_version != deploy_version:
        print_error(f"Version sync failed! DEV: {dev_version}, DEPLOY: {deploy_version}")
        sys.exit(1)
    
    return deploy_version

def main():
    """Main copy function with validation"""
    # Get DEV version before copying
    deploy_path = get_deploy_path()
    
    # Check if DEPLOY exists and get old version for comparison
    old_deploy_version = None
    if (deploy_path / 'strategy_config.py').exists():
        old_deploy_version = get_version_from_dir(str(deploy_path))
    
    # Get current DEV version
    dev_version = get_version_from_dir('.')
    
    # Validate that DEV version is different from old DEPLOY version
    # (This ensures version-update was called and we have something new to deploy)
    if old_deploy_version and dev_version == old_deploy_version:
        print_error(f"DEV and DEPLOY versions are identical ({dev_version}). Run 'make version-update' first.")
        sys.exit(1)
    
    # Copy files
    copy_files_to_deploy()
    
    # Validate version sync after copy (DEV and DEPLOY should now be identical)
    final_version = validate_version_sync()
    
    print_success(f"Files copied to DEPLOY dir with version: {final_version}")

if __name__ == "__main__":
    main()
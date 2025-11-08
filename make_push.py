"""
Push DEPLOY directory to QuantConnect cloud
"""
import os
import sys
import subprocess
from pathlib import Path
from utils import print_error, print_success, print_warning

def get_lean_exe_path():
    """Get the LEAN executable path"""
    return r"C:\Users\chris\pipx\venvs\lean\Scripts\lean.exe"

def get_deploy_path():
    """Get the DEPLOY directory path"""
    current_dir = Path.cwd()
    parent_dir = current_dir.parent
    return parent_dir / "QC_Trading_Framework_DEPLOY"

def validate_deploy_directory():
    """Validate that DEPLOY directory exists and has required files"""
    deploy_path = get_deploy_path()
    
    if not deploy_path.exists():
        print_error("DEPLOY directory does not exist. Run 'make copy' first.")
        sys.exit(1)
    
    required_files = ['main.py', 'active_strategy.py', 'strategy_config.py']
    missing_files = []
    
    for file_name in required_files:
        if not (deploy_path / file_name).exists():
            missing_files.append(file_name)
    
    if missing_files:
        print_error(f"Missing required files in DEPLOY directory: {', '.join(missing_files)}")
        print_warning("Run 'make copy' to ensure all files are present.")
        sys.exit(1)

def get_deploy_version():
    """Get version from DEPLOY directory"""
    try:
        deploy_path = get_deploy_path()
        original_cwd = os.getcwd()
        original_path = sys.path.copy()
        
        # Change to DEPLOY directory
        abs_deploy_path = str(deploy_path.absolute())
        os.chdir(abs_deploy_path)
        sys.path.insert(0, abs_deploy_path)
        
        # Clear module cache
        modules_to_clear = [mod for mod in sys.modules.keys() if mod.startswith('strategy_config')]
        for mod in modules_to_clear:
            del sys.modules[mod]
        
        import strategy_config
        version = strategy_config.STRATEGY_VERSION
        
        # Restore original state
        os.chdir(original_cwd)
        sys.path[:] = original_path
        
        if 'strategy_config' in sys.modules:
            del sys.modules['strategy_config']
            
        return version
    except Exception as e:
        os.chdir(original_cwd)
        sys.path[:] = original_path
        print_error(f"Failed to get version from DEPLOY directory: {e}")
        sys.exit(1)

def push_to_quantconnect():
    """Push DEPLOY directory to QuantConnect cloud"""
    lean_exe = get_lean_exe_path()
    deploy_path = get_deploy_path()
    parent_dir = deploy_path.parent
    
    # Validate LEAN executable exists
    if not Path(lean_exe).exists():
        print_error(f"LEAN executable not found at: {lean_exe}")
        print_warning("Please check your LEAN installation path.")
        sys.exit(1)
    
    try:
        # Change to parent directory and run lean command
        original_cwd = os.getcwd()
        os.chdir(parent_dir)
        
        # Run the lean cloud push command
        result = subprocess.run([
            lean_exe, 
            'cloud', 
            'push', 
            '--project', 
            'QC_Trading_Framework_DEPLOY'
        ], capture_output=True, text=True, timeout=300)
        
        # Restore original directory
        os.chdir(original_cwd)
        
        if result.returncode == 0:
            return result.stdout
        else:
            print_error("QuantConnect push failed!")
            print_error(f"Error output: {result.stderr}")
            if result.stdout:
                print(f"Standard output: {result.stdout}")
            sys.exit(1)
            
    except subprocess.TimeoutExpired:
        os.chdir(original_cwd)
        print_error("QuantConnect push timed out after 5 minutes.")
        sys.exit(1)
    except Exception as e:
        os.chdir(original_cwd)
        print_error(f"Failed to execute QuantConnect push: {e}")
        sys.exit(1)

def verify_deployment(expected_version):
    """Verify deployment by pulling and checking version"""
    print("Verifying deployment by pulling from QuantConnect...")
    
    lean_exe = get_lean_exe_path()
    deploy_path = get_deploy_path()
    parent_dir = deploy_path.parent
    
    try:
        # Change to parent directory and run lean command
        original_cwd = os.getcwd()
        os.chdir(parent_dir)
        
        # Run the lean cloud pull command quietly
        result = subprocess.run([
            lean_exe, 
            'cloud', 
            'pull', 
            '--project', 
            'QC_Trading_Framework_DEPLOY'
        ], capture_output=True, text=True, timeout=180)
        
        # Restore original directory
        os.chdir(original_cwd)
        
        if result.returncode != 0:
            print_warning("Could not verify deployment - pull failed")
            return False
            
        # Check the version from pulled project
        actual_version = get_pulled_version()
        
        if actual_version == expected_version:
            print_success(f"Deployment verified! QuantConnect has version {actual_version}")
            return True
        else:
            print_error(f"Deployment failed: Expected version: {expected_version}, Found version: {actual_version}")
            return False
            
    except subprocess.TimeoutExpired:
        os.chdir(original_cwd)
        print_warning("Deployment verification timed out")
        return False
    except Exception as e:
        os.chdir(original_cwd)
        print_warning(f"Failed to verify deployment: {e}")
        return False

def get_pulled_version():
    """Get version from pulled DEPLOY directory"""
    try:
        deploy_path = get_deploy_path()
        strategy_config_path = deploy_path / "strategy_config.py"
        
        if not strategy_config_path.exists():
            return "Unknown"
        
        # Read the file and extract version
        with open(strategy_config_path, 'r') as f:
            content = f.read()
        
        # Look for STRATEGY_VERSION line
        for line in content.split('\n'):
            if 'STRATEGY_VERSION' in line and '=' in line:
                # Extract version string
                version_part = line.split('=')[1].strip()
                # Remove quotes and whitespace
                version = version_part.strip('"\'')
                return version
        
        return "Unknown"
    except Exception as e:
        return "Unknown"

def main():
    """Main push function"""
    # Validate DEPLOY directory
    validate_deploy_directory()
    
    # Get version being deployed
    version = get_deploy_version()
    print(f"Deploying version {version} to QuantConnect...")
    
    # Push to QuantConnect
    output = push_to_quantconnect()
    
    # Show all QuantConnect output (cleaned up)
    lines = output.split('\n')
    for line in lines:
        if line.strip():  # Only show non-empty lines
            print(f"  {line}")
    
    # Check if push appeared successful
    push_successful = "successfully" in output.lower() or "uploaded" in output.lower()
    
    if push_successful:
        # Verify deployment by pulling and checking version
        if not verify_deployment(version):
            sys.exit(1)
    else:
        print_error(f"Push failed for version {version}")
        sys.exit(1)

if __name__ == "__main__":
    main()

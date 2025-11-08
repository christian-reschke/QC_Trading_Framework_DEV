"""
Pull DEPLOY directory from QuantConnect cloud
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

def validate_lean_installation():
    """Validate that LEAN executable exists"""
    lean_exe = get_lean_exe_path()
    
    if not Path(lean_exe).exists():
        print_error(f"LEAN executable not found at: {lean_exe}")
        print_warning("Please check your LEAN installation path.")
        sys.exit(1)

def pull_from_quantconnect():
    """Pull DEPLOY directory from QuantConnect cloud"""
    lean_exe = get_lean_exe_path()
    deploy_path = get_deploy_path()
    parent_dir = deploy_path.parent
    
    try:
        # Change to parent directory and run lean command
        original_cwd = os.getcwd()
        os.chdir(parent_dir)
        
        # Run the lean cloud pull command
        result = subprocess.run([
            lean_exe, 
            'cloud', 
            'pull', 
            '--project', 
            'QC_Trading_Framework_DEPLOY'
        ], capture_output=True, text=True, timeout=300)
        
        # Restore original directory
        os.chdir(original_cwd)
        
        if result.returncode == 0:
            return result.stdout
        else:
            print_error("QuantConnect pull failed!")
            print_error(f"Error output: {result.stderr}")
            if result.stdout:
                print(f"Standard output: {result.stdout}")
            sys.exit(1)
            
    except subprocess.TimeoutExpired:
        os.chdir(original_cwd)
        print_error("QuantConnect pull timed out after 5 minutes.")
        sys.exit(1)
    except Exception as e:
        os.chdir(original_cwd)
        print_error(f"Failed to execute QuantConnect pull: {e}")
        sys.exit(1)

def get_pulled_version():
    """Get version from pulled DEPLOY directory"""
    try:
        deploy_path = get_deploy_path()
        strategy_config_path = deploy_path / "strategy_config.py"
        
        if not strategy_config_path.exists():
            print_warning("strategy_config.py not found in pulled project")
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
        print_warning(f"Failed to get version from pulled project: {e}")
        return "Unknown"

def validate_pulled_project():
    """Validate that pulled project has required files"""
    deploy_path = get_deploy_path()
    
    if not deploy_path.exists():
        print_error("DEPLOY directory was not created by pull operation")
        return False
    
    required_files = ['main.py', 'active_strategy.py', 'strategy_config.py']
    missing_files = []
    
    for file_name in required_files:
        if not (deploy_path / file_name).exists():
            missing_files.append(file_name)
    
    if missing_files:
        print_warning(f"Pulled project is missing files: {', '.join(missing_files)}")
        return False
    
    return True

def show_project_status():
    """Show status of pulled project"""
    deploy_path = get_deploy_path()
    
    output_string = "Pulled Project Status:"
    
    # Show version
    version = get_pulled_version()
    output_string = output_string + f" Version: {version}"
    
    # Show symbol configuration
    try:
        config_path = deploy_path / "strategy_config.py"
        with open(config_path, 'r') as f:
            content = f.read()
        
        # Extract symbol
        for line in content.split('\n'):
            if 'SYMBOL' in line and '=' in line and not line.strip().startswith('#'):
                symbol_part = line.split('=')[1].strip()
                symbol = symbol_part.strip('"\'')
                output_string = output_string + f", Symbol: {symbol}"
                break
        
        # Extract timeframe
        for line in content.split('\n'):
            if 'TIMEFRAME_MINUTES' in line and '=' in line and not line.strip().startswith('#'):
                timeframe_part = line.split('=')[1].strip()
                output_string = output_string + f", Timeframe: {timeframe_part} minutes"
                break
                
        print(output_string)

    except Exception as e:
        print_warning(f"Could not read configuration: {e}")    

def main():
    """Main pull function"""
    print("Pulling project from QuantConnect...")
    
    # Validate LEAN installation
    validate_lean_installation()
    
    # Pull from QuantConnect
    output = pull_from_quantconnect()
    
    # Show QuantConnect output (cleaned up)
    lines = output.split('\n')
    for line in lines:
        if line.strip():  # Only show non-empty lines
            print(f"  {line}")
    
    # Validate pulled project
    if validate_pulled_project():        
        # Show project status
        show_project_status()

        #version = get_pulled_version()
        #print_success(f"Successfully pulled version {version} from QuantConnect!")
                        
    else:
        print_error("Pulled project validation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()

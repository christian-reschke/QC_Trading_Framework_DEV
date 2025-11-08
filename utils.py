"""
Shared utility functions for the trading framework
"""

def print_red(message):
    """Print message in red color"""
    print(f"\033[91m{message}\033[0m")

def print_green(message):
    """Print message in green color"""
    print(f"\033[92m{message}\033[0m")

def print_yellow(message):
    """Print message in yellow color"""
    print(f"\033[93m{message}\033[0m")

def print_error(message):
    """Print error message in red"""
    print_red(f"ERROR: {message}")

def print_success(message):
    """Print success message in green"""
    print_green(f"SUCCESS: {message}")

def print_warning(message):
    """Print warning message in yellow"""
    print_yellow(f"WARNING: {message}")
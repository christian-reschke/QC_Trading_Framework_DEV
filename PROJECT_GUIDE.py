"""
SPY EMA Strategy Project - Developer Guide
==========================================

This file serves as your practical guide for working with the SPY EMA Crossover Strategy project.
It contains both documentation and runnable utility functions.

LAST UPDATED: November 5, 2025
PROJECT STATUS: DUAL PROJECT STRUCTURE IMPLEMENTED
ARCHITECTURE: Development + Deployment separation

==========================================
DUAL PROJECT STRUCTURE
==========================================

DEVELOPMENT PROJECT: d:\QC\SPY_EMA_Strategy_DEV\
- Complete C# framework with all modules and tests
- Full project history and development files
- Python algorithm development and testing
- Documentation and research files
- Git repository (when restored)

DEPLOYMENT PROJECT: d:\QC\SPY_EMA_Strategy_DEPLOY\
- ONLY essential QuantConnect files (main.py, config.json, research.ipynb)
- Clean project structure for cloud deployment
- No emojis, no special characters, no development artifacts
- Direct push to QuantConnect without conflicts

==========================================
DEPLOYMENT WORKFLOW
==========================================

1. DEVELOP in SPY_EMA_Strategy_DEV:
   - Edit main.py algorithm
   - Test with C# framework
   - Run local simulations
   - Update documentation

2. DEPLOY via SPY_EMA_Strategy_DEPLOY:
   - Copy main.py to deployment project
   - Verify clean encoding (no emojis/special chars)
   - Push to QuantConnect: lean cloud push --project SPY_EMA_Strategy_DEPLOY
   - Run cloud backtest: lean cloud backtest SPY_EMA_Strategy_DEPLOY

3. NAMING CONVENTION:
   - Dev Project: [Strategy]_DEV (full development environment)
   - Deploy Project: [Strategy]_DEPLOY (clean QuantConnect deployment)
   - Cloud Backtest: [Strategy]_[YYYYMMDD]_[Version] (e.g., SPY_EMA_20251105_v1)

==========================================
QUICK START COMMANDS
==========================================
"""

DEPLOY TO QUANTCONNECT:
> cd "d:\QC\Crawling Fluorescent Orange Chinchilla"
> lean cloud push --project .
> lean cloud backtest . --name "SPY_EMA_Strategy_Test"

NOTE: May need to rename directory first due to special characters!

RUN C# UNIT TESTS:
> cd "d:\QC\Crawling Fluorescent Orange Chinchilla\tests"
> dotnet run --project TestRunner.cs

RUN STRATEGY SIMULATION:
> cd "d:\QC\Crawling Fluorescent Orange Chinchilla\strategies" 
> dotnet run --project SPYEMAStrategy.cs

VIEW LATEST BACKTEST:
No actual backtest yet - need to push files first!
Default template ran instead of our SPY EMA strategy.

==========================================
PROJECT STRUCTURE GUIDE
==========================================
"""

import os
from datetime import datetime

# Project Structure Dictionary
PROJECT_STRUCTURE = {
    "CORE ALGORITHM": {
        "main.py": "QuantConnect algorithm - MAIN TRADING LOGIC",
        "config.json": "Project configuration and cloud settings"
    },
    
    "C# FRAMEWORK": {
        "src/framework/interfaces/": "Core interfaces (IEntryModule, IExitModule, etc.)",
        "src/framework/builder/": "Strategy builder pattern",
        "src/framework/metrics/": "Performance calculation (QuickResults)",
        "src/modules/entries/": "Entry signal modules (EMA50Entry, etc.)",
        "src/modules/exits/": "Exit signal modules (EMA100Exit, etc.)",
        "src/modules/sizing/": "Position sizing modules",
        "src/modules/risk/": "Risk management modules"
    },
    
    "TESTING & EXAMPLES": {
        "tests/": "Unit tests and test runner",
        "strategies/": "Example strategies and simulations"
    },
    
    "DOCUMENTATION": {
        "README.html": "Architecture and design documentation",
        "PROJECT_GUIDE.py": "This file - your practical guide!",
        "research.ipynb": "Jupyter notebook for research"
    }
}

def show_project_structure():
    """
    Display the current project structure with descriptions
    """
    print("SPY EMA Strategy Project Structure")
    print("=" * 50)
    
    for category, files in PROJECT_STRUCTURE.items():
        print(f"\n{category}:")
        for file_path, description in files.items():
            exists = "YES" if os.path.exists(file_path) else "NO"
            print(f"   {exists} {file_path}")
            print(f"      {description}")

def show_quick_commands():
    """
    Display the most commonly used commands
    """
    commands = {
        "DEPLOY TO QUANTCONNECT": [
            'cd "d:\\QC\\Crawling Fluorescent Orange Chinchilla"',
            'lean cloud backtest . --name "SPY_EMA_Test_$(Get-Date -Format "MMdd_HHmm")"'
        ],
        
        "RUN ALL TESTS": [
            'cd "d:\\QC\\Crawling Fluorescent Orange Chinchilla"',
            'dotnet run --project tests/TestRunner.cs'
        ],
        
        "RUN STRATEGY SIMULATION": [
            'cd "d:\\QC\\Crawling Fluorescent Orange Chinchilla"',
            'dotnet run --project strategies/SPYEMAStrategy.cs'
        ],
        
        "CHECK CLOUD STATUS": [
            'lean cloud status .'
        ]
    }
    
    print("Quick Commands Reference")
    print("=" * 50)
    
    for title, command_list in commands.items():
        print(f"\n{title}:")
        for cmd in command_list:
            print(f"   > {cmd}")

def current_strategy_summary():
    """
    Print current strategy configuration and latest results
    """
    print("Current Strategy Summary")
    print("=" * 50)
    print("SIGNAL LOGIC:")
    print("   ENTRY: SPY close > EMA50")
    print("   EXIT:  SPY close < EMA100")
    print("   SIZE:  99% allocation")
    print("   RISK:  Basic risk management")
    print()
    print("NO ACTUAL BACKTEST YET!")
    print("   The 30.11% results were from default template")
    print("   Need to push our SPY EMA strategy files first")
    print()
    print("STRATEGY READY TO DEPLOY:")
    print("   ENTRY: SPY close > EMA50") 
    print("   EXIT:  SPY close < EMA100")
    print("   SIZE:  99% allocation")
    print("   RISK:  Basic risk management")
    print()
    print("NEXT: Push files and run real backtest!")

def show_next_steps():
    """
    Display suggested next steps for project development
    """
    print("Suggested Next Steps")
    print("=" * 50)
    print()
    print("IMMEDIATE (This Week):")
    print("   FIRST: Push SPY EMA strategy to QuantConnect!")
    print("   Run real backtest of our strategy")
    print("   Try different EMA periods after initial results")
    print("   Test extended timeframe: 2023-2025")
    print()
    print("SHORT-TERM (This Month):")
    print("   Add stop-loss module")
    print("   Implement volatility-based position sizing")
    print("   Create more entry signal modules")
    print()
    print("MEDIUM-TERM (Next Quarter):")
    print("   Multi-asset strategy (SPY + QQQ + IWM)")
    print("   Machine learning signal enhancement")
    print("   Paper trading deployment")

if __name__ == "__main__":
    """
    Run this file to see the complete project guide
    """
    print("SPY EMA Strategy Project Guide")
    print("=" * 60)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    show_project_structure()
    print("\n")
    show_quick_commands()
    print("\n")
    current_strategy_summary()
    print("\n")
    show_next_steps()
    
    print("\n" + "=" * 60)
    print("TIP: Import this file in other Python scripts to use utility functions")
    print("TIP: Edit this file to add your own notes and shortcuts")
    print("REALITY CHECK: Need to actually push our strategy files first!")
    print("NEXT: Fix directory name issue and deploy for real")
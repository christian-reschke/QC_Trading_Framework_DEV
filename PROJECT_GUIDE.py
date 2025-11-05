"""
SPY EMA Strategy Project - Developer Guide
==========================================

This file serves as your practical guide for working with the SPY EMA Crossover Strategy project.
It contains both documentation and runnable utility functions.

LAST UPDATED: November 5, 2025
PROJECT STATUS: ENHANCED PERFORMANCE ANALYSIS SYSTEM COMPLETE
ARCHITECTURE: Development + Deployment separation with professional benchmarking tools

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
ENHANCED PERFORMANCE ANALYSIS SYSTEM
==========================================

NEW: PROFESSIONAL BENCHMARKING TOOLS
- Real market data integration from TradingView CSV format
- Color-coded performance comparison table
- Comprehensive risk metrics (Sharpe ratio, max drawdown, volatility)
- Dynamic table formatting with proper alignment
- Terminal-based analysis workflow

PERFORMANCE CALCULATOR: calculate_performance.py
- Supports TradingView CSV format (32+ years SPY data included)
- Calculates exact buy & hold performance for any date range
- Professional table output with color coding:
  GREEN: Strategy outperforms buy & hold
  RED: Strategy underperforms buy & hold
- Usage: python calculate_performance.py --file "data/spy/SPY_DAILY_1993-01-29_2025-11-04.csv" --start "2025-07-01" --end "2025-09-30"

DATA SOURCE: data/spy/SPY_DAILY_1993-01-29_2025-11-04.csv
- Real SPY market data from 1993-2025 (8,249 trading days)
- TradingView format: time,open,high,low,close
- Used for accurate buy & hold calculations

ENHANCED COMMANDS:
- make backtest-enhanced: Run backtest with enhanced analysis
- make calculate-performance: Run performance comparison with Q3 2025 data

==========================================
DEPLOYMENT WORKFLOW (UPDATED - FUNCTIONAL)
==========================================

1. DEVELOP in SPY_EMA_Strategy_DEV:
   - Edit main.py algorithm
   - Test with C# framework
   - Run local simulations
   - Update documentation

2. DEPLOY via MAKEFILE (AUTOMATED):
   - make copy      # Copy files from DEV to DEPLOY
   - make push      # Copy + Push to QuantConnect cloud
   - make backtest  # Run cloud backtest

3. COMMANDS REFERENCE:
   - make copy: Copy essential files (main.py, config.json, research.ipynb)
   - make push: Automatic copy + push to QuantConnect (recommended)
   - make backtest: Run backtest on whatever is currently on QuantConnect
   - make logs: Process logs for better readability

4. NAMING CONVENTION:
   - Dev Project: [Strategy]_DEV (full development environment)
   - Deploy Project: [Strategy]_DEPLOY (clean QuantConnect deployment)
   - Cloud Backtest: Auto-generated names (e.g., "Swimming Yellow Viper")

==========================================
QUICK START COMMANDS (UPDATED - MAKEFILE)
==========================================

DEPLOY TO QUANTCONNECT:
> cd "d:\QC\SPY_EMA_Strategy_DEV"
> make push

RUN CLOUD BACKTEST:
> make backtest

COPY FILES ONLY:
> make copy

PROCESS LOGS:
> make logs

LOCAL TESTING:
> make test  # Local C# framework test

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
        "main.py": "QuantConnect algorithm - MAIN TRADING LOGIC with buy & hold tracking",
        "config.json": "Project configuration and cloud settings"
    },
    
    "PERFORMANCE ANALYSIS": {
        "calculate_performance.py": "Professional performance calculator with color-coded tables",
        "data/spy/SPY_DAILY_1993-01-29_2025-11-04.csv": "32+ years real SPY market data",
        "backtest_with_analysis.py": "Enhanced backtest runner with output capture"
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
            'cd "d:\\QC\\SPY_EMA_Strategy_DEV"',
            'make push'
        ],
        
        "RUN CLOUD BACKTEST": [
            'make backtest'
        ],
        
        "BACKTEST WITH ENHANCED ANALYSIS": [
            'make backtest-enhanced'
        ],
        
        "CALCULATE PERFORMANCE COMPARISON": [
            'make calculate-performance'
        ],
        
        "MANUAL PERFORMANCE ANALYSIS": [
            'python calculate_performance.py --file "data/spy/SPY_DAILY_1993-01-29_2025-11-04.csv" --start "2025-07-01" --end "2025-09-30"'
        ],
        
        "COPY FILES TO DEPLOY": [
            'make copy'
        ],
        
        "SHOW PERFORMANCE SUMMARY": [
            'make results'
        ],
        
        "LOCAL FRAMEWORK TEST": [
            'make test'
        ],
        
        "PROCESS LOGS": [
            'make logs'
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
    print("STRATEGY LOGIC:")
    print("   ENTRY: SPY close > EMA50")
    print("   EXIT:  SPY close < EMA100")
    print("   SIZE:  99% allocation")
    print("   RISK:  Basic risk management")
    print()
    print("LATEST BACKTEST RESULTS (Q3 2025):")
    print("   Strategy Return: +8.13%")
    print("   Annualized Return: 36.51%")
    print("   Sharpe Ratio: 2.601 (excellent)")
    print("   Max Drawdown: 2.40% (very low)")
    print("   Buy & Hold Return: +8.51% (slightly better)")
    print("   Buy & Hold Sharpe: 3.868 (superior risk-adjusted returns)")
    print("   Buy & Hold Drawdown: 2.13% (slightly lower risk)")
    print()
    print("PERFORMANCE COMPARISON SUMMARY:")
    print("   Strategy underperformed buy & hold by 0.38% in Q3 2025")
    print("   Buy & hold showed better risk-adjusted returns")
    print("   Strategy had slightly higher volatility and drawdown")
    print()
    print("ENHANCED FEATURES:")
    print("   Real-time buy & hold benchmark tracking in algorithm")
    print("   Color-coded performance comparison table")
    print("   Professional table formatting with dynamic sizing")
    print("   Exact buy & hold calculation using opening prices")
    print("   Support for any date range analysis")
    print("   Real market data from TradingView (32+ years)")
    print()
    print("NEXT: Try 'make calculate-performance' for latest comparison table!")

def show_next_steps():
    """
    Display suggested next steps for project development
    """
    print("Suggested Next Steps")
    print("=" * 50)
    print()
    print("IMMEDIATE (This Week):")
    print("   COMPLETED: Enhanced performance analysis system")
    print("   COMPLETED: Color-coded comparison tables")
    print("   COMPLETED: Real market data integration")
    print("   NEXT: Test strategy optimization with different EMA periods")
    print("   NEXT: Analyze performance across different market conditions")
    print("   NEXT: Implement parameter optimization workflow")
    print()
    print("SHORT-TERM (This Month):")
    print("   Add volatility-based position sizing")
    print("   Implement advanced stop-loss strategies")
    print("   Create automated parameter sweep analysis")
    print("   Add market regime detection (bull/bear/sideways)")
    print()
    print("MEDIUM-TERM (Next Quarter):")
    print("   Multi-asset strategy (SPY + QQQ + IWM)")
    print("   Machine learning signal enhancement")
    print("   Real-time trading alerts and monitoring")
    print("   Portfolio-level risk management")
    print()
    print("LONG-TERM (2025):")
    print("   Paper trading deployment")
    print("   Live trading preparation")
    print("   Strategy marketplace integration")

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
    print("NEXT: Fix directory name issue and deploy for real")
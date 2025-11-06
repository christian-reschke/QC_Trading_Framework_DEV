#!/usr/bin/env python3
"""
Enhanced backtest runner that captures and displays performance comparison
"""

import subprocess
import re
import sys
import os
from datetime import datetime

def run_backtest_with_capture():
    """
    Run the backtest and try to capture output for analysis
    """
    print("Running backtest with performance capture...")
    
    try:
        # Get project paths
        current_dir = os.getcwd()
        parent_dir = os.path.dirname(current_dir)
        project_name = os.path.basename(current_dir)
        deploy_name = project_name.replace('_DEV', '_DEPLOY')
        
        # Change to parent directory for lean command
        os.chdir(parent_dir)
        
        # Run the lean backtest command
        lean_exe = r"C:\Users\chris\pipx\venvs\lean\Scripts\lean.exe"
        cmd = [lean_exe, "cloud", "backtest", deploy_name]
        
        # Run the lean backtest command with live output
        print(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, text=True, timeout=300)
        
        # Since we can't easily capture the URL with live output,
        # we'll let the user see the URL in the live output
        backtest_url = None
        
        # Change back to original directory
        os.chdir(current_dir)
        
        return result.returncode == 0, backtest_url
        
    except subprocess.TimeoutExpired:
        print("ERROR: Backtest timed out after 5 minutes")
        return False, None
    except Exception as e:
        print(f"ERROR: Error running backtest: {e}")
        return False, None

def extract_performance_from_output(output_text):
    """
    Extract the actual performance comparison from algorithm logs
    """
    performance_data = {}
    
    # Look for our custom performance comparison section
    lines = output_text.split('\n')
    in_comparison_section = False
    
    for line in lines:
        if "BACKTEST COMPLETE - PERFORMANCE COMPARISON" in line:
            in_comparison_section = True
            continue
            
        if in_comparison_section and line.strip().startswith('='):
            in_comparison_section = False
            break
            
        if in_comparison_section:
            # Extract strategy performance
            if "Final Portfolio Value:" in line:
                match = re.search(r'\$([0-9,]+)', line)
                if match:
                    performance_data['strategy_final'] = match.group(1).replace(',', '')
            
            elif "Total Return:" in line and "STRATEGY" in lines[lines.index(line)-3:lines.index(line)]:
                match = re.search(r'([0-9.]+)%', line)
                if match:
                    performance_data['strategy_return'] = float(match.group(1))
            
            # Extract buy & hold performance
            elif "SPY Start Price:" in line:
                match = re.search(r'\$([0-9.]+)', line)
                if match:
                    performance_data['spy_start'] = float(match.group(1))
                    
            elif "SPY End Price:" in line:
                match = re.search(r'\$([0-9.]+)', line)
                if match:
                    performance_data['spy_end'] = float(match.group(1))
                    
            elif "Buy & Hold Return:" in line:
                match = re.search(r'([0-9.-]+)%', line)
                if match:
                    performance_data['buy_hold_return'] = float(match.group(1))
                    
            elif "Buy & Hold Final Value:" in line:
                match = re.search(r'\$([0-9,]+)', line)
                if match:
                    performance_data['buy_hold_final'] = match.group(1).replace(',', '')
            
            # Extract outperformance
            elif "OUTPERFORMED by" in line:
                match = re.search(r'([0-9.]+)%', line)
                if match:
                    performance_data['outperformance'] = float(match.group(1))
                    performance_data['outperformed'] = True
                    
            elif "UNDERPERFORMED by" in line:
                match = re.search(r'([0-9.]+)%', line)
                if match:
                    performance_data['outperformance'] = -float(match.group(1))
                    performance_data['outperformed'] = False
                    
            # Extract trading statistics
            elif "Trading Days:" in line:
                match = re.search(r'([0-9]+)', line)
                if match:
                    performance_data['trading_days'] = int(match.group(1))
                    
            elif "Annualized Strategy Return:" in line:
                match = re.search(r'([0-9.-]+)%', line)
                if match:
                    performance_data['annualized_strategy'] = float(match.group(1))
                    
            elif "Annualized Buy & Hold Return:" in line:
                match = re.search(r'([0-9.-]+)%', line)
                if match:
                    performance_data['annualized_buy_hold'] = float(match.group(1))
    
    return performance_data

def display_real_performance_comparison(performance_data):
    """
    Display the actual calculated performance comparison
    """
    print("\n" + "="*70)
    print("ACTUAL PERFORMANCE COMPARISON (FROM ALGORITHM)")
    print("="*70)
    
    if not performance_data:
        print("ERROR: Could not extract performance data from logs")
        print("   The detailed comparison should be in the QuantConnect logs")
        return
    
    print(f"\nSTRATEGY PERFORMANCE:")
    if 'strategy_final' in performance_data:
        print(f"   Final Portfolio Value: ${performance_data['strategy_final']:,}")
    if 'strategy_return' in performance_data:
        print(f"   Total Return: {performance_data['strategy_return']:.2f}%")
    
    print(f"\nBUY & HOLD BENCHMARK:")
    if 'spy_start' in performance_data and 'spy_end' in performance_data:
        print(f"   SPY Start Price: ${performance_data['spy_start']:.2f}")
        print(f"   SPY End Price: ${performance_data['spy_end']:.2f}")
    if 'buy_hold_return' in performance_data:
        print(f"   Buy & Hold Return: {performance_data['buy_hold_return']:.2f}%")
    if 'buy_hold_final' in performance_data:
        print(f"   Buy & Hold Final Value: ${performance_data['buy_hold_final']:,}")
    
    print(f"\nCOMPARISON RESULTS:")
    if 'outperformance' in performance_data:
        if performance_data.get('outperformed', False):
            print(f"   SUCCESS: Strategy OUTPERFORMED by {performance_data['outperformance']:.2f}%")
        else:
            print(f"   RESULT: Strategy UNDERPERFORMED by {abs(performance_data['outperformance']):.2f}%")
    
    if 'trading_days' in performance_data:
        print(f"\nTRADING STATISTICS:")
        print(f"   Trading Days: {performance_data['trading_days']}")
        
        if 'annualized_strategy' in performance_data:
            print(f"   Annualized Strategy Return: {performance_data['annualized_strategy']:.2f}%")
        if 'annualized_buy_hold' in performance_data:
            print(f"   Annualized Buy & Hold Return: {performance_data['annualized_buy_hold']:.2f}%")
    
    print("="*70)

if __name__ == "__main__":
    success, url = run_backtest_with_capture()
    
    # Automatically run performance analysis using our CSV data
    if success:
        print("\n" + "="*70)
        print("PERFORMANCE ANALYSIS")
        print("="*70)
        
        # Import and run the performance calculator
        try:
            from calculate_performance import calculate_performance_from_file, compare_with_strategy
            
            # Use clean 2024 period matching strategy settings
            file_path = "data/spy/SPY_DAILY_1993-01-29_2025-11-04.csv"
            start_date = "2024-01-01"  # Clean 12-month period
            end_date = "2024-12-31"
            starting_capital = 100000   # Match $100K from QuantConnect
            
            print(f"Calculating buy & hold performance for period: {start_date} to {end_date}")
            print(f"Starting capital: ${starting_capital:,} (matching QuantConnect)")
            
            buy_hold_data = calculate_performance_from_file(file_path, start_date, end_date, starting_capital)
            if buy_hold_data:
                compare_with_strategy(buy_hold_data)
            else:
                print("ERROR: Could not calculate performance comparison")
                
        except Exception as e:
            print(f"ERROR: Error running performance analysis: {e}")
            print("You can run manually with: make calculate-performance")
        
        print("="*70)
#!/usr/bin/env python3
"""
Enhanced backtest runner that captures and displays performance comparison
"""

import subprocess
import re
import sys
import os
import glob
from datetime import datetime
from utils import print_error, print_warning

def find_symbol_data_file(symbol):
    """
    Find the data file for a given symbol, looking for any daily data file
    Returns the path to the first matching file found
    """
    data_dir = f"data/{symbol.lower()}"
    if not os.path.exists(data_dir):
        print_error(f"Data directory not found: {data_dir}")
        return None
    
    # Look for any daily data file for this symbol
    pattern = f"{data_dir}/{symbol}_DAILY_*.csv"
    matching_files = glob.glob(pattern)
    
    if not matching_files:
        print_error(f"No daily data files found for {symbol} in {data_dir}")
        return None
    
    # Return the first matching file (should usually be only one)
    return matching_files[0]

def parse_backtest_results(output_text):
    """
    Parse actual backtest results from QuantConnect output
    """
    from strategy_config import SYMBOL
    strategy_metrics = {}
    
    # Parse deployed version from QC output
    version_match = re.search(r'STRATEGY_VERSION:\s*([^\s\n]+)', output_text)
    if not version_match:
        # Try parsing from runtime statistics table format
        version_match = re.search(r'\|\s*Strategy Version\s*\|\s*([^\s|]+)', output_text)
    if version_match:
        strategy_metrics['deployed_version'] = version_match.group(1).strip()
    
    # Split into lines and look for specific patterns
    lines = output_text.split('\n')
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Debug: print lines that contain key metrics (commented out to reduce noise)
        # if any(keyword in line for keyword in ['Return', 'Sharpe', 'Drawdown', 'Equity']):
        #     print(f"DEBUG LINE: {line}")
        
        # Look for Return line in right column - pattern: "| Probabilistic | 75.995% | Return | 24.26 % |"
        if '| Return' in line and '%' in line:
            # Split by pipe and find the section with "Return"
            parts = line.split('|')
            for i, part in enumerate(parts):
                if 'Return' in part and i + 1 < len(parts):
                    # Get the next part which should contain the percentage
                    value_part = parts[i + 1].strip()
                    match = re.search(r'(\d+\.\d+)\s*%', value_part)
                    if match:
                        return_val = float(match.group(1)) / 100
                        strategy_metrics['return'] = return_val
                        # print(f"DEBUG: Found return = {return_val} from part: '{value_part}'")
                        break
        
        # Look for Sharpe Ratio in right column - pattern: "| Net Profit | 24.263% | Sharpe Ratio | 1.162 |"
        elif '| Sharpe Ratio' in line:
            # Split by pipe and find the section with "Sharpe Ratio"
            parts = line.split('|')
            for i, part in enumerate(parts):
                if 'Sharpe Ratio' in part and i + 1 < len(parts):
                    # Get the next part which should contain the decimal value
                    value_part = parts[i + 1].strip()
                    match = re.search(r'(\d+\.\d+)', value_part)
                    if match:
                        sharpe_val = float(match.group(1))
                        strategy_metrics['sharpe'] = sharpe_val
                        # print(f"DEBUG: Found sharpe = {sharpe_val} from part: '{value_part}'")
                        break
        
        # Look for Drawdown percentage
        elif '| Drawdown' in line and '%' in line:
            match = re.search(r'(\d+\.\d+)\s*%', line)
            if match:
                drawdown_val = float(match.group(1)) / 100
                strategy_metrics['drawdown'] = drawdown_val
                # print(f"DEBUG: Found drawdown = {drawdown_val}")
        
        # Look for Equity value
        elif '| Equity' in line and '$' in line:
            match = re.search(r'\$([0-9,]+\.[0-9]+)', line)
            if match:
                equity_str = match.group(1).replace(',', '')
                strategy_metrics['final_value'] = float(equity_str)
        
        # Look for Start Equity
        elif '| Start Equity' in line:
            match = re.search(r'(\d+)', line)
            if match:
                strategy_metrics['start_value'] = float(match.group(1))
    
    # Final debug output (commented out to reduce noise)
    # print(f"DEBUG: Final parsed strategy metrics: {strategy_metrics}")
    
    return strategy_metrics

def run_backtest_with_capture():
    """
    Run the backtest and capture output for analysis
    """
    
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
        
        # Run the lean backtest command and capture output
        print(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, text=True, capture_output=True, timeout=300)
        
        # Print the output for user to see (commented out to reduce terminal noise)
        # print(result.stdout)
        if result.stderr:
            print("  STDERR:", result.stderr)
        
        # Change back to original directory
        os.chdir(current_dir)
        
        # Parse the actual performance results from output
        strategy_metrics = parse_backtest_results(result.stdout)
        
        return result.returncode == 0, None, strategy_metrics
        
    except subprocess.TimeoutExpired:
        print_error("Backtest timed out after 5 minutes")
        return False, None, None
    except Exception as e:
        print_error(f"Error running backtest: {e}")
        return False, None, None

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
            elif f"{SYMBOL} Start Price:" in line:
                match = re.search(r'\$([0-9.]+)', line)
                if match:
                    performance_data['symbol_start'] = float(match.group(1))
                    
            elif f"{SYMBOL} End Price:" in line:
                match = re.search(r'\$([0-9.]+)', line)
                if match:
                    performance_data['symbol_end'] = float(match.group(1))
                    
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
    print("="*70)
    print("ACTUAL PERFORMANCE COMPARISON (FROM ALGORITHM)")
    print("="*70)
    
    if not performance_data:
        print_error("Could not extract performance data from logs")
        print("   The detailed comparison should be in the QuantConnect logs")
        return
    
    print(f"\nSTRATEGY PERFORMANCE:")
    if 'strategy_final' in performance_data:
        print(f"   Final Portfolio Value: ${performance_data['strategy_final']:,}")
    if 'strategy_return' in performance_data:
        print(f"   Total Return: {performance_data['strategy_return']:.2f}%")
    
    print(f"\nBUY & HOLD BENCHMARK:")
    if 'symbol_start' in performance_data and 'symbol_end' in performance_data:
        from strategy_config import SYMBOL
        print(f"   {SYMBOL} Start Price: ${performance_data['symbol_start']:.2f}")
        print(f"   {SYMBOL} End Price: ${performance_data['symbol_end']:.2f}")
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
    success, url, strategy_metrics = run_backtest_with_capture()
    
    # Automatically run performance analysis using our CSV data
    if success:
        # Get deployed version for display
        deployed_version = strategy_metrics.get('deployed_version', 'unknown')
        
        print("="*70)
        print(f"PERFORMANCE ANALYSIS ({deployed_version})")
        print("-"*70)
        
        # Import and run the performance calculator
        try:
            from calculate_performance import calculate_performance_from_file, compare_with_strategy
            # Import configuration from safe config file (no security risk)
            from strategy_config import SYMBOL, TIMEFRAME_MINUTES, START_DATE, END_DATE, STARTING_CAPITAL
            
            # Get timeframe for dynamic labeling
            timeframe_label = "Strategy"
            
            # Use centralized period configuration matching strategy settings
            file_path = find_symbol_data_file(SYMBOL)
            start_date = START_DATE  # From centralized config
            end_date = END_DATE      # From centralized config
            starting_capital = STARTING_CAPITAL   # From centralized config
            
            print(f"Symbol:\t\t\t{SYMBOL}")
            print(f"Timeframe:\t\t{TIMEFRAME_MINUTES}min")
            print(f"Starting capital:\t${starting_capital:,}")
            print(f"Time range:\t\t{start_date} to {end_date}")
            print("=" * 70)
            buy_hold_data = calculate_performance_from_file(file_path, start_date, end_date, starting_capital)
            
            if buy_hold_data and strategy_metrics:
                # Use actual backtest results - NO fallbacks
                actual_return = strategy_metrics.get('return')
                actual_sharpe = strategy_metrics.get('sharpe') 
                actual_drawdown = strategy_metrics.get('drawdown')
                
                if actual_return is not None and actual_sharpe is not None and actual_drawdown is not None:
                    compare_with_strategy(buy_hold_data, actual_return, actual_sharpe, actual_drawdown, timeframe_label)
                else:
                    print_error("Could not parse strategy metrics from backtest output")
                    print("Missing metrics:", [k for k in ['return', 'sharpe', 'drawdown'] if strategy_metrics.get(k) is None])
                    print("Parsed metrics:", strategy_metrics)
            else:
                print_error("Could not calculate performance comparison - missing data")
                if not buy_hold_data:
                    print("  - Failed to calculate buy & hold data")
                    print_warning(f"To compare your strategy results to the buy and hold benchmark,")
                    print(f"         put a TradingView data file into folder: data/{SYMBOL.lower()}/")
                    print(f"         Expected file: {file_path}")
                if not strategy_metrics:
                    print("  - Failed to parse strategy metrics")
                
        except Exception as e:
            print_error(f"Error running performance analysis: {e}")
            print("You can run manually with: make calculate-performance")
        
        print("="*70)
"""
Simple table formatting test
"""
import glob
import os
from calculate_performance import calculate_performance_from_file, compare_with_strategy
from strategy_config import SYMBOL, TIMEFRAME_MINUTES, START_DATE, END_DATE, STARTING_CAPITAL
from mock_backtest import get_mock_strategy_metrics

def find_symbol_data_file(symbol):
    """
    Find the data file for a given symbol, looking for any daily data file
    Returns the path to the first matching file found
    """
    data_dir = f"data/{symbol.lower()}"
    if not os.path.exists(data_dir):
        print(f"ERROR: Data directory not found: {data_dir}")
        return None
    
    # Look for any daily data file for this symbol
    pattern = f"{data_dir}/{symbol}_DAILY_*.csv"
    matching_files = glob.glob(pattern)
    
    if not matching_files:
        print(f"ERROR: No daily data files found for {symbol} in {data_dir}")
        return None
    
    # Return the first matching file (should usually be only one)
    return matching_files[0]

def test_table_only():
    """Test just the table formatting"""
    
    print("Testing table formatting...")
    print()
    
    # Get mock data
    strategy_metrics = get_mock_strategy_metrics()
    
    # Get buy hold data
    file_path = find_symbol_data_file(SYMBOL)
    buy_hold_data = calculate_performance_from_file(file_path, START_DATE, END_DATE, STARTING_CAPITAL)
    
    if buy_hold_data and strategy_metrics:
        actual_return = strategy_metrics.get('return')
        actual_sharpe = strategy_metrics.get('sharpe') 
        actual_drawdown = strategy_metrics.get('drawdown')
        
        print("=" * 70)
        compare_with_strategy(buy_hold_data, actual_return, actual_sharpe, actual_drawdown, "Strategy")
        print("=" * 70)
    else:
        print("ERROR: Could not load test data")

if __name__ == "__main__":
    test_table_only()
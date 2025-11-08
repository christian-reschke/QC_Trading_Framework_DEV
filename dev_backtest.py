"""
Development backtest runner using mock data for testing table formatting
"""
import sys
import os
import glob
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

def main():
    """Main mock backtest function for development"""
    print("Running MOCK backtest for development...")
    
    # Import mock data
    from mock_backtest import run_mock_backtest
    
    # Get mock backtest results
    success, url, strategy_metrics = run_mock_backtest()
    
    if success:
        # Get deployed version for display
        deployed_version = strategy_metrics.get('deployed_version', 'unknown')
        
        print("\n" + "="*70)
        print(f"PERFORMANCE ANALYSIS ({deployed_version})")
        print("-" * 70)
        
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

if __name__ == "__main__":
    main()
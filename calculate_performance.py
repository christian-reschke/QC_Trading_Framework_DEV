#!/usr/bin/env python3
"""
Calculate buy & hold performance from SPY price data directly
This bypasses the need to parse logs - we calculate it ourselves with real data
"""

from datetime import datetime, date
import sys
import os
import csv

def read_spy_data_from_csv(file_path):
    """
    Read SPY price data from CSV file
    Supports both standard format (Date,Open,High,Low,Close,Volume) 
    and TradingView format (time,open,high,low,close)
    """
    data = []
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
        
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            
            # Check the format by looking at column names
            fieldnames = reader.fieldnames
            
            # TradingView format (lowercase)
            if 'time' in fieldnames and 'close' in fieldnames:
                for row in reader:
                    data.append({
                        'date': row['time'],
                        'open': float(row['open']),
                        'high': float(row['high']),
                        'low': float(row['low']),
                        'close': float(row['close']),
                        'volume': 0  # TradingView doesn't include volume
                    })
            
            # Standard format (uppercase)
            elif 'Date' in fieldnames and 'Close' in fieldnames:
                for row in reader:
                    data.append({
                        'date': row['Date'],
                        'open': float(row['Open']),
                        'high': float(row['High']),
                        'low': float(row['Low']),
                        'close': float(row['Close']),
                        'volume': int(row.get('Volume', 0))
                    })
            
            else:
                return None
                
        return data
        
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def get_price_for_date_range(data, start_date, end_date):
    """
    Get start and end prices for a specific date range
    Uses OPENING price of start date and CLOSING price of end date
    (this reflects actual buy & hold trading - buy at open, value at close)
    """
    if not data:
        return None, None
        
    start_price = None
    end_price = None
    
    # Find prices for the date range
    for row in data:
        # Use opening price of the start date (when you would actually buy)
        if row['date'] >= start_date and start_price is None:
            start_price = row['open']  # Changed from 'close' to 'open'
            
        # Use closing price of the end date (final value)
        if row['date'] <= end_date:
            end_price = row['close']
            
    return start_price, end_price

def calculate_performance_metrics(data, start_date=None, end_date=None):
    """
    Calculate comprehensive performance metrics including drawdown and Sharpe ratio
    """
    if not data:
        return None
    
    # Filter data for date range if specified
    filtered_data = []
    if start_date and end_date:
        for row in data:
            if start_date <= row['date'] <= end_date:
                filtered_data.append(row)
    else:
        filtered_data = data
    
    if len(filtered_data) < 2:
        return None
    
    # Calculate daily returns
    daily_returns = []
    prices = [row['close'] for row in filtered_data]
    
    for i in range(1, len(prices)):
        daily_return = (prices[i] - prices[i-1]) / prices[i-1]
        daily_returns.append(daily_return)
    
    # Calculate maximum drawdown
    peak = prices[0]
    max_drawdown = 0
    
    for price in prices:
        if price > peak:
            peak = price
        drawdown = (peak - price) / peak
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    # Calculate Sharpe ratio (assuming risk-free rate of 2% annually)
    risk_free_rate = 0.02 / 252  # Daily risk-free rate
    excess_returns = [r - risk_free_rate for r in daily_returns]
    
    if len(excess_returns) > 1:
        import math
        mean_excess = sum(excess_returns) / len(excess_returns)
        variance = sum((r - mean_excess) ** 2 for r in excess_returns) / (len(excess_returns) - 1)
        std_dev = math.sqrt(variance)
        sharpe_ratio = (mean_excess / std_dev) * math.sqrt(252) if std_dev > 0 else 0
    else:
        sharpe_ratio = 0
    
    return {
        'max_drawdown': max_drawdown,
        'sharpe_ratio': sharpe_ratio,
        'daily_returns': daily_returns,
        'volatility': math.sqrt(variance * 252) if len(excess_returns) > 1 else 0
    }

def calculate_performance_from_file(file_path, start_date=None, end_date=None):
    """
    Calculate performance from CSV data file
    Uses opening price of start date and closing price of end date
    """
    data = read_spy_data_from_csv(file_path)
    if not data:
        return None
        
    if start_date and end_date:
        start_price, end_price = get_price_for_date_range(data, start_date, end_date)
    else:
        # Use opening price of first day and closing price of last day
        start_price = data[0]['open']
        end_price = data[-1]['close']
    
    if start_price and end_price:
        # Calculate basic performance
        basic_performance = calculate_performance_from_prices(start_price, end_price)
        
        # Calculate additional metrics
        metrics = calculate_performance_metrics(data, start_date, end_date)
        
        if basic_performance and metrics:
            basic_performance.update(metrics)
        
        return basic_performance
    else:
        return None

def calculate_performance_from_prices(start_price, end_price, initial_capital=1000000):
    """
    Calculate buy & hold performance given start and end prices
    """
    if start_price <= 0 or end_price <= 0:
        return None
        
    allocation = 0.99  # 99% allocation like our strategy
    investment = initial_capital * allocation
    shares = investment / start_price
    final_value = shares * end_price
    
    buy_hold_return = (final_value - investment) / investment
    
    return {
        'start_price': start_price,
        'end_price': end_price,
        'shares': shares,
        'investment': investment,
        'final_value': final_value,
        'return': buy_hold_return
    }

def compare_with_strategy(buy_hold_data, strategy_return=0.0813, strategy_sharpe=2.601, strategy_drawdown=0.024):
    """
    Compare buy & hold with strategy performance in clean table format
    """
    if not buy_hold_data:
        return
    
    # ANSI color codes
    GREEN = '\033[92m'  # Bright green for better performance
    RED = '\033[91m'    # Bright red for worse performance
    RESET = '\033[0m'   # Reset to default color
    
    # Define table structure based on first column width
    col1_width = 21  # "│ Metric              │" = 21 chars
    col_width = max(15, col1_width - 4)  # min. 15
    
    # Create dynamic borders based on column widths
    border_top = f"┌{'─' * col1_width}┬{'─' * col_width}┬{'─' * col_width}┐"
    border_mid = f"├{'─' * col1_width}┼{'─' * col_width}┼{'─' * col_width}┤"
    border_bot = f"└{'─' * col1_width}┴{'─' * col_width}┴{'─' * col_width}┘"
    
    # Headers with proper padding
    header_col2 = "Buy & Hold".center(col_width - 1) + " "
    header_col3 = "Strategy".center(col_width - 1) + " "
    
    # Just the table with proper padding
    print(border_top)
    print(f"│ Metric              │{header_col2}│{header_col3}│")
    print(border_mid)
    
    # Start Value
    start_value = 1000000
    bh_start = f"$ {start_value:,.0f} ".rjust(col_width)
    strategy_start = f"$ {start_value:,.0f} ".rjust(col_width)
    print(f"│ Start Value         │{bh_start}│{strategy_start}│")
    
    # Final Value
    bh_final = buy_hold_data['final_value']
    strategy_final = 1000000 * (1 + strategy_return)
    bh_final_str = f"$ {bh_final:,.0f} ".rjust(col_width)
    strategy_final_str = f"$ {strategy_final:,.0f} ".rjust(col_width)
    print(f"│ Final Value         │{bh_final_str}│{strategy_final_str}│")
    
    # Return
    bh_return = buy_hold_data['return']
    bh_return_str = f"{bh_return:.2%} ".rjust(col_width)
    
    # Color strategy return based on performance vs buy & hold
    strategy_color = GREEN if strategy_return > bh_return else RED
    strategy_return_str = f"{strategy_color}{strategy_return:.2%} {RESET}".rjust(col_width + len(strategy_color) + len(RESET))
    print(f"│ Return              │{bh_return_str}│{strategy_return_str}│")
    
    # Max Drawdown (lower is better)
    bh_drawdown = buy_hold_data.get('max_drawdown', 0)
    bh_dd_str = f"{bh_drawdown:.2%} ".rjust(col_width)
    
    # Color strategy drawdown (lower is better, so reverse logic)
    drawdown_color = GREEN if strategy_drawdown < bh_drawdown else RED
    strategy_dd_str = f"{drawdown_color}{strategy_drawdown:.2%} {RESET}".rjust(col_width + len(drawdown_color) + len(RESET))
    print(f"│ Max Drawdown        │{bh_dd_str}│{strategy_dd_str}│")
    
    # Sharpe Ratio (higher is better)
    bh_sharpe = buy_hold_data.get('sharpe_ratio', 0)
    bh_sharpe_str = f"{bh_sharpe:.3f} ".rjust(col_width)
    
    # Color strategy Sharpe ratio
    sharpe_color = GREEN if strategy_sharpe > bh_sharpe else RED
    strategy_sharpe_str = f"{sharpe_color}{strategy_sharpe:.3f} {RESET}".rjust(col_width + len(sharpe_color) + len(RESET))
    print(f"│ Sharpe Ratio        │{bh_sharpe_str}│{strategy_sharpe_str}│")
    
    print(border_bot)

if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) >= 2:
        # Check for file-based calculation
        if sys.argv[1] == '--file' and len(sys.argv) >= 3:
            file_path = sys.argv[2]
            start_date = None
            end_date = None
            
            # Check for date range arguments
            if len(sys.argv) >= 6 and sys.argv[3] == '--start' and sys.argv[5] == '--end':
                start_date = sys.argv[4]
                end_date = sys.argv[6]
            elif len(sys.argv) >= 4 and sys.argv[3] == '--start':
                start_date = sys.argv[4]
            elif len(sys.argv) >= 4 and sys.argv[3] == '--end':
                end_date = sys.argv[4]
            
            buy_hold_data = calculate_performance_from_file(file_path, start_date, end_date)
            if buy_hold_data:
                compare_with_strategy(buy_hold_data)
        
        # Direct price calculation
        elif len(sys.argv) == 3:
            try:
                start_price = float(sys.argv[1])
                end_price = float(sys.argv[2])
                
                buy_hold_data = calculate_performance_from_prices(start_price, end_price)
                compare_with_strategy(buy_hold_data)
                
            except ValueError:
                print("Invalid price values provided")
    else:
        # Default: run Q3 2025 analysis
        file_path = "data/spy/SPY_DAILY_1993-01-29_2025-11-04.csv"
        start_date = "2025-07-01"
        end_date = "2025-09-30"
        
        buy_hold_data = calculate_performance_from_file(file_path, start_date, end_date)
        if buy_hold_data:
            compare_with_strategy(buy_hold_data)
        else:
            print("ERROR: Could not calculate performance comparison")
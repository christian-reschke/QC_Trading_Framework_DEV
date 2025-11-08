"""
Test script to reproduce zero value parsing issues
"""
from utils import QCOutputParser

# Create test output with zero values (from the 1-day backtest)
zero_values_output = """Started compiling project 'QC_Trading_Framework_DEPLOY'
Build Request Successful for Project ID: 26025124, with CompileID:
4ba20836df5fb58e7b7e151371171b70-6443afc94a19947d280ef2b9af425d48, Lean
Version: 2.5.0.0.17369
Successfully compiled project 'QC_Trading_Framework_DEPLOY'
Started backtest named 'Crawling Brown Badger' for project
'QC_Trading_Framework_DEPLOY'
Backtest url:
https://www.quantconnect.com/project/26025124/ff008bb7776bbf4ba315a74d03cf4487
 ---------------------------------------- 100%
+-----------------------------------------------------------------------------+
| Statistic                | Value       | Statistic                 | Value  |
|--------------------------+-------------+---------------------------+--------|
| Equity                   | $100,000.00 | Fees                      | -$0.00 |
| Holdings                 | $0.00       | Net Profit                | $0.00  |
| Probabilistic Sharpe     | 0%          | Return                    | 0.00 % |
| Ratio                    |             |                           |        |
| Strategy Version         | v2.1.65     | Unrealized                | $0.00  |
| Volume                   | $0.00       |                           |        |
|--------------------------+-------------+---------------------------+--------|
| Total Orders             | 0           | Average Win               | 0%     |
| Average Loss             | 0%          | Compounding Annual Return | 0%     |
| Drawdown                 | 0%          | Expectancy                | 0      |
| Start Equity             | 100000      | End Equity                | 100000 |
| Net Profit               | 0%          | Sharpe Ratio              | 0      |
| Sortino Ratio            | 0           | Probabilistic Sharpe      | 0%     |
|                          |             | Ratio                     |        |
| Loss Rate                | 0%          | Win Rate                  | 0%     |
| Profit-Loss Ratio        | 0           | Alpha                     | 0      |
| Beta                     | 0           | Annual Standard Deviation | 0      |
| Annual Variance          | 0           | Information Ratio         | -1.647 |
| Tracking Error           | 0.105       | Treynor Ratio             | 0      |
| Total Fees               | $0.00       | Estimated Strategy        | $0     |
|                          |             | Capacity                  |        |
| Lowest Capacity Asset    |             | Portfolio Turnover        | 0%     |
| Drawdown Recovery        | 0           |                           |        |
+-----------------------------------------------------------------------------+
Backtest id: ff008bb7776bbf4ba315a74d03cf4487
Backtest name: Crawling Brown Badger
Backtest url:
https://www.quantconnect.com/project/26025124/ff008bb7776bbf4ba315a74d03cf4487"""

print("Testing parser with zero values...")

try:
    parser = QCOutputParser(zero_values_output)
    
    print(f"Backtest name: {parser.get_backtest_name()}")
    print(f"Return percent: {parser.get_return_percent()}")
    print(f"Sharpe ratio: {parser.get_sharpe_ratio()}")
    print(f"Max drawdown: {parser.get_max_drawdown_percent()}")
    print(f"Total orders: {parser.get_total_orders()}")
    print(f"Total fees: {parser.get_total_fees()}")
    print(f"Win rate: {parser.get_win_rate_percent()}")
    print(f"Final equity: {parser.get_final_equity()}")
    
    print("\nParser succeeded with zero values!")
    
except Exception as e:
    print(f"Parser failed with error: {e}")
    print(f"Error type: {type(e)}")
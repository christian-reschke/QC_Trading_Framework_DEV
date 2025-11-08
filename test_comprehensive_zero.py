"""
Comprehensive test to see what might be wrong with zero value parsing
"""
from utils import QCOutputParser
import json

# Use the actual zero values output from the 1-day backtest
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

print("Testing comprehensive zero values parsing...")
print("=" * 60)

try:
    parser = QCOutputParser(zero_values_output)
    
    # Test all getter methods
    print("Backtest Info:")
    print(f"  Name: {parser.get_backtest_name()}")
    print(f"  ID: {parser.get_backtest_id()}")
    print(f"  URL: {parser.get_backtest_url()}")
    print(f"  Version: {parser.get_strategy_version()}")
    
    print("\nPerformance Metrics:")
    print(f"  Return %: {parser.get_return_percent()}")
    print(f"  Annual Return %: {parser.get_annual_return_percent()}")
    print(f"  Net Profit %: {parser.get_net_profit_percent()}")
    print(f"  Final Equity: {parser.get_final_equity()}")
    print(f"  End Equity: {parser.get_end_equity()}")
    print(f"  Start Equity: {parser.get_start_equity()}")
    
    print("\nRisk Metrics:")
    print(f"  Max Drawdown %: {parser.get_max_drawdown_percent()}")
    print(f"  Sharpe Ratio: {parser.get_sharpe_ratio()}")
    print(f"  Sortino Ratio: {parser.get_sortino_ratio()}")
    print(f"  Alpha: {parser.get_alpha()}")
    print(f"  Beta: {parser.get_beta()}")
    
    print("\nTrade Metrics:")
    print(f"  Total Orders: {parser.get_total_orders()}")
    print(f"  Win Rate %: {parser.get_win_rate_percent()}")
    print(f"  Loss Rate %: {parser.get_loss_rate_percent()}")
    print(f"  Profit-Loss Ratio: {parser.get_profit_loss_ratio()}")
    print(f"  Total Fees: {parser.get_total_fees()}")
    print(f"  Expectancy: {parser.get_expectancy()}")
    
    print("\n" + "=" * 60)
    print("Full parsed data structure:")
    print(json.dumps(parser.to_dict(), indent=2))
    
    print("\n" + "=" * 60)
    print("SUCCESS: Parser handled all zero values correctly!")
    
except Exception as e:
    print(f"ERROR: Parser failed with: {e}")
    import traceback
    traceback.print_exc()
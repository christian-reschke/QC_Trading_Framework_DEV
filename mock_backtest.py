"""
Mock backtest responses for development and testing
"""

def get_mock_backtest_output():
    """
    Returns a mock QuantConnect backtest output for testing table formatting
    """
    return """
Started compiling project 'QC_Trading_Framework_DEPLOY'
Build Request Successful for Project ID: 26025124, with CompileID:
deb51e4560b132e66dc084ecb1ae4db0-1d72b5f5bff4460fa6d8ae4bb692c8fe, Lean
Version: 2.5.0.0.17369
Successfully compiled project 'QC_Trading_Framework_DEPLOY'
Started backtest named 'Test Backtest' for project
'QC_Trading_Framework_DEPLOY'
Backtest url:
https://www.quantconnect.com/project/26025124/78b9174581b72b6ba93e0d025eedcb92
 ---------------------------------------- 100%
+-----------------------------------------------------------------------------+
| Statistic           | Value            | Statistic           | Value        |
|---------------------+------------------+---------------------+--------------|
| Equity              | $124,263.45      | Fees                | -$5.31       |
| Holdings            | $123,169.76      | Net Profit          | $12,702.43   |
| Probabilistic       | 75.995%          | Return              | 24.26 %      |
| Sharpe Ratio        |                  |                     |              |
| Strategy Version    | v2.1.40          | Unrealized          | $11,543.15   |
| Drawdown            | 5.800%           | Expectancy          | 0            |
| Start Equity        | 100000           | End Equity          | 124263.45    |
| Net Profit          | 24.263%          | Sharpe Ratio        | 1.162        |
|                     |                  | Sharpe Ratio        |              |
| Drawdown Recovery   | 62               |                     |              |
+-----------------------------------------------------------------------------+
"""

def get_mock_strategy_metrics():
    """
    Returns mock parsed strategy metrics for testing
    """
    return {
        'deployed_version': 'v2.1.40',
        'final_value': 124263.45,
        'return': 0.2426,  # 24.26%
        'drawdown': 0.058,  # 5.8%
        'start_value': 100000.0,
        'sharpe': 1.162
    }

def run_mock_backtest():
    """
    Mock backtest function that returns fake success data
    """
    output = get_mock_backtest_output()
    metrics = get_mock_strategy_metrics()
    return True, "https://fake-url.com", metrics
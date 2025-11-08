def get_backtest_output():
    return """Executing: C:\\Users\\chris\\pipx\\venvs\\lean\\Scripts\\lean.exe cloud backtest QC_Trading_Framework_DEPLOY
======================================================================
RAW QUANTCONNECT OUTPUT:
======================================================================
Started compiling project 'QC_Trading_Framework_DEPLOY'
Build Request Successful for Project ID: 26025124, with CompileID: 
df66bf5af5eafcbd2c72344c63024674-0b20368c01e5458a9c8aa5b37c875fd6, Lean 
Version: 2.5.0.0.17369
Successfully compiled project 'QC_Trading_Framework_DEPLOY'
Started backtest named 'Crawling Yellow-Green Giraffe' for project 
'QC_Trading_Framework_DEPLOY'
Backtest url: 
https://www.quantconnect.com/project/26025124/3d044e792641d892dcae6312dc0d3bfd
 ---------------------------------------- 100%
+-----------------------------------------------------------------------------+
| Statistic            | Value            | Statistic           | Value       |
|----------------------+------------------+---------------------+-------------|
| Equity               | $110,477.43      | Fees                | -$124.88    |
| Holdings             | $109,420.70      | Net Profit          | $11,619.53  |
| Probabilistic Sharpe | 21.763%          | Return              | 10.48 %     |
| Ratio                |                  |                     |             |
| Strategy Version     | v2.1.56          | Unrealized          | $-1,214.95  |
| Volume               | $7,444,785.15    |                     |             |
|----------------------+------------------+---------------------+-------------|
| Total Orders         | 77               | Average Win         | 8.81%       |
| Average Loss         | -3.34%           | Compounding Annual  | 10.457%     |
|                      |                  | Return              |             |
| Drawdown             | 38.200%          | Expectancy          | 0.149       |
| Start Equity         | 100000           | End Equity          | 110477.43   |
| Net Profit           | 10.477%          | Sharpe Ratio        | 0.235       |
| Sortino Ratio        | 0.378            | Probabilistic       | 21.763%     |
|                      |                  | Sharpe Ratio        |             |
| Loss Rate            | 68%              | Win Rate            | 32%         |
| Profit-Loss Ratio    | 2.64             | Alpha               | -0.059      |
| Beta                 | 1.205            | Annual Standard     | 0.353       |
|                      |                  | Deviation           |             |
| Annual Variance      | 0.124            | Information Ratio   | -0.104      |
| Tracking Error       | 0.33             | Treynor Ratio       | 0.069       |
| Total Fees           | $124.88          | Estimated Strategy  | $1300000.00 |
|                      |                  | Capacity            |             |
| Lowest Capacity      | MDB WOU3US9M42N9 | Portfolio Turnover  | 20.81%      |
| Asset                |                  |                     |             |
| Drawdown Recovery    | 300              |                     |             |
+-----------------------------------------------------------------------------+
Backtest id: 3d044e792641d892dcae6312dc0d3bfd
Backtest name: Crawling Yellow-Green Giraffe
Backtest url:
https://www.quantconnect.com/project/26025124/3d044e792641d892dcae6312dc0d3bfd"""

def get_negative_backtest_output():
    return """Executing: C:\\Users\\chris\\pipx\\venvs\\lean\\Scripts\\lean.exe cloud backtest QC_Trading_Framework_DEPLOY
======================================================================
RAW QUANTCONNECT OUTPUT:
======================================================================
Started compiling project 'QC_Trading_Framework_DEPLOY'
Build Request Successful for Project ID: 26025124, with CompileID:
64df612f8f1351679a7dfde446a0d349-1b0804ee45758693632d5ec6276bd0bd, Lean
Version: 2.5.0.0.17369
Successfully compiled project 'QC_Trading_Framework_DEPLOY'
Started backtest named 'Determined Blue Antelope' for project
'QC_Trading_Framework_DEPLOY'
Backtest url:
https://www.quantconnect.com/project/26025124/afb54e1a186b17a68f23f38bbf3f1416
 ---------------------------------------- 100%
+-----------------------------------------------------------------------------+
| Statistic            | Value            | Statistic           | Value       |
|----------------------+------------------+---------------------+-------------|
| Equity               | $62,687.95       | Fees                | -$134.72    |
| Holdings             | $62,160.27       | Net Profit          | $-36,009.10 |
| Probabilistic Sharpe | 2.950%           | Return              | -37.31 %    |
| Ratio                |                  |                     |             |
| Strategy Version     | v2.1.53          | Unrealized          | $-1,344.35  |
| Volume               | $8,309,994.53    |                     |             |
|----------------------+------------------+---------------------+-------------|
| Total Orders         | 111              | Average Win         | 7.18%       |
| Average Loss         | -3.83%           | Compounding Annual  | -37.259%    |
|                      |                  | Return              |             |
| Drawdown             | 60.100%          | Expectancy          | -0.164      |
| Start Equity         | 100000           | End Equity          | 62687.94    |
| Net Profit           | -37.312%         | Sharpe Ratio        | -0.683      |
| Sortino Ratio        | -1.041           | Probabilistic       | 2.950%      |
|                      |                  | Sharpe Ratio        |             |
| Loss Rate            | 71%              | Win Rate            | 29%         |
| Profit-Loss Ratio    | 1.87             | Alpha               | -0.474      |
| Beta                 | 1.726            | Annual Standard     | 0.398       |
|                      |                  | Deviation           |             |
| Annual Variance      | 0.159            | Information Ratio   | -1.072      |
| Tracking Error       | 0.363            | Treynor Ratio       | -0.158      |
| Total Fees           | $134.72          | Estimated Strategy  | $900000.00  |
|                      |                  | Capacity            |             |
| Lowest Capacity      | MDB WOU3US9M42N9 | Portfolio Turnover  | 30.10%      |
| Asset                |                  |                     |             |
| Drawdown Recovery    | 11               |                     |             |
+-----------------------------------------------------------------------------+
Backtest id: afb54e1a186b17a68f23f38bbf3f1416
Backtest name: Determined Blue Antelope
Backtest url:
https://www.quantconnect.com/project/26025124/afb54e1a186b17a68f23f38bbf3f1416"""
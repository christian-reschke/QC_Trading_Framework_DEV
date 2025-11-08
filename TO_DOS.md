# Trading Strategy Backtesting Plan

**Instructions:** 
- After successfully completing one of the steps, check the checkbox.
- Make sure to keep notes meaningful, and double check if they are neccessary.
- Don't try to execute the python files directly. Use the make commands instead.

## Backtesting Plan for MDB Strategy

Current Strategy: VolaBreakoutStrategy  
Symbol: MDB  
Period: 2024-01-01 to 2024-12-31  
Starting Capital: $100,000  

### Timeframe Testing Schedule

#### Minute-Based Timeframes
- [x] 1 minute
- [x] 5 minutes
- [x] 10 minutes
- [x] 15 minutes
- [x] 20 minutes
- [x] 30 minutes
- [x] 45 minutes

#### Hour-Based Timeframes
- [x] 1 hour (60 minutes)
- [x] 2 hours (120 minutes)
- [x] 4 hours (240 minutes)
- [x] 1 day (1440 minutes)
- [ ] 8 hours (480 minutes)

#### Daily Timeframe
- [ ] 1 day (1440 minutes)

### Testing Process for Each Timeframe

1. Update `TIMEFRAME_MINUTES` in `strategy_config.py`
2. Run `make push` to deploy to QuantConnect (automatically increments version)
3. Run `make backtest` to execute backtest
4. **Copy exact QuantConnect output** including backtest name and raw metrics
5. Record results in Results Section below with raw output
6. Check off the corresponding timeframe above

---

## Results Section

### Completed Backtests

#### 15 Minutes (Baseline) ✓
- **Return**: 8.46%
- **Max Drawdown**: 38.90%
- **Sharpe Ratio**: 0.19
- **Notes**: Backtest name: "Upgraded Yellow-Green Frog" - Positive performance, best so far
- **Version**: v2.1.57

**Raw QuantConnect Output:**
```
Started compiling project 'QC_Trading_Framework_DEPLOY'
Build Request Successful for Project ID: 26025124, with CompileID:
8a2d141cb64752e785317bde9c0c1cb9-b4e1cd0a8c1400c055693e502efe3067, Lean
Version: 2.5.0.0.17369
Successfully compiled project 'QC_Trading_Framework_DEPLOY'
Started backtest named 'Upgraded Yellow-Green Frog' for project
'QC_Trading_Framework_DEPLOY'
Backtest url:
https://www.quantconnect.com/project/26025124/5ce2ca14e6231aa98806348e7f97d74b
 ---------------------------------------- 100%
+-----------------------------------------------------------------------------+
| Statistic            | Value            | Statistic           | Value       |
|----------------------+------------------+---------------------+-------------|
| Equity               | $108,458.65      | Fees                | -$110.30    |
| Holdings             | $0.00            | Net Profit          | $8,458.65   |
| Probabilistic Sharpe | 20.477%          | Return              | 8.46 %      |
| Ratio                |                  |                     |             |
| Strategy Version     | v2.1.57          | Unrealized          | $0.00       |
| Volume               | $6,699,431.81    |                     |             |
|----------------------+------------------+---------------------+-------------|
| Total Orders         | 68               | Average Win         | 8.99%       |
| Average Loss         | -3.62%           | Compounding Annual  | 8.443%      |
|                      |                  | Return              |             |
| Drawdown             | 38.900%          | Expectancy          | 0.127       |
| Start Equity         | 100000           | End Equity          | 108458.65   |
| Net Profit           | 8.459%           | Sharpe Ratio        | 0.19        |
| Sortino Ratio        | 0.289            | Probabilistic       | 20.477%     |
|                      |                  | Sharpe Ratio        |             |
| Loss Rate            | 68%              | Win Rate            | 32%         |
| Profit-Loss Ratio    | 2.48             | Alpha               | -0.063      |
| Beta                 | 1.095            | Annual Standard     | 0.346       |
|                      |                  | Deviation           |             |
| Annual Variance      | 0.119            | Information Ratio   | -0.158      |
| Tracking Error       | 0.326            | Treynor Ratio       | 0.06        |
| Total Fees           | $110.30          | Estimated Strategy  | $1600000.00 |
|                      |                  | Capacity            |             |
| Lowest Capacity      | MDB WOU3US9M42N9 | Portfolio Turnover  | 18.44%      |
| Asset                |                  |                     |             |
| Drawdown Recovery    | 300              |                     |             |
+-----------------------------------------------------------------------------+
Backtest id: 5ce2ca14e6231aa98806348e7f97d74b
Backtest name: Upgraded Yellow-Green Frog
Backtest url:
https://www.quantconnect.com/project/26025124/5ce2ca14e6231aa98806348e7f97d74b
```

#### 1 Minute
- **Return**: -46.66%
- **Max Drawdown**: 57.60%
- **Sharpe Ratio**: -0.82
- **Notes**: Backtest name: "Emotional Light Brown Kangaroo" - Poor performance, significant losses
- **Version**: v2.1.51

**Raw QuantConnect Output:**
```
Build Request Successful for Project ID: 26025124, with CompileID:  
bb8ad84349217a09c30ea7d95199c8f0-deda2e314c3471d509e9711ea448a877, Lean
Version: 2.5.0.0.17369
Successfully compiled project 'QC_Trading_Framework_DEPLOY'
Started backtest named 'Emotional Light Brown Kangaroo' for project 
'QC_Trading_Framework_DEPLOY'     
Backtest url:    
https://www.quantconnect.com/project/26025124/cc6b37195ab2f1095f71b25cd6a3c83f       
 ---------------------------------------- 100%     
+-----------------------------------------------------------------------------+      
| Statistic            | Value            | Statistic           | Value       |      
|----------------------+------------------+---------------------+-------------|      
| Equity         
      | $53,394.08       | Fees                | -$165.66    |      
| Holdings             | $52,847.87       | Net Profit          | $-45,915.85 |      
| Probabilistic Sharpe | 1.861%           | Return              | -46.61 %    |      
| Ratio          
      |          
        |                     |             |      
| Strategy Version     | v2.1.51          | Unrealized          | $-725.27    |      
| Volume         
      | $10,184,965.80   |                     |             |      
|----------------------+------------------+---------------------+-------------|      
| Total Orders         | 135              | Average Win         | 5.71%       |      
| Average Loss         | -4.28%           | Compounding Annual  | -46.545%    |      
|                
      |          
        | Return              |             |      
| Drawdown             | 57.600%          | Expectancy          | -0.163      |      
| Start Equity         | 100000           | End Equity          | 53394.08    |      
| Net Profit           | -46.606%         | Sharpe Ratio        | -0.73       |      
| Sortino Ratio        | -0.82            | Probabilistic       | 1.861%      |      
|                
      |          
        | Sharpe Ratio        |             |      
| Loss Rate            | 64%              | Win Rate            | 36%         |      
| Profit-Loss Ratio    | 1.34             | Alpha               | -0.547      |      
| Beta           
      | 1.822            | Annual Standard     | 0.457       |      
|                
      |          
        | Deviation           |             |      
| Annual Variance      | 0.209            | Information Ratio   | -1.063      |      
| Tracking Error       | 0.424            | Treynor Ratio       | -0.183      |      
| Total Fees           | $165.66          | Estimated Strategy  | $980000.00  |      
|                
      |          
        | Capacity            |             |      
| Lowest Capacity      | MDB WOU3US9M42N9 | Portfolio Turnover  | 36.58%      |      
| Asset          
      |          
        |                     |             |      
| Drawdown Recovery    | 14               |                     |             |      
+-----------------------------------------------------------------------------+      
Backtest id: cc6b37195ab2f1095f71b25cd6a3c83f      
Backtest name: Emotional Light Brown Kangaroo      
Backtest url:    
https://www.quantconnect.com/project/26025124/cc6b37195ab2f1095f71b25cd6a3c83f
``` 

#### 5 Minutes
- **Return**: -37.31%
- **Max Drawdown**: 60.10%
- **Sharpe Ratio**: -0.683
- **Notes**: Backtest name: "Retrospective Yellow-Green Chimpanzee" - Significant losses, better than 1min but still poor
- **Version**: v2.1.53

**Raw QuantConnect Output:**
```
Started compiling project 'QC_Trading_Framework_DEPLOY'
Build Request Successful for Project ID: 26025124, with CompileID: 
f1e530cf48f3f1af1fab1ef185facaac-1b0804ee45758693632d5ec6276bd0bd, Lean 
Version: 2.5.0.0.17369
Successfully compiled project 'QC_Trading_Framework_DEPLOY'
Started backtest named 'Retrospective Yellow-Green Chimpanzee' for project 
'QC_Trading_Framework_DEPLOY'
Backtest url: 
https://www.quantconnect.com/project/26025124/5f803693d38bdb5e7724c3777f2b40b9
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
Backtest id: 5f803693d38bdb5e7724c3777f2b40b9
Backtest name: Retrospective Yellow-Green Chimpanzee
Backtest url:
https://www.quantconnect.com/project/26025124/5f803693d38bdb5e7724c3777f2b40b9
``` 

#### 10 Minutes
- **Return**: 10.48%
- **Max Drawdown**: 38.20%
- **Sharpe Ratio**: 0.235
- **Notes**: Backtest name: "Determined Blue Antelope" - Identical results to 5min, same performance
- **Version**: v2.1.53

**Raw QuantConnect Output:**
```
Started compiling project 'QC_Trading_Framework_DEPLOY'
Build Request Successful for Project ID: 26025124, with CompileID:
fcef981463a3d2f37eca020bdbe7849f-0b20368c01e5458a9c8aa5b37c875fd6, Lean
Version: 2.5.0.0.17369
Successfully compiled project 'QC_Trading_Framework_DEPLOY'
Started backtest named 'Casual Sky Blue Chinchilla' for project
'QC_Trading_Framework_DEPLOY'
Backtest url:
https://www.quantconnect.com/project/26025124/d8c587ba80c2a9982eef823f70398b24
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
Backtest id: d8c587ba80c2a9982eef823f70398b24
```

#### 20 Minutes
- **Return**: 4.18%
- **Max Drawdown**: 36.00%
- **Sharpe Ratio**: 0.098
- **Notes**: Backtest name: "Virtual Fluorescent Yellow Sheep" - Positive but lower than 15min
- **Version**: v2.1.58

**Raw QuantConnect Output:**
```
Started compiling project 'QC_Trading_Framework_DEPLOY'
Build Request Successful for Project ID: 26025124, with CompileID:
aa2601f2c4f5d2b8c64ffcc4844df14d-c569e8d113efd899a41d2db776e0bf9b, Lean
Version: 2.5.0.0.17369
Successfully compiled project 'QC_Trading_Framework_DEPLOY'
Started backtest named 'Virtual Fluorescent Yellow Sheep' for project
'QC_Trading_Framework_DEPLOY'
Backtest url:
https://www.quantconnect.com/project/26025124/59ba69cab560f849a969b0cbbbd19d83
 ---------------------------------------- 100%
+-----------------------------------------------------------------------------+
| Statistic            | Value            | Statistic           | Value       |
|----------------------+------------------+---------------------+-------------|
| Equity               | $104,178.48      | Fees                | -$105.54    |
| Holdings             | $0.00            | Net Profit          | $4,178.48   |
| Probabilistic Sharpe | 17.893%          | Return              | 4.18 %      |
| Ratio                |                  |                     |             |
| Strategy Version     | v2.1.58          | Unrealized          | $0.00       |
| Volume               | $6,415,416.24    |                     |             |
|----------------------+------------------+---------------------+-------------|
| Total Orders         | 66               | Average Win         | 8.47%       |
| Average Loss         | -3.73%           | Compounding Annual  | 4.171%      |
|                      |                  | Return              |             |
| Drawdown             | 36.000%          | Expectancy          | 0.090       |
| Start Equity         | 100000           | End Equity          | 104178.48   |
| Net Profit           | 4.178%           | Sharpe Ratio        | 0.098       |
| Sortino Ratio        | 0.143            | Probabilistic       | 17.893%     |
|                      |                  | Sharpe Ratio        |             |
| Loss Rate            | 67%              | Win Rate            | 33%         |
| Profit-Loss Ratio    | 2.27             | Alpha               | -0.09       |
| Beta                 | 1.052            | Annual Standard     | 0.342       |
|                      |                  | Deviation           |             |
| Annual Variance      | 0.117            | Information Ratio   | -0.259      |
| Tracking Error       | 0.323            | Treynor Ratio       | 0.032       |
| Total Fees           | $105.54          | Estimated Strategy  | $2400000.00 |
|                      |                  | Capacity            |             |
| Lowest Capacity      | MDB WOU3US9M42N9 | Portfolio Turnover  | 17.90%      |
| Asset                |                  |                     |             |
| Drawdown Recovery    | 13               |                     |             |
+-----------------------------------------------------------------------------+
Backtest id: 59ba69cab560f849a969b0cbbbd19d83
Backtest name: Virtual Fluorescent Yellow Sheep
Backtest url:
https://www.quantconnect.com/project/26025124/59ba69cab560f849a969b0cbbbd19d83
``` 

#### 30 Minutes
- **Return**: 21.20%
- **Max Drawdown**: 24.90%
- **Sharpe Ratio**: 0.469
- **Notes**: Backtest name: "Ugly Sky Blue Snake" - Best performance yet! Significant improvement
- **Version**: v2.1.59

**Raw QuantConnect Output:**
```
Started compiling project 'QC_Trading_Framework_DEPLOY'
Build Request Successful for Project ID: 26025124, with CompileID:
4e490fd0e57d4ee85dab53cd460e938a-7a4090420ece5cb3b5d1fd129fe36d29, Lean
Version: 2.5.0.0.17369
Successfully compiled project 'QC_Trading_Framework_DEPLOY'
Started backtest named 'Ugly Sky Blue Snake' for project
'QC_Trading_Framework_DEPLOY'
Backtest url:
https://www.quantconnect.com/project/26025124/daa6471a68a7ea4444518bf827412190
 ---------------------------------------- 100%
+-----------------------------------------------------------------------------+
| Statistic            | Value            | Statistic           | Value       |
|----------------------+------------------+---------------------+-------------|
| Equity               | $121,198.56      | Fees                | -$85.20     |
| Holdings             | $0.00            | Net Profit          | $21,198.56  |
| Probabilistic Sharpe | 31.468%          | Return              | 21.20 %     |
| Ratio                |                  |                     |             |
| Strategy Version     | v2.1.59          | Unrealized          | $0.00       |
| Volume               | $5,124,550.06    |                     |             |
|----------------------+------------------+---------------------+-------------|
| Total Orders         | 48               | Average Win         | 9.50%       |
| Average Loss         | -3.24%           | Compounding Annual  | 21.156%     |
|                      |                  | Return              |             |
| Drawdown             | 24.900%          | Expectancy          | 0.311       |
| Start Equity         | 100000           | End Equity          | 121198.56   |
| Net Profit           | 21.199%          | Sharpe Ratio        | 0.469       |
| Sortino Ratio        | 0.545            | Probabilistic       | 31.468%     |
|                      |                  | Sharpe Ratio        |             |
| Loss Rate            | 67%              | Win Rate            | 33%         |
| Profit-Loss Ratio    | 2.93             | Alpha               | 0.035       |
| Beta                 | 0.843            | Annual Standard     | 0.285       |
|                      |                  | Deviation           |             |
| Annual Variance      | 0.081            | Information Ratio   | 0.06        |
| Tracking Error       | 0.272            | Treynor Ratio       | 0.159       |
| Total Fees           | $85.20           | Estimated Strategy  | $2500000.00 |
|                      |                  | Capacity            |             |
| Lowest Capacity      | MDB WOU3US9M42N9 | Portfolio Turnover  | 13.00%      |
| Asset                |                  |                     |             |
| Drawdown Recovery    | 283              |                     |             |
+-----------------------------------------------------------------------------+
Backtest id: daa6471a68a7ea4444518bf827412190
Backtest name: Ugly Sky Blue Snake
Backtest url:
https://www.quantconnect.com/project/26025124/daa6471a68a7ea4444518bf827412190
``` 

#### 45 Minutes
- **Return**: 12.50%
- **Max Drawdown**: 24.70%
- **Sharpe Ratio**: 0.259
- **Notes**: Backtest name: "Emotional Tan Albatross" - Good performance, lower than 30min but still solid
- **Version**: v2.1.60

**Raw QuantConnect Output:**
```
Started compiling project 'QC_Trading_Framework_DEPLOY'
Build Request Successful for Project ID: 26025124, with CompileID:
a7da158e5ab5f14d60c660d952d22cb2-a22b6f3864006ae6870927b0a150b59e, Lean
Version: 2.5.0.0.17369
Successfully compiled project 'QC_Trading_Framework_DEPLOY'
Started backtest named 'Emotional Tan Albatross' for project
'QC_Trading_Framework_DEPLOY'
Backtest url:
https://www.quantconnect.com/project/26025124/d898574e7d6875480187958b64afff3b
 ---------------------------------------- 100%
+-----------------------------------------------------------------------------+
| Statistic            | Value            | Statistic           | Value       |
|----------------------+------------------+---------------------+-------------|
| Equity               | $112,500.61      | Fees                | -$75.88     |
| Holdings             | $0.00            | Net Profit          | $12,500.61  |
| Probabilistic Sharpe | 24.228%          | Return              | 12.50 %     |
| Ratio                |                  |                     |             |
| Strategy Version     | v2.1.60          | Unrealized          | $0.00       |
| Volume               | $4,586,125.75    |                     |             |
|----------------------+------------------+---------------------+-------------|
| Total Orders         | 44               | Average Win         | 7.66%       |
| Average Loss         | -4.06%           | Compounding Annual  | 12.476%     |
|                      |                  | Return              |             |
| Drawdown             | 24.700%          | Expectancy          | 0.180       |
| Start Equity         | 100000           | End Equity          | 112500.61   |
| Net Profit           | 12.501%          | Sharpe Ratio        | 0.259       |
| Sortino Ratio        | 0.299            | Probabilistic       | 24.228%     |
|                      |                  | Sharpe Ratio        |             |
| Loss Rate            | 59%              | Win Rate            | 41%         |
| Profit-Loss Ratio    | 1.88             | Alpha               | -0.027      |
| Beta                 | 0.859            | Annual Standard     | 0.283       |
|                      |                  | Deviation           |             |
| Annual Variance      | 0.08             | Information Ratio   | -0.163      |
| Tracking Error       | 0.269            | Treynor Ratio       | 0.085       |
| Total Fees           | $75.88           | Estimated Strategy  | $2400000.00 |
|                      |                  | Capacity            |             |
| Lowest Capacity      | MDB WOU3US9M42N9 | Portfolio Turnover  | 11.94%      |
| Asset                |                  |                     |             |
| Drawdown Recovery    | 286              |                     |             |
+-----------------------------------------------------------------------------+
Backtest id: d898574e7d6875480187958b64afff3b
Backtest name: Emotional Tan Albatross
Backtest url:
https://www.quantconnect.com/project/26025124/d898574e7d6875480187958b64afff3b
``` 

#### 1 Hour (60 Minutes)
- **Return**: 12.21%
- **Max Drawdown**: 15.60%
- **Sharpe Ratio**: 0.247
- **Notes**: Backtest name: "Focused Tan Dinosaur" - Good performance, excellent low drawdown!
- **Version**: v2.1.62

**Raw QuantConnect Output:**
```
Started compiling project 'QC_Trading_Framework_DEPLOY'
Build Request Successful for Project ID: 26025124, with CompileID:
e309988a1f1fb43ff2353acca2c13a26-d76c67a412df4fbfbd9b636a2ec8bc34, Lean
Version: 2.5.0.0.17369
Successfully compiled project 'QC_Trading_Framework_DEPLOY'
Started backtest named 'Focused Tan Dinosaur' for project
'QC_Trading_Framework_DEPLOY'
Backtest url:
https://www.quantconnect.com/project/26025124/6c874106fda5d0d4d0be2f632acff698
 ---------------------------------------- 100%
+-----------------------------------------------------------------------------+
| Statistic            | Value            | Statistic           | Value       |
|----------------------+------------------+---------------------+-------------|
| Equity               | $112,206.00      | Fees                | -$56.98     |
| Holdings             | $0.00            | Net Profit          | $12,206.00  |
| Probabilistic Sharpe | 25.784%          | Return              | 12.21 %     |
| Ratio                |                  |                     |             |
| Strategy Version     | v2.1.62          | Unrealized          | $0.00       |
| Volume               | $3,463,592.32    |                     |             |
|----------------------+------------------+---------------------+-------------|
| Total Orders         | 32               | Average Win         | 6.58%       |
| Average Loss         | -3.56%           | Compounding Annual  | 12.182%     |
|                      |                  | Return              |             |
| Drawdown             | 15.600%          | Expectancy          | 0.246       |
| Start Equity         | 100000           | End Equity          | 112206      |
| Net Profit           | 12.206%          | Sharpe Ratio        | 0.247       |
| Sortino Ratio        | 0.221            | Probabilistic       | 25.784%     |
|                      |                  | Sharpe Ratio        |             |
| Loss Rate            | 56%              | Win Rate            | 44%         |
| Profit-Loss Ratio    | 1.85             | Alpha               | -0.009      |
| Beta                 | 0.562            | Annual Standard     | 0.232       |
|                      |                  | Deviation           |             |
| Annual Variance      | 0.054            | Information Ratio   | -0.262      |
| Tracking Error       | 0.229            | Treynor Ratio       | 0.102       |
| Total Fees           | $56.98           | Estimated Strategy  | $2600000.00 |
|                      |                  | Capacity            |             |
| Lowest Capacity      | MDB WOU3US9M42N9 | Portfolio Turnover  | 8.65%       |
| Asset                |                  |                     |             |
| Drawdown Recovery    | 139              |                     |             |
+-----------------------------------------------------------------------------+
Backtest id: 6c874106fda5d0d4d0be2f632acff698
Backtest name: Focused Tan Dinosaur
Backtest url:
https://www.quantconnect.com/project/26025124/6c874106fda5d0d4d0be2f632acff698
``` 

#### 2 Hours (120 Minutes)
- **Return**: -19.70%
- **Max Drawdown**: 33.20%
- **Sharpe Ratio**: -1.045
- **Notes**: Backtest name: "Muscular Tan Alpaca" - Performance drops significantly at 2+ hours
- **Version**: v2.1.63

**Raw QuantConnect Output:**
```
Started compiling project 'QC_Trading_Framework_DEPLOY'
Build Request Successful for Project ID: 26025124, with CompileID:
845b060dcf8dc3f99851cb6694d8b77d-6d28ea0381f6e3f6030ea79bca14e85c, Lean
Version: 2.5.0.0.17369
Successfully compiled project 'QC_Trading_Framework_DEPLOY'
Started backtest named 'Muscular Tan Alpaca' for project
'QC_Trading_Framework_DEPLOY'
Backtest url:
https://www.quantconnect.com/project/26025124/37e52300cd54e97441467ef47f788826
 ---------------------------------------- 100%
+-----------------------------------------------------------------------------+
| Statistic            | Value            | Statistic           | Value       |
|----------------------+------------------+---------------------+-------------|
| Equity               | $80,303.02       | Fees                | -$34.88     |
| Holdings             | $0.00            | Net Profit          | $-19,696.98 |
| Probabilistic Sharpe | 1.378%           | Return              | -19.70 %    |
| Ratio                |                  |                     |             |
| Strategy Version     | v2.1.63          | Unrealized          | $0.00       |
| Volume               | $2,108,121.38    |                     |             |
|----------------------+------------------+---------------------+-------------|
| Total Orders         | 22               | Average Win         | 4.34%       |
| Average Loss         | -5.35%           | Compounding Annual  | -19.665%    |
|                      |                  | Return              |             |
| Drawdown             | 33.200%          | Expectancy          | -0.341      |
| Start Equity         | 100000           | End Equity          | 80303.02    |
| Net Profit           | -19.697%         | Sharpe Ratio        | -1.045      |
| Sortino Ratio        | -0.635           | Probabilistic       | 1.378%      |
|                      |                  | Sharpe Ratio        |             |
| Loss Rate            | 64%              | Win Rate            | 36%         |
| Profit-Loss Ratio    | 0.81             | Alpha               | -0.214      |
| Beta                 | 0.267            | Annual Standard     | 0.174       |
|                      |                  | Deviation           |             |
| Annual Variance      | 0.03             | Information Ratio   | -1.589      |
| Tracking Error       | 0.188            | Treynor Ratio       | -0.681      |
| Total Fees           | $34.88           | Estimated Strategy  | $1800000.00 |
|                      |                  | Capacity            |             |
| Lowest Capacity      | MDB WOU3US9M42N9 | Portfolio Turnover  | 5.95%       |
| Asset                |                  |                     |             |
| Drawdown Recovery    | 16               |                     |             |
+-----------------------------------------------------------------------------+
Backtest id: 37e52300cd54e97441467ef47f788826
Backtest name: Muscular Tan Alpaca
Backtest url:
https://www.quantconnect.com/project/26025124/37e52300cd54e97441467ef47f788826
``` 

#### 3 Hours (180 Minutes)
- **Return**: _%
- **Max Drawdown**: _%
- **Sharpe Ratio**: 
- **Notes**: 
- **Version**: 

#### 4 Hours (240 Minutes)
- **Return**: -2.58%
- **Max Drawdown**: 16.90%
- **Sharpe Ratio**: -0.824
- **Notes**: Backtest name: "Formal Green Shark" - Very few trades (6), slight loss but low drawdown
- **Version**: v2.1.64

**Raw QuantConnect Output:**
```
Started compiling project 'QC_Trading_Framework_DEPLOY'
Build Request Successful for Project ID: 26025124, with CompileID:
52f9568bd1320762d57d392c4557ddb4-b9faf80efb283fa0b16cd75d4625b634, Lean
Version: 2.5.0.0.17369
Successfully compiled project 'QC_Trading_Framework_DEPLOY'
Started backtest named 'Formal Green Shark' for project
'QC_Trading_Framework_DEPLOY'
Backtest url:
https://www.quantconnect.com/project/26025124/f70598e930c5931208351acfe8c23f32
 ---------------------------------------- 100%
+-----------------------------------------------------------------------------+
| Statistic            | Value            | Statistic            | Value      |
|----------------------+------------------+----------------------+------------|
| Equity               | $97,421.31       | Fees                 | -$8.79     |
| Holdings             | $0.00            | Net Profit           | $-2,578.69 |
| Probabilistic Sharpe | 8.176%           | Return               | -2.58 %    |
| Ratio                |                  |                      |            |
| Strategy Version     | v2.1.64          | Unrealized           | $0.00      |
| Volume               | $618,404.14      |                      |            |
|----------------------+------------------+----------------------+------------|
| Total Orders         | 6                | Average Win          | 10.79%     |
| Average Loss         | -6.23%           | Compounding Annual   | -2.574%    |
|                      |                  | Return               |            |
| Drawdown             | 16.900%          | Expectancy           | -0.089     |
| Start Equity         | 100000           | End Equity           | 97421.31   |
| Net Profit           | -2.579%          | Sharpe Ratio         | -0.824     |
| Sortino Ratio        | -0.353           | Probabilistic Sharpe | 8.176%     |
|                      |                  | Ratio                |            |
| Loss Rate            | 67%              | Win Rate             | 33%        |
| Profit-Loss Ratio    | 1.73             | Alpha                | -0.085     |
| Beta                 | 0.136            | Annual Standard      | 0.084      |
|                      |                  | Deviation            |            |
| Annual Variance      | 0.007            | Information Ratio    | -1.52      |
| Tracking Error       | 0.123            | Treynor Ratio        | -0.511     |
| Total Fees           | $8.79            | Estimated Strategy   | $860000.00 |
|                      |                  | Capacity             |            |
| Lowest Capacity      | MDB WOU3US9M42N9 | Portfolio Turnover   | 1.62%      |
| Asset                |                  |                      |            |
| Drawdown Recovery    | 2                |                      |            |
+-----------------------------------------------------------------------------+
Backtest id: f70598e930c5931208351acfe8c23f32
Backtest name: Formal Green Shark
Backtest url:
https://www.quantconnect.com/project/26025124/f70598e930c5931208351acfe8c23f32
``` 

#### 8 Hours (480 Minutes)
- **Return**: _%
- **Max Drawdown**: _%
- **Sharpe Ratio**: 
- **Notes**: 
- **Version**: 

#### 1 Day (1440 Minutes)
- **Return**: 0.00%
- **Max Drawdown**: 0.00%
- **Sharpe Ratio**: 0.00
- **Notes**: Backtest name: "Crawling Brown Badger" - NO TRADES! Strategy requires shorter timeframes
- **Version**: v2.1.65

**Raw QuantConnect Output:**
```
Started compiling project 'QC_Trading_Framework_DEPLOY'
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
https://www.quantconnect.com/project/26025124/ff008bb7776bbf4ba315a74d03cf4487
``` 

---

## Analysis Notes

### Best Performing Timeframes
1. **TBD** - % return, % drawdown, sharpe ratio
2. **TBD** - % return, % drawdown, sharpe ratio  
3. **TBD** - % return, % drawdown, sharpe ratio

### Observations
- **Optimal Range**: TBD
- **Risk Patterns**: TBD
- **Market Efficiency**: TBD

### Next Steps
- [ ] Analyze correlation between timeframe and performance
- [ ] Identify optimal timeframe range for MDB
- [ ] Test top 3 timeframes with different symbols
- [ ] Optimize strategy parameters for best timeframe

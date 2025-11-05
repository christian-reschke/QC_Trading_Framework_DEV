# Reference Data Directory

This directory contains reference chart data for exact performance calculations.

## Directory Structure

```
data/
├── spy/                    # SPY price data
│   ├── spy_q3_2025.csv    # Q3 2025 daily prices
│   ├── spy_2023.csv       # Full year 2023
│   ├── spy_2024.csv       # Full year 2024
│   └── spy_2025.csv       # Full year 2025
├── benchmarks/            # Benchmark comparison data
│   ├── spy_buy_hold.csv   # Buy & hold reference
│   └── market_returns.csv # Market benchmark returns
└── README.md              # This file
```

## Data Format

### SPY Price Data (CSV format)
```csv
Date,Open,High,Low,Close,Volume
2025-07-01,550.25,552.30,549.80,551.45,45234567
2025-07-02,551.50,553.20,550.90,552.75,38901234
...
```

### Expected Columns
- **Date**: YYYY-MM-DD format
- **Open**: Opening price
- **High**: Daily high
- **Low**: Daily low  
- **Close**: Closing price (most important for calculations)
- **Volume**: Trading volume

## Usage

The `calculate_performance.py` script can be enhanced to read from these files:

```python
# Read SPY data for Q3 2025
python calculate_performance.py --data-file data/spy/spy_q3_2025.csv

# Calculate performance for specific date range
python calculate_performance.py --start-date 2025-07-01 --end-date 2025-09-30
```

## Data Sources

Recommended sources for accurate data:
- Yahoo Finance (yfinance)
- Alpha Vantage
- QuantConnect data exports
- SPDR official data

## File Naming Convention

- Use lowercase with underscores
- Include time period in filename
- Use `.csv` format for easy processing
- Example: `spy_q3_2025.csv`, `spy_daily_2024.csv`
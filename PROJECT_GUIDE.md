# SPY EMA Strategy Project - Developer Guide

<!-- 
===============================================================================================================
FILE: PROJECT_GUIDE.md
PURPOSE: Current workflows, commands, performance analysis tools, daily operations
===============================================================================================================
-->

**Last Updated:** November 5, 2025  
**Project Status:** Enhanced Performance Analysis System Complete  
**Architecture:** Development + Deployment separation with professional benchmarking tools

## Dual Project Structure

### Development Project: d:\QC\SPY_EMA_Strategy_DEV\
- Complete C# framework with all modules and tests
- Full project history and development files
- Python algorithm development and testing
- Documentation and research files
- Git repository (when restored)

### Deployment Project: d:\QC\SPY_EMA_Strategy_DEPLOY\
- ONLY essential QuantConnect files (main.py, config.json, research.ipynb)
- Clean project structure for cloud deployment
- No special characters, no development artifacts
- Direct push to QuantConnect without conflicts

## Enhanced Performance Analysis System

### Professional Benchmarking Tools
- Real market data integration from TradingView CSV format
- Color-coded performance comparison table
- Comprehensive risk metrics (Sharpe ratio, max drawdown, volatility)
- Dynamic table formatting with proper alignment
- Terminal-based analysis workflow

### Performance Calculator: calculate_performance.py
**Real Market Data Analysis Tool**

#### Features:
- **TradingView CSV Support** - Import real SPY daily data (1993-2025)
- **Buy & Hold Benchmark** - Exact comparison using opening prices from data range
- **Color-Coded Tables** - Green (outperform), Red (underperform), Clear visual comparison
- **Comprehensive Metrics** - Returns, Sharpe ratio, max drawdown, volatility
- **Dynamic Formatting** - Professional table layout with proper alignment
- **Date Range Analysis** - Support for any date range within available data

#### Usage:
```bash
# Standard performance comparison for date range
python calculate_performance.py --file "data/spy/SPY_DAILY_1993-01-29_2025-11-04.csv" --start "2025-07-01" --end "2025-09-30"

# Quick analysis for current backtest results
python calculate_performance.py --file "data/spy/SPY_DAILY_1993-01-29_2025-11-04.csv" --start "2025-01-01" --end "2025-11-04"
```

### Current Q3 2025 Performance Results
**Strategy vs Buy & Hold Analysis (2025-07-01 to 2025-09-30)**

| Metric | Strategy | Buy & Hold | Comparison |
|--------|----------|------------|------------|
| **Total Return** | 8.13% | 8.51% | ❌ -0.38% |
| **Sharpe Ratio** | 2.601 | 3.868 | ❌ -1.267 |
| **Max Drawdown** | 2.40% | 2.13% | ❌ +0.27% |
| **Volatility** | 3.13% | 2.20% | ❌ +0.93% |

**Analysis:** Buy & hold outperformed with better risk-adjusted returns and lower volatility.

## Algorithm Development Workflow

### Core Files Structure
```
main.py                 # Main QuantConnect algorithm
config.json            # Algorithm configuration
research.ipynb         # Jupyter research notebook
calculate_performance.py # Performance analysis tool
data/spy/              # Real market data files
```

### Development Commands
```bash
# Enhanced backtest with analysis
make backtest-enhanced

# Deploy to QuantConnect 
make push

# Performance analysis with color-coded tables
make calculate-performance

# Quick local testing
python quick_test.py
```

### Makefile Commands Reference
```bash
# Current working commands
make push                 # Deploy to QuantConnect cloud
make backtest-enhanced   # Run backtest + performance analysis
make calculate-performance # Generate comparison tables

# Standard commands
make install            # Install dependencies  
make clean             # Clean build files
make test              # Run unit tests
```

## Data Management

### SPY Market Data
**File:** `data/spy/SPY_DAILY_1993-01-29_2025-11-04.csv`
- **Source:** TradingView export
- **Range:** January 29, 1993 to November 4, 2025 (32+ years)
- **Format:** Date, Open, High, Low, Close, Volume
- **Purpose:** Real market data for accurate buy & hold calculations

### Buy & Hold Calculation Method
1. **Start Price:** Opening price on start date from real market data
2. **End Price:** Closing price on end date from real market data  
3. **Return Calculation:** (End Price - Start Price) / Start Price
4. **Risk Metrics:** Calculate from daily returns using real price movements

## Enhanced Backtest Workflow

### Full Analysis Pipeline
```bash
# 1. Deploy algorithm to QuantConnect
make push

# 2. Run backtest on cloud platform
# (Manual step in QuantConnect web interface)

# 3. Analyze results with real market data
make calculate-performance
```

### Performance Analysis Integration
- Algorithm tracks both strategy and buy & hold performance
- Real market data provides exact benchmark calculations
- Color-coded tables show immediate performance comparison
- Professional metrics for comprehensive analysis

## C# Framework Components

### Module Structure
```
src/
├── framework/
│   ├── builder/         # Strategy builder pattern
│   ├── interfaces/      # Component interfaces
│   └── metrics/         # Performance metrics
├── modules/
│   ├── entries/         # Entry signal modules
│   ├── exits/           # Exit signal modules
│   ├── risk/            # Risk management
│   └── sizing/          # Position sizing
```

### Key Components
- **SimpleStrategyBuilder.cs** - Main strategy construction
- **EMA50Entry.cs** / **EMA100Exit.cs** - Signal modules
- **BasicRiskManagement.cs** - Risk controls
- **QuickResults.cs** - Performance tracking

## Testing Framework

### Unit Tests
```bash
# Run all tests
make test

# Test specific components
dotnet test tests/unit/BuilderTests.cs
dotnet test tests/unit/MetricsTests.cs
```

### Test Coverage
- Builder pattern functionality
- Module integration testing
- Performance metrics validation
- Mock data testing scenarios

## Project File Organization

### Current Working Files
- `main.py` - Primary algorithm implementation
- `config.json` - Algorithm configuration
- `calculate_performance.py` - Performance analysis tool
- `Makefile` - Build and deployment commands
- `PROJECT_GUIDE.md` - This operational guide
- `README.md` - Project overview and master framework concept
- `masterplan.md` - Future architecture and strategic planning

### Documentation Standards
- **README.md** - High-level project overview
- **PROJECT_GUIDE.md** - Detailed workflows and operations (this file)
- **masterplan.md** - Future architecture and planning
- Clear separation of purposes, no redundancy

## Development Best Practices

### Code Standards
- Clean Python code following PEP 8
- Comprehensive docstrings for functions
- Professional variable and function naming
- No special characters in production files

### Performance Analysis Standards  
- Always use real market data for benchmarking
- Include buy & hold comparison for context
- Use color-coded tables for clear visualization
- Document methodology and data sources

### Deployment Standards
- Clean separation between development and deployment
- Essential files only in deployment project
- Regular performance validation
- Professional presentation of results

## Troubleshooting

### Common Issues
1. **Performance Analysis Errors**
   - Verify data file path and format
   - Check date range is within available data
   - Ensure CSV format matches expected structure

2. **Deployment Issues**
   - Use deployment project for QuantConnect push
   - Verify no special characters in files
   - Check main.py syntax and imports

3. **Data Issues**
   - Update SPY data file regularly
   - Verify TradingView export format
   - Check for missing dates in data range

### Quick Fixes
```bash
# Verify data file
head -5 data/spy/SPY_DAILY_1993-01-29_2025-11-04.csv

# Test performance calculator
python calculate_performance.py --help

# Check deployment project status  
ls ../SPY_EMA_Strategy_DEPLOY/
```

---
**Next Steps:** See masterplan.md for future architecture planning and framework transformation roadmap.
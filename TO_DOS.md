# Trading Strategy Backtesting Plan

**Instructions:** 
- After successfully completing one of the steps, check the checkbox.
- Make sure to keep notes meaningful, and double check if they are neccessary.

## Backtesting Plan for MDB Strategy

Current Strategy: VolaBreakoutStrategy  
Symbol: MDB  
Period: 2024-01-01 to 2024-12-31  
Starting Capital: $100,000  

### Timeframe Testing Schedule

#### Minute-Based Timeframes
- [ ] 1 minute
- [ ] 5 minutes
- [ ] 10 minutes
- [ ] 15 minutes
- [ ] 20 minutes
- [ ] 30 minutes
- [ ] 45 minutes

#### Hour-Based Timeframes
- [ ] 1 hour (60 minutes)
- [ ] 2 hours (120 minutes)
- [ ] 3 hours (180 minutes)
- [ ] 4 hours (240 minutes)
- [ ] 8 hours (480 minutes)

#### Daily Timeframe
- [ ] 1 day (1440 minutes)

### Testing Process for Each Timeframe

1. Update `TIMEFRAME_MINUTES` in `strategy_config.py`
3. Run `make push` to deploy to QuantConnect
4. Execute backtest on QuantConnect platform
5. Record results in Results Section below
6. Check off the corresponding timeframe above

---

## Results Section

### Completed Backtests

#### 15 Minutes (Baseline) ✓
- **Return**: TBD%
- **Max Drawdown**: TBD%
- **Sharpe Ratio**: TBD
- **Notes**: 
- **Version**:

#### 1 Minute
- **Return**: _%
- **Max Drawdown**: _%
- **Sharpe Ratio**: 
- **Notes**: 
- **Version**: 

#### 5 Minutes
- **Return**: _%
- **Max Drawdown**: _%
- **Sharpe Ratio**: 
- **Notes**: 
- **Version**: 

#### 10 Minutes
- **Return**: _%
- **Max Drawdown**: _%
- **Sharpe Ratio**: 
- **Notes**: 
- **Version**: 

#### 20 Minutes
- **Return**: _%
- **Max Drawdown**: _%
- **Sharpe Ratio**: 
- **Notes**: 
- **Version**: 

#### 30 Minutes
- **Return**: _%
- **Max Drawdown**: _%
- **Sharpe Ratio**: 
- **Notes**: 
- **Version**: 

#### 45 Minutes
- **Return**: _%
- **Max Drawdown**: _%
- **Sharpe Ratio**: 
- **Notes**: 
- **Version**: 

#### 1 Hour (60 Minutes)
- **Return**: _%
- **Max Drawdown**: _%
- **Sharpe Ratio**: 
- **Notes**: 
- **Version**: 

#### 2 Hours (120 Minutes)
- **Return**: _%
- **Max Drawdown**: _%
- **Sharpe Ratio**: 
- **Notes**: 
- **Version**: 

#### 3 Hours (180 Minutes)
- **Return**: _%
- **Max Drawdown**: _%
- **Sharpe Ratio**: 
- **Notes**: 
- **Version**: 

#### 4 Hours (240 Minutes)
- **Return**: _%
- **Max Drawdown**: _%
- **Sharpe Ratio**: 
- **Notes**: 
- **Version**: 

#### 8 Hours (480 Minutes)
- **Return**: _%
- **Max Drawdown**: _%
- **Sharpe Ratio**: 
- **Notes**: 
- **Version**: 

#### 1 Day (1440 Minutes)
- **Return**: _%
- **Max Drawdown**: _%
- **Sharpe Ratio**: 
- **Notes**: 
- **Version**: 

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

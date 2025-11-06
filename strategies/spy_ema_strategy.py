"""
SPY EMA Crossover Strategy

Strategy Rules:
- BUY SPY when close price crosses ABOVE EMA50
- SELL SPY when close price crosses BELOW EMA100  
- Position Size: 99% of available cash
- Timeframe: Daily

Entry: Price > EMA50
Exit: Price < EMA100
"""

from AlgorithmImports import *
from framework.interfaces import IStrategy


class SPYEMAStrategy(IStrategy):
    """SPY EMA Crossover Strategy Implementation"""
    
    def initialize(self, algorithm):
        """Initialize the SPY EMA strategy"""
        # Set algorithm framework settings
        algorithm.set_start_date(2024, 1, 1)   # Clean 2024 year
        algorithm.set_end_date(2024, 12, 31)   # Clean 2024 year  
        algorithm.set_cash(100_000)            # $100K starting capital
        
        # Add SPY with daily resolution
        self.spy = algorithm.add_equity("SPY", Resolution.DAILY).symbol
        
        # Create EMA indicators
        self.ema50 = algorithm.ema(self.spy, 50, Resolution.DAILY)
        self.ema100 = algorithm.ema(self.spy, 100, Resolution.DAILY)
        
        # Track our entry price for logging
        self.entry_price = None
        self.entry_time = None
        
        # Track SPY prices for buy-and-hold comparison
        self.spy_prices = []
        self.trading_days = []
        
        # Algorithm parameters
        self.allocation_percent = 0.99  # Use 99% to allow for fees
        
        # Warm up indicators (need 100 days for EMA100)
        algorithm.set_warm_up(105)  # Extra buffer for stability
        
        # Log strategy parameters
        algorithm.log(f" SPY EMA CROSSOVER STRATEGY INITIALIZED")
        algorithm.log(f"    Period: {algorithm.start_date} to {algorithm.end_date}")
        algorithm.log(f"    Starting Capital: ${algorithm.portfolio.cash:,.0f}")
        algorithm.log(f"    Entry: Price > EMA50, Exit: Price < EMA100")
        algorithm.log(f"    Allocation: {self.allocation_percent:.0%}")

    def on_data(self, algorithm, data):
        """Process market data for SPY EMA strategy"""
        # Skip if warming up or no data
        if algorithm.is_warming_up or not data.contains_key(self.spy):
            return
            
        # Skip if indicators not ready
        if not (self.ema50.is_ready and self.ema100.is_ready):
            return
            
        # Get current data - add safety check
        spy_data = data.get(self.spy)
        if spy_data is None:
            return
            
        current_price = spy_data.close
        
        # Track SPY prices for buy-and-hold calculation
        self.spy_prices.append(float(current_price))
        self.trading_days.append(algorithm.time)
        
        ema50_value = self.ema50.current.value
        ema100_value = self.ema100.current.value
        current_holdings = algorithm.portfolio[self.spy].quantity
        
        # ENTRY LOGIC: Buy when price crosses above EMA50 (and we're not already long)
        if current_holdings == 0:  # No position
            if current_price > ema50_value:
                # Calculate position size - use 99% of available cash
                available_cash = algorithm.portfolio.cash * self.allocation_percent
                quantity = int(available_cash / current_price)
                
                if quantity > 0:
                    algorithm.market_order(self.spy, quantity)
                    self.entry_price = current_price
                    self.entry_time = algorithm.time
                    
                    algorithm.log(f" BUY SIGNAL: {quantity:,} shares SPY @ ${current_price:.2f}")
                    algorithm.log(f"    EMA50: ${ema50_value:.2f} | EMA100: ${ema100_value:.2f}")
                    algorithm.log(f"    Position Value: ${quantity * current_price:,.0f}")
        
        # EXIT LOGIC: Sell when price crosses below EMA100 (and we have a position)
        elif current_holdings > 0:  # Have long position
            if current_price < ema100_value:
                # Close entire position
                algorithm.market_order(self.spy, -current_holdings)
                
                # Calculate trade performance
                if self.entry_price:
                    trade_return = (current_price - self.entry_price) / self.entry_price
                    trade_pnl = current_holdings * (current_price - self.entry_price)
                    hold_days = (algorithm.time - self.entry_time).days if self.entry_time else 0
                    
                    algorithm.log(f" SELL SIGNAL: {current_holdings:,} shares SPY @ ${current_price:.2f}")
                    algorithm.log(f"   EMA50: ${ema50_value:.2f} | EMA100: ${ema100_value:.2f}")
                    algorithm.log(f"   Trade Return: {trade_return:.2%} | P&L: ${trade_pnl:,.0f}")
                    algorithm.log(f"   Hold Period: {hold_days} days")
                    
                self.entry_price = None
                self.entry_time = None
        
        # Log daily status (only when we have a position or significant moves)
        if current_holdings > 0 or algorithm.time.day == 1:  # Monthly status updates
            portfolio_value = algorithm.portfolio.total_portfolio_value
            unrealized_pnl = 0
            if self.entry_price and current_holdings > 0:
                unrealized_pnl = current_holdings * (current_price - self.entry_price)
                
            algorithm.log(f" Status: Portfolio=${portfolio_value:,.0f} | SPY=${current_price:.2f} | "
                    f"EMA50={ema50_value:.2f} | EMA100={ema100_value:.2f} | "
                    f"Shares={current_holdings:,} | Unrealized=${unrealized_pnl:,.0f}")

    def on_end_of_algorithm(self, algorithm):
        """Called when the algorithm terminates - log final performance vs Buy & Hold"""
        final_value = algorithm.portfolio.total_portfolio_value
        strategy_return = (final_value - 1_000_000) / 1_000_000
        
        # Calculate Buy and Hold performance from price history
        if len(self.spy_prices) >= 2:
            start_price = self.spy_prices[0]
            end_price = self.spy_prices[-1]
            buy_hold_return = (end_price - start_price) / start_price
            
            # Calculate what the buy-and-hold value would be
            initial_investment = 1_000_000 * self.allocation_percent
            buy_hold_shares = initial_investment / start_price
            buy_hold_final_value = buy_hold_shares * end_price
            
            outperformance = strategy_return - buy_hold_return
            trading_days = len(self.spy_prices)
        else:
            buy_hold_return = 0
            outperformance = strategy_return
            buy_hold_final_value = 1_000_000
            start_price = end_price = 0
            trading_days = 0
        
        algorithm.log(f"\n BACKTEST COMPLETE - PERFORMANCE COMPARISON")
        algorithm.log(f"=" * 60)
        algorithm.log(f"    STRATEGY PERFORMANCE:")
        algorithm.log(f"      Starting Capital: $1,000,000")
        algorithm.log(f"      Final Portfolio Value: ${final_value:,.0f}")
        algorithm.log(f"      Total Return: {strategy_return:.2%}")
        algorithm.log(f"")
        algorithm.log(f"    BUY & HOLD BENCHMARK (SPY):")
        algorithm.log(f"      SPY Start Price: ${start_price:.2f}")
        algorithm.log(f"      SPY End Price: ${end_price:.2f}")
        algorithm.log(f"      Buy & Hold Return: {buy_hold_return:.2%}")
        algorithm.log(f"      Buy & Hold Final Value: ${buy_hold_final_value:,.0f}")
        algorithm.log(f"")
        algorithm.log(f"    COMPARISON:")
        if outperformance > 0:
            algorithm.log(f"      Strategy OUTPERFORMED by {outperformance:.2%}")
        elif outperformance < 0:
            algorithm.log(f"      Strategy UNDERPERFORMED by {abs(outperformance):.2%}")
        else:
            algorithm.log(f"      = Strategy matched Buy & Hold")
        algorithm.log(f"")
        algorithm.log(f"    TRADING STATISTICS:")
        algorithm.log(f"      Trading Days: {trading_days}")
        if trading_days > 0:
            annualized_strategy = ((final_value / 1_000_000) ** (252 / trading_days)) - 1
            annualized_buy_hold = ((1 + buy_hold_return) ** (252 / trading_days)) - 1
            algorithm.log(f"      Annualized Strategy Return: {annualized_strategy:.2%}")
            algorithm.log(f"      Annualized Buy & Hold Return: {annualized_buy_hold:.2%}")
        algorithm.log(f"=" * 60)
        
        # Final position status
        spy_holdings = algorithm.portfolio[self.spy].quantity
        if spy_holdings > 0:
            current_price = algorithm.securities[self.spy].close
            algorithm.log(f"    Final Position: {spy_holdings:,} shares @ ${current_price:.2f}")
        else:
            algorithm.log(f"    Final Position: CASH")


# For the active_strategy.py pattern, we also need to export the class as ActiveStrategy
class ActiveStrategy(SPYEMAStrategy):
    """Active strategy alias for SPY EMA Strategy"""
    pass
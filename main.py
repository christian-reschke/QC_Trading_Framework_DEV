# region imports
from AlgorithmImports import *
# endregion

class SPYEMACrossoverStrategy(QCAlgorithm):
    """
    SPY EMA Crossover Strategy - QuantConnect Implementation
    
    Strategy Rules:
    - BUY SPY when close price crosses ABOVE EMA50
    - SELL SPY when close price crosses BELOW EMA100  
    - Position Size: 100% of available cash
    - Timeframe: Daily
    """
    # test comment 2
    
    def initialize(self):
        # Set algorithm framework settings
        self.set_start_date(2025, 7, 1)   # Q3 2025 start
        self.set_end_date(2025, 9, 30)    # Q3 2025 end  
        self.set_cash(1_000_000)          # $1M starting capital
        
        # Add SPY with daily resolution
        self.spy = self.add_equity("SPY", Resolution.DAILY).symbol
        
        # Create EMA indicators
        self.ema50 = self.ema(self.spy, 50, Resolution.DAILY)
        self.ema100 = self.ema(self.spy, 100, Resolution.DAILY)
        
        # Track our entry price for logging
        self.entry_price = None
        self.entry_time = None
        
        # Algorithm parameters
        self.allocation_percent = 0.99  # Use 99% to allow for fees
        
        # Warm up indicators (need 100 days for EMA100)
        self.set_warm_up(105)  # Extra buffer for stability
        
        # Log strategy parameters
        self.log(f" SPY EMA CROSSOVER STRATEGY INITIALIZED")
        self.log(f"    Period: {self.start_date} to {self.end_date}")
        self.log(f"    Starting Capital: ${self.portfolio.cash:,.0f}")
        self.log(f"    Entry: Price > EMA50, Exit: Price < EMA100")
        self.log(f"    Allocation: {self.allocation_percent:.0%}")

    def on_data(self, data: Slice):
        # Skip if warming up or no data
        if self.is_warming_up or not data.contains_key(self.spy):
            return
            
        # Skip if indicators not ready
        if not (self.ema50.is_ready and self.ema100.is_ready):
            return
            
        # Get current data - add safety check
        spy_data = data.get(self.spy)
        if spy_data is None:
            return
            
        current_price = spy_data.close
        ema50_value = self.ema50.current.value
        ema100_value = self.ema100.current.value
        current_holdings = self.portfolio[self.spy].quantity
        
        # ENTRY LOGIC: Buy when price crosses above EMA50 (and we're not already long)
        if current_holdings == 0:  # No position
            if current_price > ema50_value:
                # Calculate position size - use 99% of available cash
                available_cash = self.portfolio.cash * self.allocation_percent
                quantity = int(available_cash / current_price)
                
                if quantity > 0:
                    self.market_order(self.spy, quantity)
                    self.entry_price = current_price
                    self.entry_time = self.time
                    
                    self.log(f" BUY SIGNAL: {quantity:,} shares SPY @ ${current_price:.2f}")
                    self.log(f"    EMA50: ${ema50_value:.2f} | EMA100: ${ema100_value:.2f}")
                    self.log(f"    Position Value: ${quantity * current_price:,.0f}")
        
        # EXIT LOGIC: Sell when price crosses below EMA100 (and we have a position)
        elif current_holdings > 0:  # Have long position
            if current_price < ema100_value:
                # Close entire position
                self.market_order(self.spy, -current_holdings)
                
                # Calculate trade performance
                if self.entry_price:
                    trade_return = (current_price - self.entry_price) / self.entry_price
                    trade_pnl = current_holdings * (current_price - self.entry_price)
                    hold_days = (self.time - self.entry_time).days if self.entry_time else 0
                    
                    self.log(f" SELL SIGNAL: {current_holdings:,} shares SPY @ ${current_price:.2f}")
                    self.log(f"   EMA50: ${ema50_value:.2f} | EMA100: ${ema100_value:.2f}")
                    self.log(f"   Trade Return: {trade_return:.2%} | P&L: ${trade_pnl:,.0f}")
                    self.log(f"   Hold Period: {hold_days} days")
                    
                self.entry_price = None
                self.entry_time = None
        
        # Log daily status (only when we have a position or significant moves)
        if current_holdings > 0 or self.time.day == 1:  # Monthly status updates
            portfolio_value = self.portfolio.total_portfolio_value
            unrealized_pnl = 0
            if self.entry_price and current_holdings > 0:
                unrealized_pnl = current_holdings * (current_price - self.entry_price)
                
            self.log(f" Status: Portfolio=${portfolio_value:,.0f} | SPY=${current_price:.2f} | "
                    f"EMA50=${ema50_value:.2f} | EMA100=${ema100_value:.2f} | "
                    f"Shares={current_holdings:,} | Unrealized=${unrealized_pnl:,.0f}")

    def on_end_of_algorithm(self):
        """Called when the algorithm terminates - log final performance"""
        final_value = self.portfolio.total_portfolio_value
        total_return = (final_value - 1_000_000) / 1_000_000
        
        self.log(f"\n BACKTEST COMPLETE!")
        self.log(f"    Starting Capital: $1,000,000")
        self.log(f"    Final Portfolio Value: ${final_value:,.0f}")
        self.log(f"    Total Return: {total_return:.2%}")
        self.log(f"    Strategy: Buy SPY > EMA50, Sell SPY < EMA100")
        
        # Final position status
        spy_holdings = self.portfolio[self.spy].quantity
        if spy_holdings > 0:
            current_price = self.securities[self.spy].close
            self.log(f"    Final Position: {spy_holdings:,} shares @ ${current_price:.2f}")
        else:
            self.log(f"    Final Position: CASH")

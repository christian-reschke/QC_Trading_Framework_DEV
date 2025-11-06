# region imports
from AlgorithmImports import *
import numpy as np
# endregion

class VolaBreakoutQCStrategy(QCAlgorithm):
    """
    Vola Breakout Strategy - QuantConnect Implementation
    
    Entry Conditions (ALL must be true):
    1. inTrend = price > ema and ema > ema[1]          # EMA trend filter
    2. isLowBBW = bbw < bbwThreshold                   # Low volatility (compression)
    3. breakAboveBB = close > bbUpper                  # Upper Bollinger Band breakout
    4. breakAboveRecentHigh = close > highest(high, 5)[1]  # Recent high momentum
    
    Exit Conditions:
    - Trailing stop loss: 4% below highest price since entry
    """
    
    def initialize(self):
        # Set algorithm settings
        self.set_start_date(2024, 1, 1)   # Full year 2024
        self.set_end_date(2024, 12, 31)    
        self.set_cash(1_000_000)          # $1M starting capital
        
        # Add SPY with daily resolution
        self.spy = self.add_equity("SPY", Resolution.DAILY).symbol
        
        # Technical indicators
        self.ema_period = 30
        self.bb_period = 20
        self.recent_high_period = 5
        
        # Create indicators
        self.ema = self.ema(self.spy, self.ema_period, Resolution.DAILY)
        self.bb = self.bb(self.spy, self.bb_period, 2.0, MovingAverageType.SIMPLE, Resolution.DAILY)
        
        # Manual calculation arrays for additional indicators
        self.price_history = RollingWindow[float](max(self.bb_period + 1, self.recent_high_period + 1))
        self.high_history = RollingWindow[float](self.recent_high_period + 1)
        self.ema_history = RollingWindow[float](2)  # For EMA trend check
        
        # Strategy parameters
        self.bbw_threshold = 0.12  # 12% BBW threshold
        self.trailing_stop_percent = 0.04  # 4% trailing stop
        self.allocation_percent = 0.99
        
        # Position tracking
        self.entry_price = None
        self.entry_time = None
        self.highest_price_since_entry = None
        self.trailing_stop_price = None
        
        # Performance tracking
        self.spy_prices = []
        self.trading_days = []
        self.trade_count = 0
        
        # Warm up period
        self.set_warm_up(max(self.bb_period, self.ema_period) + 10)
        
        # Log initialization
        self.log(f"VOLA BREAKOUT STRATEGY INITIALIZED")
        self.log(f"  Period: {self.start_date} to {self.end_date}")
        self.log(f"  EMA Period: {self.ema_period}")
        self.log(f"  BB Period: {self.bb_period}")
        self.log(f"  BBW Threshold: {self.bbw_threshold:.1%}")
        self.log(f"  Trailing Stop: {self.trailing_stop_percent:.1%}")

    def on_data(self, data: Slice):
        # Skip if warming up or no data
        if self.is_warming_up or not data.contains_key(self.spy):
            return
            
        # Get current data
        spy_data = data.get(self.spy)
        if spy_data is None:
            return
            
        current_price = spy_data.close
        current_high = spy_data.high
        
        # Update price history
        self.price_history.add(float(current_price))
        self.high_history.add(float(current_high))
        
        # Track for buy-and-hold comparison
        self.spy_prices.append(float(current_price))
        self.trading_days.append(self.time)
        
        # Wait for indicators to be ready
        if not (self.ema.is_ready and self.bb.is_ready):
            return
            
        # Update EMA history for trend check
        self.ema_history.add(float(self.ema.current.value))
        
        # Skip if we don't have enough history
        if self.price_history.count < max(self.bb_period, self.recent_high_period) + 1:
            return
        if self.ema_history.count < 2:
            return
            
        # Get indicator values
        ema_current = self.ema.current.value
        ema_previous = self.ema_history[1]
        bb_upper = self.bb.upper_band.current.value
        bb_lower = self.bb.lower_band.current.value
        bb_middle = self.bb.middle_band.current.value
        
        # Calculate Bollinger Band Width (BBW)
        bbw = (bb_upper - bb_lower) / bb_middle if bb_middle > 0 else 0
        
        # Calculate recent high (highest high of last 5 periods, excluding today)
        recent_highs = [self.high_history[i] for i in range(1, min(self.recent_high_period + 1, self.high_history.count))]
        recent_high = max(recent_highs) if recent_highs else 0
        
        current_holdings = self.portfolio[self.spy].quantity
        
        # ENTRY LOGIC - All 4 conditions must be true
        if current_holdings == 0:  # No position
            # Condition 1: EMA trend filter
            in_trend = current_price > ema_current and ema_current > ema_previous
            
            # Condition 2: Low BBW (volatility compression)
            is_low_bbw = bbw < self.bbw_threshold
            
            # Condition 3: Break above upper Bollinger Band
            break_above_bb = current_price > bb_upper
            
            # Condition 4: Break above recent high
            break_above_recent_high = current_price > recent_high
            
            # Log conditions for debugging (monthly)
            if self.time.day == 1 or (in_trend and is_low_bbw and break_above_bb and break_above_recent_high):
                self.log(f"Entry Conditions Check:")
                self.log(f"  Price: ${current_price:.2f} | EMA: ${ema_current:.2f} | EMA[-1]: ${ema_previous:.2f}")
                self.log(f"  BB Upper: ${bb_upper:.2f} | Recent High: ${recent_high:.2f}")
                self.log(f"  BBW: {bbw:.3f} (threshold: {self.bbw_threshold:.3f})")
                self.log(f"  Conditions: Trend={in_trend} | LowBBW={is_low_bbw} | BreakBB={break_above_bb} | BreakHigh={break_above_recent_high}")
            
            # Enter position if ALL conditions are met
            if in_trend and is_low_bbw and break_above_bb and break_above_recent_high:
                available_cash = self.portfolio.cash * self.allocation_percent
                quantity = int(available_cash / current_price)
                
                if quantity > 0:
                    self.market_order(self.spy, quantity)
                    self.entry_price = current_price
                    self.entry_time = self.time
                    self.highest_price_since_entry = current_price
                    self.trailing_stop_price = current_price * (1 - self.trailing_stop_percent)
                    self.trade_count += 1
                    
                    self.log(f"ENTRY #{self.trade_count}: {quantity:,} shares @ ${current_price:.2f}")
                    self.log(f"   BBW: {bbw:.3f} | Recent High: ${recent_high:.2f}")
                    self.log(f"   Initial Stop: ${self.trailing_stop_price:.2f}")
        
        # EXIT LOGIC - Trailing Stop
        elif current_holdings > 0:  # Have position
            # Update trailing stop
            if current_price > self.highest_price_since_entry:
                self.highest_price_since_entry = current_price
                new_stop = current_price * (1 - self.trailing_stop_percent)
                if new_stop > self.trailing_stop_price:
                    self.trailing_stop_price = new_stop
            
            # Check if stop is hit
            if current_price <= self.trailing_stop_price:
                # Close position
                self.market_order(self.spy, -current_holdings)
                
                # Calculate trade performance
                if self.entry_price:
                    trade_return = (current_price - self.entry_price) / self.entry_price
                    trade_pnl = current_holdings * (current_price - self.entry_price)
                    hold_days = (self.time - self.entry_time).days if self.entry_time else 0
                    
                    self.log(f"EXIT #{self.trade_count}: {current_holdings:,} shares @ ${current_price:.2f}")
                    self.log(f"   Entry: ${self.entry_price:.2f} | High: ${self.highest_price_since_entry:.2f}")
                    self.log(f"   Return: {trade_return:.2%} | P&L: ${trade_pnl:,.0f} | Days: {hold_days}")
                
                # Reset position tracking
                self.entry_price = None
                self.entry_time = None
                self.highest_price_since_entry = None
                self.trailing_stop_price = None
            
            # Log position status (weekly)
            elif self.time.weekday() == 0:  # Monday
                unrealized_pnl = current_holdings * (current_price - self.entry_price) if self.entry_price else 0
                self.log(f"Position: {current_holdings:,} shares | Price: ${current_price:.2f} | "
                        f"Stop: ${self.trailing_stop_price:.2f} | Unrealized: ${unrealized_pnl:,.0f}")

    def on_end_of_algorithm(self):
        """Final performance summary"""
        final_value = self.portfolio.total_portfolio_value
        strategy_return = (final_value - 1_000_000) / 1_000_000
        
        # Calculate Buy and Hold benchmark
        if len(self.spy_prices) >= 2:
            start_price = self.spy_prices[0]
            end_price = self.spy_prices[-1]
            buy_hold_return = (end_price - start_price) / start_price
            
            initial_investment = 1_000_000 * self.allocation_percent
            buy_hold_shares = initial_investment / start_price
            buy_hold_final_value = buy_hold_shares * end_price
            
            outperformance = strategy_return - buy_hold_return
        else:
            buy_hold_return = 0
            outperformance = strategy_return
            buy_hold_final_value = 1_000_000
            start_price = end_price = 0
        
        self.log(f"\nVOLA BREAKOUT STRATEGY - FINAL RESULTS")
        self.log(f"=" * 60)
        self.log(f"STRATEGY PERFORMANCE:")
        self.log(f"  Final Portfolio Value: ${final_value:,.0f}")
        self.log(f"  Total Return: {strategy_return:.2%}")
        self.log(f"  Total Trades: {self.trade_count}")
        self.log(f"")
        self.log(f"BUY & HOLD BENCHMARK:")
        self.log(f"  SPY: ${start_price:.2f} to ${end_price:.2f}")
        self.log(f"  Buy & Hold Return: {buy_hold_return:.2%}")
        self.log(f"  Buy & Hold Value: ${buy_hold_final_value:,.0f}")
        self.log(f"")
        self.log(f"COMPARISON:")
        if outperformance > 0:
            self.log(f"  Strategy OUTPERFORMED by {outperformance:.2%}")
        elif outperformance < 0:
            self.log(f"  Strategy UNDERPERFORMED by {abs(outperformance):.2%}")
        else:
            self.log(f"  Strategy MATCHED Buy & Hold")
        self.log(f"=" * 60)
        
        # Final position
        spy_holdings = self.portfolio[self.spy].quantity
        if spy_holdings > 0:
            current_price = self.securities[self.spy].close
            self.log(f"Final Position: {spy_holdings:,} shares @ ${current_price:.2f}")
        else:
            self.log(f"Final Position: CASH")
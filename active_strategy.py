"""
Vola Breakout Strategy - Dynamic Timeframe

Strategy Rules:
- Entry: inTrend AND isLowBBW AND breakAboveBB AND breakAboveRecentHigh
- Exit: Trailing stop loss
- Position Size: 99% of available cash
- Timeframe: Configurable via TIMEFRAME_MINUTES (using BarBuilder)

Entry Conditions:
1. inTrend = price > ema and ema > ema[1]          # EMA trend filter
2. isLowBBW = isReady and bbw < bbwThreshold       # Bollinger Band Width volatility filter
3. breakAboveBB = close > bbUpper                  # Upper Bollinger Band breakout
4. breakAboveRecentHigh = close > ta.highest(high, 5)[1]  # Recent high momentum confirmation

Exit: Trailing stop

Configuration: Change TIMEFRAME_MINUTES in the class to adjust timeframe
"""

from AlgorithmImports import *
from framework.interfaces import IStrategy
from framework.bar_builder import BarBuilder
from framework.logging_service import BacktestLogger
from strategy_config import (
    TIMEFRAME_MINUTES, START_DATE, END_DATE, STARTING_CAPITAL, 
    STRATEGY_VERSION, SYMBOL, LOGGING_ENABLED, RUN_ID, 
    LOG_TRADES, LOG_DAILY_PERFORMANCE, LOG_INDICATORS, LOG_ENTRY_CONDITIONS
)


class VolaBreakoutStrategy(IStrategy):
    """Volatility Breakout Strategy Implementation - Dynamic Timeframe"""
    
    def initialize(self, algorithm):
        """Initialize the strategy"""
        self.algorithm = algorithm
        
        # Set backtest period from centralized configuration
        start_parts = START_DATE.split("-")
        end_parts = END_DATE.split("-")
        algorithm.SetStartDate(int(start_parts[0]), int(start_parts[1]), int(start_parts[2]))
        algorithm.SetEndDate(int(end_parts[0]), int(end_parts[1]), int(end_parts[2]))
        algorithm.SetCash(STARTING_CAPITAL)
        
        # Use MINUTE resolution as base for custom bar building
        self.symbol = algorithm.AddEquity(SYMBOL, Resolution.MINUTE).Symbol
        
        # Initialize bar builder with dynamic timeframe
        self.bar_builder = BarBuilder(algorithm, self.symbol, TIMEFRAME_MINUTES, self.on_bar_completed)
        
        # Strategy parameters
        self.ema_period = 50
        self.bb_period = 20
        self.bb_std = 2
        self.bbw_threshold = 0.1  # BBW threshold for low volatility
        self.recent_high_period = 5
        self.trail_percent = 0.05  # 5% trailing stop
        
        # Manual indicator tracking (since we use custom bars)
        self.ema_values = []
        self.bb_values = []  # Store tuples of (upper, middle, lower)
        self.price_history = []
        self.high_history = []
        
        # State tracking
        self.position_entry_price = None
        self.highest_price_since_entry = None
        self.entry_time = None
        
        # Initialize logging service
        self.logger = BacktestLogger(
            algorithm=algorithm,
            run_id=RUN_ID,
            enabled=LOGGING_ENABLED
        )
        self.logger.set_metadata(
            strategy_name="VolaBreakoutStrategy",
            symbol=SYMBOL,
            timeframe_minutes=TIMEFRAME_MINUTES
        )
        
        algorithm.Log(f"VOLA BREAKOUT STRATEGY ({TIMEFRAME_MINUTES}MIN) INITIALIZED - Bar Builder: {TIMEFRAME_MINUTES} minutes")
        algorithm.Log(f"STRATEGY_VERSION: {STRATEGY_VERSION}")  # Version verification
        algorithm.SetRuntimeStatistic("Strategy Version", STRATEGY_VERSION)
        algorithm.Log(f"Strategy Parameters: EMA{self.ema_period}, BB{self.bb_period}, Trail{self.trail_percent:.1%}")

    def on_data(self, algorithm, data):
        """Process new market data - feeds into bar builder"""
        if not data.ContainsKey(self.symbol) or data[self.symbol] is None:
            return
            
        if algorithm.IsWarmingUp:
            return
        
        # Update the bar builder with new minute data
        self.bar_builder.update(data)

    def on_bar_completed(self, bar):
        """Handle completed bar (timeframe determined by TIMEFRAME_MINUTES)"""
        algorithm = self.algorithm
        current_price = bar.Close
        current_holdings = algorithm.Portfolio[self.symbol].Quantity
        
        # DEBUG: Log every bar completion
        algorithm.Log(f"{TIMEFRAME_MINUTES}MIN BAR COMPLETED: {bar.Time} | O:{bar.Open:.2f} H:{bar.High:.2f} L:{bar.Low:.2f} C:{bar.Close:.2f}")
        
        # Update price and high history
        self.price_history.append(current_price)
        self.high_history.append(bar.High)
        
        # Keep only needed history (for indicators and lookbacks)
        max_history = max(self.ema_period, self.bb_period) + self.recent_high_period + 10
        if len(self.price_history) > max_history:
            self.price_history = self.price_history[-max_history:]
            self.high_history = self.high_history[-max_history:]
        
        # Update indicators
        self._update_indicators(bar)
        
        # Log indicators if enabled
        if LOG_INDICATORS and len(self.ema_values) > 0 and len(self.bb_values) > 0:
            bb_upper, bb_middle, bb_lower = self.bb_values[-1]
            bb_width = (bb_upper - bb_lower) / bb_middle if bb_middle > 0 else 0
            
            indicator_data = {
                "ema": self.ema_values[-1],
                "bb_upper": bb_upper,
                "bb_middle": bb_middle,
                "bb_lower": bb_lower,
                "bb_width": bb_width,
                "price": current_price,
                "high": bar.High,
                "low": bar.Low,
                "volume": bar.Volume if hasattr(bar, 'Volume') else 0
            }
            self.logger.log_indicators(indicator_data)
        
        # Log daily performance (only once per day)
        if LOG_DAILY_PERFORMANCE and algorithm.Time.hour == 16 and algorithm.Time.minute == 0:
            self.logger.log_daily_performance()
        
        # Plot current data for debugging
        self._plot_debug_data(algorithm, current_price, bar)
        
        # Entry logic
        if current_holdings == 0:
            entry_conditions = self._get_entry_conditions_dict(current_price, bar)
            entry_signal = self._check_entry_conditions(current_price, bar)
            
            # Log entry conditions if enabled
            if LOG_ENTRY_CONDITIONS:
                self.logger.log_entry_conditions(entry_conditions, entry_signal)
            
            if entry_signal:
                # Calculate position size (99% of portfolio)
                cash_to_invest = algorithm.Portfolio.Cash * 0.99
                shares_to_buy = int(cash_to_invest / current_price)
                
                if shares_to_buy > 0:
                    algorithm.MarketOrder(self.symbol, shares_to_buy)
                    self.position_entry_price = current_price
                    self.highest_price_since_entry = current_price
                    self.entry_time = algorithm.Time
                    
                    # Log trade entry
                    if LOG_TRADES:
                        self.logger.log_trade_entry(
                            symbol=self.symbol,
                            quantity=shares_to_buy,
                            price=current_price,
                            entry_conditions=entry_conditions
                        )
                    
                    algorithm.Log(f"ENTRY: Bought {shares_to_buy} shares of {SYMBOL} at ${current_price:.2f} ({TIMEFRAME_MINUTES}min bar)")
        
        # Exit logic (trailing stop)
        elif current_holdings > 0:
            if self._check_exit_conditions(current_price):
                # Calculate hold period
                hold_days = None
                if self.entry_time:
                    hold_days = (algorithm.Time - self.entry_time).days
                
                # Log trade exit before liquidating
                if LOG_TRADES:
                    self.logger.log_trade_exit(
                        symbol=self.symbol,
                        quantity=current_holdings,
                        price=current_price,
                        entry_price=self.position_entry_price,
                        hold_days=hold_days,
                        exit_reason="trailing_stop"
                    )
                
                algorithm.Liquidate(self.symbol)
                algorithm.Log(f"EXIT: Sold {SYMBOL} at ${current_price:.2f} (Entry: ${self.position_entry_price:.2f}) ({TIMEFRAME_MINUTES}min bar)")
                self.position_entry_price = None
                self.highest_price_since_entry = None
                self.entry_time = None
            else:
                # Update highest price for trailing stop
                if current_price > self.highest_price_since_entry:
                    self.highest_price_since_entry = current_price

    def _update_indicators(self, bar):
        """Update EMA and Bollinger Bands manually"""
        if len(self.price_history) < 2:
            return
            
        # Update EMA
        if len(self.ema_values) == 0:
            # First EMA value is just the price
            self.ema_values.append(bar.Close)
        else:
            # EMA formula: EMA = (Price * (2/(period+1))) + (Previous EMA * (1 - (2/(period+1))))
            multiplier = 2.0 / (self.ema_period + 1)
            ema = (bar.Close * multiplier) + (self.ema_values[-1] * (1 - multiplier))
            self.ema_values.append(ema)
        
        # Update Bollinger Bands (need at least bb_period values)
        if len(self.price_history) >= self.bb_period:
            recent_prices = self.price_history[-self.bb_period:]
            sma = sum(recent_prices) / len(recent_prices)
            
            # Calculate standard deviation
            variance = sum((price - sma) ** 2 for price in recent_prices) / len(recent_prices)
            std_dev = variance ** 0.5
            
            bb_upper = sma + (self.bb_std * std_dev)
            bb_lower = sma - (self.bb_std * std_dev)
            bb_middle = sma
            
            self.bb_values.append((bb_upper, bb_middle, bb_lower))
            
            # Keep reasonable history
            if len(self.bb_values) > 100:
                self.bb_values = self.bb_values[-50:]
        
        # Keep reasonable EMA history
        if len(self.ema_values) > 100:
            self.ema_values = self.ema_values[-50:]

    def _check_entry_conditions(self, current_price, bar):
        """Check all entry conditions"""
        # Need sufficient data for all indicators
        if len(self.ema_values) < 2 or len(self.bb_values) < 1:
            return False
        
        if len(self.price_history) < self.recent_high_period + 2:
            return False
        
        # 1. inTrend = price > ema and price rising
        ema_current = self.ema_values[-1]
        prev_price = self.price_history[-2]
        in_trend = current_price > ema_current and current_price > prev_price
        
        # 2. isLowBBW = bbw < bbwThreshold
        bb_upper, bb_middle, bb_lower = self.bb_values[-1]
        bb_width = (bb_upper - bb_lower) / bb_middle if bb_middle > 0 else 1.0
        is_low_bbw = bb_width < self.bbw_threshold
        
        # 3. breakAboveBB = close > bbUpper
        break_above_bb = current_price > bb_upper
        
        # 4. breakAboveRecentHigh = close > highest(high, 5)[1]
        if len(self.high_history) >= self.recent_high_period + 1:
            recent_highs = self.high_history[-(self.recent_high_period+1):-1]  # Exclude current bar
            recent_high = max(recent_highs)
            break_above_recent_high = current_price > recent_high
        else:
            break_above_recent_high = False
        
        # All conditions must be true
        entry_signal = in_trend and is_low_bbw and break_above_bb and break_above_recent_high
        
        if entry_signal:
            self.algorithm.Log(f"ENTRY SIGNAL ({TIMEFRAME_MINUTES}min): Price=${current_price:.2f}, EMA=${ema_current:.2f}, BBW={bb_width:.3f}, BB_Upper=${bb_upper:.2f}, Recent_High=${recent_high:.2f}")
        
        return entry_signal

    def _get_entry_conditions_dict(self, current_price, bar):
        """Get all entry conditions as a dictionary for logging"""
        if len(self.ema_values) < 2 or len(self.bb_values) < 1:
            return {}
        
        if len(self.price_history) < self.recent_high_period + 2:
            return {}
        
        # Calculate all conditions
        ema_current = self.ema_values[-1]
        prev_price = self.price_history[-2]
        bb_upper, bb_middle, bb_lower = self.bb_values[-1]
        bb_width = (bb_upper - bb_lower) / bb_middle if bb_middle > 0 else 1.0
        
        # Calculate recent high
        recent_high = 0
        if len(self.high_history) >= self.recent_high_period + 1:
            recent_highs = self.high_history[-(self.recent_high_period+1):-1]
            recent_high = max(recent_highs)
        
        # Individual conditions
        in_trend = current_price > ema_current and current_price > prev_price
        is_low_bbw = bb_width < self.bbw_threshold
        break_above_bb = current_price > bb_upper
        break_above_recent_high = current_price > recent_high
        
        return {
            "current_price": current_price,
            "ema_current": ema_current,
            "prev_price": prev_price,
            "bb_upper": bb_upper,
            "bb_middle": bb_middle,
            "bb_lower": bb_lower,
            "bb_width": bb_width,
            "bbw_threshold": self.bbw_threshold,
            "recent_high": recent_high,
            "in_trend": in_trend,
            "is_low_bbw": is_low_bbw,
            "break_above_bb": break_above_bb,
            "break_above_recent_high": break_above_recent_high,
            "all_conditions_met": in_trend and is_low_bbw and break_above_bb and break_above_recent_high
        }

    def _plot_debug_data(self, algorithm, current_price, bar):
        """Plot debugging data to charts"""
        if len(self.ema_values) == 0 or len(self.bb_values) == 0:
            return
            
        # Plot Price & Indicators
        algorithm.Plot("Price & Indicators", f"{SYMBOL} Price", current_price)
        algorithm.Plot("Price & Indicators", "EMA50", self.ema_values[-1])
        
        bb_upper, bb_middle, bb_lower = self.bb_values[-1]
        algorithm.Plot("Price & Indicators", "BB Upper", bb_upper)
        algorithm.Plot("Price & Indicators", "BB Lower", bb_lower)
        algorithm.Plot("Price & Indicators", "BB Middle", bb_middle)
        
        # Plot Bollinger Band Width
        bb_width = (bb_upper - bb_lower) / bb_middle if bb_middle > 0 else 0
        algorithm.Plot("Bollinger Band Width", "BBW", bb_width)
        algorithm.Plot("Bollinger Band Width", "BBW Threshold", self.bbw_threshold)
        
        # Plot Entry Conditions (as flags when true)
        try:
            if len(self.price_history) >= self.recent_high_period + 2:
                # Check individual conditions
                ema_current = self.ema_values[-1]
                prev_price = self.price_history[-2]
                in_trend = current_price > ema_current and current_price > prev_price
                
                is_low_bbw = bb_width < self.bbw_threshold
                break_above_bb = current_price > bb_upper
                
                if len(self.high_history) >= self.recent_high_period + 1:
                    recent_highs = self.high_history[-(self.recent_high_period+1):-1]
                    recent_high = max(recent_highs)
                    break_above_recent_high = current_price > recent_high
                else:
                    break_above_recent_high = False
                
                # Plot flags (1 when condition is true, 0 otherwise)
                algorithm.Plot("Entry Conditions", "Trend OK", 1 if in_trend else 0)
                algorithm.Plot("Entry Conditions", "Low Vol OK", 1 if is_low_bbw else 0)
                algorithm.Plot("Entry Conditions", "BB Breakout OK", 1 if break_above_bb else 0)
                algorithm.Plot("Entry Conditions", "Momentum OK", 1 if break_above_recent_high else 0)
                
                # Overall entry signal
                entry_signal = in_trend and is_low_bbw and break_above_bb and break_above_recent_high
                algorithm.Plot("Entry Conditions", "Entry Signal", 1 if entry_signal else 0)
                
        except Exception as e:
            # Don't let plotting errors break the strategy
            pass
        
        # Plot Position & Performance
        position_value = algorithm.Portfolio[self.symbol].HoldingsValue
        cash = algorithm.Portfolio.Cash
        total_portfolio = algorithm.Portfolio.TotalPortfolioValue
        
        algorithm.Plot("Position & Performance", "Position Value", position_value)
        algorithm.Plot("Position & Performance", "Cash", cash)
        algorithm.Plot("Position & Performance", "Total Portfolio", total_portfolio)

    def _check_exit_conditions(self, current_price):
        """Check trailing stop exit condition"""
        if self.highest_price_since_entry is None:
            return False
        
        # Trailing stop: exit if price drops more than trail_percent from highest price
        stop_price = self.highest_price_since_entry * (1 - self.trail_percent)
        return current_price <= stop_price

    def on_end_of_algorithm(self, algorithm):
        """Called at the end of the algorithm"""
        final_portfolio_value = algorithm.Portfolio.TotalPortfolioValue
        algorithm.Log(f"Vola Breakout Strategy ({TIMEFRAME_MINUTES}min) completed - Final Portfolio Value: ${final_portfolio_value:,.2f}")
        
        # Save all logged data to object store
        if LOGGING_ENABLED:
            algorithm.Log("Saving backtest data to object store...")
            saved = self.logger.save_to_object_store()
            if saved:
                algorithm.Log(f"Backtest data saved successfully. Run ID: {self.logger.run_id}")
            else:
                algorithm.Log("Failed to save backtest data to object store")
        else:
            algorithm.Log("Logging disabled - no data saved to object store")


# Create the ActiveStrategy alias for the framework
ActiveStrategy = VolaBreakoutStrategy
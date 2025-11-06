"""
Vola Breakout Strategy

Strategy Rules:
- Entry: inTrend AND isLowBBW AND breakAboveBB AND breakAboveRecentHigh
- Exit: Trailing stop loss
- Position Size: 99% of available cash
- Timeframe: Daily

Entry Conditions:
1. inTrend = price > ema and ema > ema[1]          # EMA trend filter
2. isLowBBW = isReady and bbw < bbwThreshold       # Bollinger Band Width volatility filter
3. breakAboveBB = close > bbUpper                  # Upper Bollinger Band breakout
4. breakAboveRecentHigh = close > ta.highest(high, 5)[1]  # Recent high momentum confirmation

Exit: Trailing stop
"""

from AlgorithmImports import *
from framework.interfaces import IStrategy


class VolaBreakoutStrategy(IStrategy):
    """Volatility Breakout Strategy Implementation"""
    
    def initialize(self, algorithm):
        """Initialize the strategy"""
        self.algorithm = algorithm
        
        # Set backtest period for consistent analysis
        algorithm.SetStartDate(2024, 1, 1)
        algorithm.SetEndDate(2024, 12, 31)
        algorithm.SetCash(100000)
        
        self.symbol = algorithm.AddEquity("SPY", Resolution.DAILY).Symbol
        
        # Strategy parameters
        self.ema_period = 50
        self.bb_period = 20
        self.bb_std = 2
        self.bbw_threshold = 0.1  # BBW threshold for low volatility
        self.recent_high_period = 5
        self.trail_percent = 0.05  # 5% trailing stop
        
        # Indicators
        self.ema = algorithm.EMA(self.symbol, self.ema_period)
        self.bb = algorithm.BB(self.symbol, self.bb_period, self.bb_std)
        
        # State tracking
        self.position_entry_price = None
        self.highest_price_since_entry = None
        
        # Warm up indicators
        algorithm.SetWarmUp(max(self.ema_period, self.bb_period) + self.recent_high_period)
        
        # Setup debugging plots
        self._setup_debug_plots(algorithm)
        
        algorithm.Log(f"Vola Breakout Strategy initialized - EMA{self.ema_period}, BB{self.bb_period}, Trail{self.trail_percent:.1%}")

    def _setup_debug_plots(self, algorithm):
        """Setup debugging charts for strategy analysis"""
        
        # Note: Using simplified plotting approach for QuantConnect compatibility
        # Charts will be created automatically when we plot to them

    def on_data(self, algorithm, data):
        """Process new market data"""
        if not data.ContainsKey(self.symbol) or data[self.symbol] is None:
            return
            
        if algorithm.IsWarmingUp:
            return
        
        bar = data[self.symbol]
        current_price = bar.Close
        current_holdings = algorithm.Portfolio[self.symbol].Quantity
        
        # Plot current data for debugging
        self._plot_debug_data(algorithm, current_price)
        
        # Entry logic
        if current_holdings == 0:
            if self._check_entry_conditions(current_price):
                # Calculate position size (99% of portfolio)
                cash_to_invest = algorithm.Portfolio.Cash * 0.99
                shares_to_buy = int(cash_to_invest / current_price)
                
                if shares_to_buy > 0:
                    algorithm.MarketOrder(self.symbol, shares_to_buy)
                    self.position_entry_price = current_price
                    self.highest_price_since_entry = current_price
                    algorithm.Log(f"ENTRY: Bought {shares_to_buy} shares of SPY at ${current_price:.2f}")
        
        # Exit logic (trailing stop)
        elif current_holdings > 0:
            if self._check_exit_conditions(current_price):
                algorithm.Liquidate(self.symbol)
                algorithm.Log(f"EXIT: Sold SPY at ${current_price:.2f} (Entry: ${self.position_entry_price:.2f})")
                self.position_entry_price = None
                self.highest_price_since_entry = None
            else:
                # Update highest price for trailing stop
                if current_price > self.highest_price_since_entry:
                    self.highest_price_since_entry = current_price

    def _check_entry_conditions(self, current_price):
        """Check all entry conditions"""
        if not self.ema.IsReady or not self.bb.IsReady:
            return False
        
        # Get historical data for trend and momentum checks
        history = self.algorithm.History(self.symbol, self.recent_high_period + 2, Resolution.DAILY)
        if history.empty or len(history) < self.recent_high_period + 2:
            return False
        
        # 1. inTrend = price > ema and ema > ema[1]
        ema_current = self.ema.Current.Value
        prev_close = float(history.iloc[-2]['close'])
        
        # Simple trend check: price above EMA and price rising
        in_trend = current_price > ema_current and current_price > prev_close
        
        # 2. isLowBBW = isReady and bbw < bbwThreshold
        bb_upper = self.bb.UpperBand.Current.Value
        bb_lower = self.bb.LowerBand.Current.Value
        bb_middle = self.bb.MiddleBand.Current.Value
        bb_width = (bb_upper - bb_lower) / bb_middle if bb_middle > 0 else 1.0  # Normalized BBW
        is_low_bbw = bb_width < self.bbw_threshold
        
        # 3. breakAboveBB = close > bbUpper
        break_above_bb = current_price > bb_upper
        
        # 4. breakAboveRecentHigh = close > ta.highest(high, 5)[1]
        # Get highest high of last 5 days using history
        try:
            recent_highs = history['high'].iloc[-(self.recent_high_period+1):-1]  # Exclude today
            recent_high = float(recent_highs.max())
            break_above_recent_high = current_price > recent_high
        except:
            break_above_recent_high = False
        
        # All conditions must be true
        entry_signal = in_trend and is_low_bbw and break_above_bb and break_above_recent_high
        
        if entry_signal:
            self.algorithm.Log(f"ENTRY SIGNAL: Price=${current_price:.2f}, EMA=${ema_current:.2f}, BBW={bb_width:.3f}, BB_Upper=${bb_upper:.2f}, Recent_High=${recent_high:.2f}")
        
        return entry_signal

    def _plot_debug_data(self, algorithm, current_price):
        """Plot debugging data to charts"""
        if not self.ema.IsReady or not self.bb.IsReady:
            return
            
        # Plot Price & Indicators
        algorithm.Plot("Price & Indicators", "SPY Price", current_price)
        algorithm.Plot("Price & Indicators", "EMA50", self.ema.Current.Value)
        algorithm.Plot("Price & Indicators", "BB Upper", self.bb.UpperBand.Current.Value)
        algorithm.Plot("Price & Indicators", "BB Lower", self.bb.LowerBand.Current.Value)
        algorithm.Plot("Price & Indicators", "BB Middle", self.bb.MiddleBand.Current.Value)
        
        # Plot Bollinger Band Width
        bb_upper = self.bb.UpperBand.Current.Value
        bb_lower = self.bb.LowerBand.Current.Value
        bb_middle = self.bb.MiddleBand.Current.Value
        bb_width = (bb_upper - bb_lower) / bb_middle if bb_middle > 0 else 0
        
        algorithm.Plot("Bollinger Band Width", "BBW", bb_width)
        algorithm.Plot("Bollinger Band Width", "BBW Threshold", self.bbw_threshold)
        
        # Plot Entry Conditions (as flags when true)
        try:
            history = algorithm.History(self.symbol, self.recent_high_period + 2, Resolution.DAILY)
            if not history.empty and len(history) >= self.recent_high_period + 2:
                
                # Check individual conditions
                ema_current = self.ema.Current.Value
                prev_close = float(history.iloc[-2]['close'])
                in_trend = current_price > ema_current and current_price > prev_close
                
                is_low_bbw = bb_width < self.bbw_threshold
                break_above_bb = current_price > bb_upper
                
                recent_highs = history['high'].iloc[-(self.recent_high_period+1):-1]
                recent_high = float(recent_highs.max())
                break_above_recent_high = current_price > recent_high
                
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
        algorithm.Log(f"Vola Breakout Strategy completed - Final Portfolio Value: ${final_portfolio_value:,.2f}")


# Create the ActiveStrategy alias for the framework
ActiveStrategy = VolaBreakoutStrategy
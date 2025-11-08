"""
Flexible Bar Builder for Custom Timeframes

Enables strategies to use custom timeframes (e.g., 15-minute, 4-hour, etc.)
instead of being locked to QuantConnect's fixed resolutions.

Usage:
    bar_builder = BarBuilder(algorithm, symbol, minutes=15)
    bar_builder.on_bar_updated = self.on_custom_bar
"""

from AlgorithmImports import *
from typing import Callable, Optional
from datetime import timedelta


class CustomBar:
    """Custom bar data structure"""
    
    def __init__(self, time: datetime, open_price: float, high: float, low: float, close: float, volume: int = 0):
        self.Time = time
        self.Open = open_price
        self.High = high
        self.Low = low
        self.Close = close
        self.Volume = volume
        
    def __str__(self):
        return f"CustomBar({self.Time}: O={self.Open:.2f}, H={self.High:.2f}, L={self.Low:.2f}, C={self.Close:.2f})"


class BarBuilder:
    """
    Flexible bar builder that consolidates minute data into custom timeframes
    
    Supports:
    - Any minute-based timeframe (1, 5, 15, 30, 60, 240, etc.)
    - Proper OHLCV aggregation
    - Event-driven bar completion callbacks
    - Multiple timeframes simultaneously
    """
    
    def __init__(self, algorithm, symbol: Symbol, minutes: int, on_bar_updated: Optional[Callable] = None):
        """
        Initialize the bar builder
        
        Args:
            algorithm: QuantConnect algorithm instance
            symbol: The symbol to track
            minutes: Timeframe in minutes (1, 5, 15, 30, 60, 240, etc.)
            on_bar_updated: Callback function when a new bar is completed
        """
        self.algorithm = algorithm
        self.symbol = symbol
        self.minutes = minutes
        self.on_bar_updated = on_bar_updated
        
        # Current bar being built
        self.current_bar: Optional[CustomBar] = None
        self.bar_start_time: Optional[datetime] = None
        
        # Bar history for indicators
        self.bars = []
        self.max_history = 1000  # Keep last 1000 bars
        
        # Subscribe to minute data
        self._setup_data_subscription()
        
        algorithm.Log(f"BarBuilder initialized: {symbol} {minutes}-minute bars")
    
    def _setup_data_subscription(self):
        """Setup minute-level data subscription"""
        # Add equity with minute resolution for bar building
        self.algorithm.AddEquity(str(self.symbol), Resolution.MINUTE)
        
    def _get_bar_start_time(self, current_time: datetime) -> datetime:
        """Calculate the start time for the current bar period"""
        # Round down to the nearest bar interval
        total_minutes = current_time.hour * 60 + current_time.minute
        bar_minute = (total_minutes // self.minutes) * self.minutes
        
        return current_time.replace(
            hour=bar_minute // 60,
            minute=bar_minute % 60,
            second=0,
            microsecond=0
        )
    
    def update(self, data):
        """Update the bar builder with new minute data"""
        if not data.ContainsKey(self.symbol):
            return
            
        trade_bar = data[self.symbol]
        if trade_bar is None:
            return
            
        current_time = trade_bar.Time
        bar_start = self._get_bar_start_time(current_time)
        
        # Check if we need to start a new bar
        if self.bar_start_time != bar_start:
            # Complete the previous bar if it exists
            if self.current_bar is not None:
                self._complete_bar()
            
            # Start a new bar
            self._start_new_bar(bar_start, trade_bar)
        else:
            # Update the current bar
            self._update_current_bar(trade_bar)
    
    def _start_new_bar(self, bar_start: datetime, trade_bar):
        """Start building a new bar"""
        self.bar_start_time = bar_start
        self.current_bar = CustomBar(
            time=bar_start,
            open_price=trade_bar.Open,
            high=trade_bar.High,
            low=trade_bar.Low,
            close=trade_bar.Close,
            volume=trade_bar.Volume
        )
    
    def _update_current_bar(self, trade_bar):
        """Update the current bar with new data"""
        if self.current_bar is None:
            return
            
        # Update OHLCV
        self.current_bar.High = max(self.current_bar.High, trade_bar.High)
        self.current_bar.Low = min(self.current_bar.Low, trade_bar.Low)
        self.current_bar.Close = trade_bar.Close
        self.current_bar.Volume += trade_bar.Volume
    
    def _complete_bar(self):
        """Complete the current bar and notify callback"""
        if self.current_bar is None:
            return
            
        # Add to history
        self.bars.append(self.current_bar)
        
        # Limit history size
        if len(self.bars) > self.max_history:
            self.bars = self.bars[-self.max_history:]
        
        # Notify callback
        if self.on_bar_updated:
            self.on_bar_updated(self.current_bar)
        
        self.algorithm.Log(f"Completed {self.minutes}m bar: {self.current_bar}")
    
    def get_last_bars(self, count: int = 1):
        """Get the last N completed bars"""
        if count == 1:
            return self.bars[-1] if self.bars else None
        return self.bars[-count:] if len(self.bars) >= count else self.bars
    
    def get_current_bar(self) -> Optional[CustomBar]:
        """Get the current bar being built (incomplete)"""
        return self.current_bar
    
    def is_ready(self, min_bars: int = 1) -> bool:
        """Check if we have enough bars for analysis"""
        return len(self.bars) >= min_bars


class MultiTimeframeBarBuilder:
    """
    Manages multiple bar builders for different timeframes simultaneously
    
    Example:
        mtf = MultiTimeframeBarBuilder(algorithm, symbol)
        mtf.add_timeframe(15, self.on_15min_bar)  # 15-minute bars
        mtf.add_timeframe(60, self.on_1hour_bar)  # 1-hour bars
        mtf.add_timeframe(240, self.on_4hour_bar) # 4-hour bars
    """
    
    def __init__(self, algorithm, symbol: Symbol):
        self.algorithm = algorithm
        self.symbol = symbol
        self.builders = {}  # timeframe -> BarBuilder
        
    def add_timeframe(self, minutes: int, callback: Callable):
        """Add a new timeframe to track"""
        self.builders[minutes] = BarBuilder(
            self.algorithm, 
            self.symbol, 
            minutes, 
            callback
        )
        
    def update(self, data):
        """Update all bar builders"""
        for builder in self.builders.values():
            builder.update(data)
            
    def get_builder(self, minutes: int) -> Optional[BarBuilder]:
        """Get a specific timeframe builder"""
        return self.builders.get(minutes)
        
    def get_timeframes(self) -> list:
        """Get all active timeframes"""
        return list(self.builders.keys())


# Convenience functions for common timeframes
def create_5min_builder(algorithm, symbol: Symbol, callback: Callable) -> BarBuilder:
    """Create a 5-minute bar builder"""
    return BarBuilder(algorithm, symbol, 5, callback)

def create_15min_builder(algorithm, symbol: Symbol, callback: Callable) -> BarBuilder:
    """Create a 15-minute bar builder"""
    return BarBuilder(algorithm, symbol, 15, callback)

def create_1hour_builder(algorithm, symbol: Symbol, callback: Callable) -> BarBuilder:
    """Create a 1-hour bar builder"""
    return BarBuilder(algorithm, symbol, 60, callback)

def create_4hour_builder(algorithm, symbol: Symbol, callback: Callable) -> BarBuilder:
    """Create a 4-hour bar builder"""
    return BarBuilder(algorithm, symbol, 240, callback)

def create_daily_builder(algorithm, symbol: Symbol, callback: Callable) -> BarBuilder:
    """Create a daily bar builder (1440 minutes)"""
    return BarBuilder(algorithm, symbol, 1440, callback)
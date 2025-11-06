"""
EMA-based entry modules
Converts C# EMA50Entry, EMA100Entry patterns to flexible Python
"""
from framework.interfaces import IEntryModule
from modules.indicators import ema_is_rising, price_crosses_above_ema, golden_cross
from typing import Dict, Any, List


class EMAEntry(IEntryModule):
    """
    Flexible EMA entry module - replaces separate EMA50Entry, EMA100Entry classes
    Can handle any EMA period and multiple conditions
    """
    
    def __init__(self, period: int = 50, require_rising: bool = True, require_price_above: bool = True):
        """
        Initialize EMA entry module
        Args:
            period: EMA period (50, 100, 200, etc.)
            require_rising: Require EMA to be rising
            require_price_above: Require price to cross above EMA
        """
        self.period = period
        self.require_rising = require_rising
        self.require_price_above = require_price_above
        self.name = f"EMA{period}Entry"
    
    def should_enter(self, data: Dict[str, Any]) -> bool:
        """
        Check if EMA entry conditions are met
        Args:
            data: Dictionary containing 'prices' list and 'current_price'
        Returns:
            True if entry signal triggered
        """
        prices = data.get('prices', [])
        current_price = data.get('current_price', 0.0)
        
        if len(prices) < self.period:
            return False
        
        conditions_met = True
        
        # Check if EMA is rising (if required)
        if self.require_rising:
            conditions_met &= ema_is_rising(prices, self.period)
        
        # Check if price crosses above EMA (if required)
        if self.require_price_above:
            conditions_met &= price_crosses_above_ema(current_price, prices, self.period)
        
        return conditions_met
    
    def get_module_name(self) -> str:
        return self.name


class GoldenCrossEntry(IEntryModule):
    """
    Golden Cross entry - when fast EMA crosses above slow EMA
    Replaces the need for separate crossover classes
    """
    
    def __init__(self, fast_period: int = 50, slow_period: int = 100):
        """
        Initialize Golden Cross entry
        Args:
            fast_period: Fast EMA period (default 50)
            slow_period: Slow EMA period (default 100)
        """
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.name = f"GoldenCross{fast_period}x{slow_period}Entry"
    
    def should_enter(self, data: Dict[str, Any]) -> bool:
        """
        Check if Golden Cross occurred
        Args:
            data: Dictionary containing 'prices' list
        Returns:
            True if golden cross entry signal triggered
        """
        prices = data.get('prices', [])
        
        if len(prices) < max(self.fast_period, self.slow_period):
            return False
        
        from modules.indicators.ema_core import ema_crosses_above_ema
        return ema_crosses_above_ema(prices, self.fast_period, self.slow_period)
    
    def get_module_name(self) -> str:
        return self.name


# Convenient wrapper functions for common scenarios
def create_ema50_entry() -> EMAEntry:
    """Create EMA50 entry module (matches old EMA50Entry.cs)"""
    return EMAEntry(period=50, require_rising=True, require_price_above=True)


def create_ema100_entry() -> EMAEntry:
    """Create EMA100 entry module (matches old EMA100Entry.cs pattern)"""
    return EMAEntry(period=100, require_rising=True, require_price_above=True)


def create_ema200_entry() -> EMAEntry:
    """Create EMA200 entry module"""
    return EMAEntry(period=200, require_rising=True, require_price_above=True)


def create_golden_cross_entry() -> GoldenCrossEntry:
    """Create standard 50x100 Golden Cross entry"""
    return GoldenCrossEntry(fast_period=50, slow_period=100)
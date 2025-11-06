"""
EMA-based exit modules
Converts C# EMA100Exit patterns to flexible Python
"""
from framework.interfaces import IExitModule
from modules.indicators import ema_is_falling, price_crosses_below_ema
from typing import Dict, Any


class EMAExit(IExitModule):
    """
    Flexible EMA exit module - replaces separate EMA100Exit, EMA200Exit classes
    Can handle any EMA period and multiple exit conditions
    """
    
    def __init__(self, period: int = 100, require_falling: bool = True, require_price_below: bool = True):
        """
        Initialize EMA exit module
        Args:
            period: EMA period (50, 100, 200, etc.)
            require_falling: Require EMA to be falling
            require_price_below: Require price to cross below EMA
        """
        self.period = period
        self.require_falling = require_falling
        self.require_price_below = require_price_below
        self.name = f"EMA{period}Exit"
    
    def should_exit(self, data: Dict[str, Any]) -> bool:
        """
        Check if EMA exit conditions are met
        Args:
            data: Dictionary containing 'prices' list, 'current_price', and position info
        Returns:
            True if exit signal triggered
        """
        prices = data.get('prices', [])
        current_price = data.get('current_price', 0.0)
        
        if len(prices) < self.period:
            return False
        
        conditions_met = True
        
        # Check if EMA is falling (if required)
        if self.require_falling:
            conditions_met &= ema_is_falling(prices, self.period)
        
        # Check if price crosses below EMA (if required)
        if self.require_price_below:
            conditions_met &= price_crosses_below_ema(current_price, prices, self.period)
        
        return conditions_met
    
    def get_module_name(self) -> str:
        return self.name


class DeathCrossExit(IExitModule):
    """
    Death Cross exit - when fast EMA crosses below slow EMA
    Replaces the need for separate crossover exit classes
    """
    
    def __init__(self, fast_period: int = 50, slow_period: int = 100):
        """
        Initialize Death Cross exit
        Args:
            fast_period: Fast EMA period (default 50)
            slow_period: Slow EMA period (default 100)
        """
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.name = f"DeathCross{fast_period}x{slow_period}Exit"
    
    def should_exit(self, data: Dict[str, Any]) -> bool:
        """
        Check if Death Cross occurred
        Args:
            data: Dictionary containing 'prices' list
        Returns:
            True if death cross exit signal triggered
        """
        prices = data.get('prices', [])
        
        if len(prices) < max(self.fast_period, self.slow_period):
            return False
        
        from modules.indicators.ema_core import ema_crosses_below_ema
        return ema_crosses_below_ema(prices, self.fast_period, self.slow_period)
    
    def get_module_name(self) -> str:
        return self.name


class StopLossExit(IExitModule):
    """
    Simple stop loss exit module
    """
    
    def __init__(self, stop_loss_percent: float = 0.05):
        """
        Initialize stop loss exit
        Args:
            stop_loss_percent: Stop loss as decimal (0.05 = 5%)
        """
        self.stop_loss_percent = stop_loss_percent
        self.name = f"StopLoss{int(stop_loss_percent * 100)}%"
    
    def should_exit(self, data: Dict[str, Any]) -> bool:
        """
        Check if stop loss triggered
        Args:
            data: Dictionary containing 'current_price' and 'entry_price'
        Returns:
            True if stop loss hit
        """
        current_price = data.get('current_price', 0.0)
        entry_price = data.get('entry_price', 0.0)
        
        if entry_price <= 0:
            return False
        
        loss_percent = (entry_price - current_price) / entry_price
        return loss_percent >= self.stop_loss_percent
    
    def get_module_name(self) -> str:
        return self.name


# Convenient wrapper functions for common scenarios
def create_ema100_exit() -> EMAExit:
    """Create EMA100 exit module (matches old EMA100Exit.cs)"""
    return EMAExit(period=100, require_falling=True, require_price_below=True)


def create_ema200_exit() -> EMAExit:
    """Create EMA200 exit module"""
    return EMAExit(period=200, require_falling=True, require_price_below=True)


def create_death_cross_exit() -> DeathCrossExit:
    """Create standard 50x100 Death Cross exit"""
    return DeathCrossExit(fast_period=50, slow_period=100)


def create_5_percent_stop_loss() -> StopLossExit:
    """Create 5% stop loss exit"""
    return StopLossExit(stop_loss_percent=0.05)
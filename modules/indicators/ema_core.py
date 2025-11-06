"""
Core EMA indicator functions
Parametrized functions for maximum flexibility
"""
from typing import List, Tuple


def calculate_ema(prices: List[float], period: int) -> float:
    """
    Calculate EMA for given period using standard formula
    Args:
        prices: List of historical prices
        period: EMA period (e.g., 50, 100, 200)
    Returns:
        Current EMA value
    """
    if len(prices) < period:
        # Use SMA for initial values if not enough data
        return sum(prices) / len(prices)
    
    # Start with SMA of first 'period' values
    sma = sum(prices[:period]) / period
    ema = sma
    
    # Calculate EMA for remaining values
    multiplier = 2.0 / (period + 1)
    for price in prices[period:]:
        ema = (price * multiplier) + (ema * (1 - multiplier))
    
    return ema


def get_ema_values(prices: List[float], period: int) -> Tuple[float, float]:
    """
    Get current and previous EMA values
    Args:
        prices: List of historical prices
        period: EMA period
    Returns:
        Tuple of (current_ema, previous_ema)
    """
    if len(prices) < 2:
        current = calculate_ema(prices, period)
        return current, current
    
    current = calculate_ema(prices, period)
    previous = calculate_ema(prices[:-1], period)
    return current, previous


def ema_is_rising(prices: List[float], period: int) -> bool:
    """
    Check if EMA of any period is rising
    Args:
        prices: List of historical prices
        period: EMA period
    Returns:
        True if EMA is rising, False otherwise
    """
    current, previous = get_ema_values(prices, period)
    return current > previous


def ema_is_falling(prices: List[float], period: int) -> bool:
    """
    Check if EMA of any period is falling
    Args:
        prices: List of historical prices
        period: EMA period
    Returns:
        True if EMA is falling, False otherwise
    """
    current, previous = get_ema_values(prices, period)
    return current < previous


def price_crosses_above_ema(price: float, prices: List[float], period: int) -> bool:
    """
    Check if price crosses above EMA of any period
    Args:
        price: Current price
        prices: Historical prices
        period: EMA period
    Returns:
        True if crossover occurred, False otherwise
    """
    if len(prices) < 2:
        return False
    
    ema_current = calculate_ema(prices, period)
    ema_previous = calculate_ema(prices[:-1], period)
    
    return price > ema_current and prices[-1] <= ema_previous


def price_crosses_below_ema(price: float, prices: List[float], period: int) -> bool:
    """
    Check if price crosses below EMA of any period
    Args:
        price: Current price
        prices: Historical prices
        period: EMA period
    Returns:
        True if crossover occurred, False otherwise
    """
    if len(prices) < 2:
        return False
    
    ema_current = calculate_ema(prices, period)
    ema_previous = calculate_ema(prices[:-1], period)
    
    return price < ema_current and prices[-1] >= ema_previous


def ema_crosses_above_ema(prices: List[float], fast_period: int, slow_period: int) -> bool:
    """
    Check if fast EMA crosses above slow EMA
    Args:
        prices: Historical prices
        fast_period: Fast EMA period (e.g., 50)
        slow_period: Slow EMA period (e.g., 100)
    Returns:
        True if golden cross occurred, False otherwise
    """
    if len(prices) < 2:
        return False
    
    fast_current = calculate_ema(prices, fast_period)
    slow_current = calculate_ema(prices, slow_period)
    fast_previous = calculate_ema(prices[:-1], fast_period)
    slow_previous = calculate_ema(prices[:-1], slow_period)
    
    return (fast_current > slow_current and fast_previous <= slow_previous)


def ema_crosses_below_ema(prices: List[float], fast_period: int, slow_period: int) -> bool:
    """
    Check if fast EMA crosses below slow EMA
    Args:
        prices: Historical prices
        fast_period: Fast EMA period (e.g., 50)
        slow_period: Slow EMA period (e.g., 100)
    Returns:
        True if death cross occurred, False otherwise
    """
    if len(prices) < 2:
        return False
    
    fast_current = calculate_ema(prices, fast_period)
    slow_current = calculate_ema(prices, slow_period)
    fast_previous = calculate_ema(prices[:-1], fast_period)
    slow_previous = calculate_ema(prices[:-1], slow_period)
    
    return (fast_current < slow_current and fast_previous >= slow_previous)
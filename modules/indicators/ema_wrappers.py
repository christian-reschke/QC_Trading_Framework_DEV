"""
Readable wrapper functions for common EMA scenarios
Built on parametrized core functions for consistency
"""
from .ema_core import (
    calculate_ema, ema_is_rising, ema_is_falling,
    price_crosses_above_ema, price_crosses_below_ema,
    ema_crosses_above_ema, ema_crosses_below_ema
)
from typing import List


def ema50_rising(prices: List[float]) -> bool:
    """Check if 50-period EMA is rising"""
    return ema_is_rising(prices, 50)


def ema100_rising(prices: List[float]) -> bool:
    """Check if 100-period EMA is rising"""
    return ema_is_rising(prices, 100)


def ema200_rising(prices: List[float]) -> bool:
    """Check if 200-period EMA is rising"""
    return ema_is_rising(prices, 200)


def ema50_falling(prices: List[float]) -> bool:
    """Check if 50-period EMA is falling"""
    return ema_is_falling(prices, 50)


def ema100_falling(prices: List[float]) -> bool:
    """Check if 100-period EMA is falling"""
    return ema_is_falling(prices, 100)


def ema200_falling(prices: List[float]) -> bool:
    """Check if 200-period EMA is falling"""
    return ema_is_falling(prices, 200)


def price_above_ema50(price: float, prices: List[float]) -> bool:
    """Check if price crosses above 50-period EMA"""
    return price_crosses_above_ema(price, prices, 50)


def price_above_ema100(price: float, prices: List[float]) -> bool:
    """Check if price crosses above 100-period EMA"""
    return price_crosses_above_ema(price, prices, 100)


def price_above_ema200(price: float, prices: List[float]) -> bool:
    """Check if price crosses above 200-period EMA"""
    return price_crosses_above_ema(price, prices, 200)


def price_below_ema50(price: float, prices: List[float]) -> bool:
    """Check if price crosses below 50-period EMA"""
    return price_crosses_below_ema(price, prices, 50)


def price_below_ema100(price: float, prices: List[float]) -> bool:
    """Check if price crosses below 100-period EMA"""
    return price_crosses_below_ema(price, prices, 100)


def price_below_ema200(price: float, prices: List[float]) -> bool:
    """Check if price crosses below 200-period EMA"""
    return price_crosses_below_ema(price, prices, 200)


def golden_cross(prices: List[float]) -> bool:
    """Check if 50-period EMA crosses above 100-period EMA (Golden Cross)"""
    return ema_crosses_above_ema(prices, 50, 100)


def death_cross(prices: List[float]) -> bool:
    """Check if 50-period EMA crosses below 100-period EMA (Death Cross)"""
    return ema_crosses_below_ema(prices, 50, 100)


def long_term_golden_cross(prices: List[float]) -> bool:
    """Check if 100-period EMA crosses above 200-period EMA"""
    return ema_crosses_above_ema(prices, 100, 200)


def long_term_death_cross(prices: List[float]) -> bool:
    """Check if 100-period EMA crosses below 200-period EMA"""
    return ema_crosses_below_ema(prices, 100, 200)
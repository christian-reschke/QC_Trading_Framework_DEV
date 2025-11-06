"""
Bollinger Bands indicator functions
Core calculations for Bollinger Bands Width (BBW) and band levels
"""
from typing import List, Tuple
import math


def calculate_sma(prices: List[float], period: int) -> float:
    """
    Calculate Simple Moving Average
    Args:
        prices: List of historical prices
        period: SMA period
    Returns:
        Simple moving average value
    """
    if len(prices) < period:
        return sum(prices) / len(prices) if prices else 0.0
    
    return sum(prices[-period:]) / period


def calculate_standard_deviation(prices: List[float], period: int, sma: float = None) -> float:
    """
    Calculate standard deviation for given period
    Args:
        prices: List of historical prices
        period: Period for calculation
        sma: Pre-calculated SMA (optional)
    Returns:
        Standard deviation value
    """
    if len(prices) < period:
        period = len(prices)
    
    if period <= 1:
        return 0.0
    
    recent_prices = prices[-period:]
    if sma is None:
        sma = sum(recent_prices) / len(recent_prices)
    
    variance = sum((price - sma) ** 2 for price in recent_prices) / period
    return math.sqrt(variance)


def calculate_bollinger_bands(prices: List[float], period: int = 20, std_multiplier: float = 2.0) -> Tuple[float, float, float]:
    """
    Calculate Bollinger Bands: Upper, Middle (SMA), Lower
    Args:
        prices: List of historical prices
        period: Moving average period (default 20)
        std_multiplier: Standard deviation multiplier (default 2.0)
    Returns:
        Tuple of (upper_band, middle_band, lower_band)
    """
    if len(prices) < period:
        # Not enough data, return current price as all bands
        current_price = prices[-1] if prices else 0.0
        return current_price, current_price, current_price
    
    # Calculate middle band (SMA)
    middle_band = calculate_sma(prices, period)
    
    # Calculate standard deviation
    std_dev = calculate_standard_deviation(prices, period, middle_band)
    
    # Calculate upper and lower bands
    band_width = std_dev * std_multiplier
    upper_band = middle_band + band_width
    lower_band = middle_band - band_width
    
    return upper_band, middle_band, lower_band


def calculate_bollinger_band_width(prices: List[float], period: int = 20, std_multiplier: float = 2.0) -> float:
    """
    Calculate Bollinger Band Width (BBW)
    BBW = (Upper Band - Lower Band) / Middle Band
    Args:
        prices: List of historical prices
        period: Moving average period (default 20)
        std_multiplier: Standard deviation multiplier (default 2.0)
    Returns:
        Bollinger Band Width as percentage
    """
    upper_band, middle_band, lower_band = calculate_bollinger_bands(prices, period, std_multiplier)
    
    if middle_band == 0:
        return 0.0
    
    bbw = (upper_band - lower_band) / middle_band
    return bbw


def get_recent_high(prices: List[float], lookback: int = 5) -> float:
    """
    Get the highest price in the recent lookback period
    Args:
        prices: List of historical prices
        lookback: Number of periods to look back
    Returns:
        Highest price in lookback period
    """
    if not prices:
        return 0.0
    
    if len(prices) <= lookback:
        return max(prices)
    
    return max(prices[-lookback:])


def is_break_above_recent_high(current_price: float, prices: List[float], lookback: int = 5) -> bool:
    """
    Check if current price breaks above recent high
    Args:
        current_price: Current price
        prices: Historical prices (excluding current)
        lookback: Number of periods to look back
    Returns:
        True if current price is above recent high
    """
    if not prices:
        return False
    
    recent_high = get_recent_high(prices, lookback)
    return current_price > recent_high


def is_bollinger_ready(prices: List[float], period: int = 20) -> bool:
    """
    Check if we have enough data for reliable Bollinger Bands
    Args:
        prices: List of historical prices
        period: Bollinger Bands period
    Returns:
        True if enough data for reliable calculation
    """
    return len(prices) >= period


# Wrapper functions for common scenarios
def bb_bands_20_period(prices: List[float]) -> Tuple[float, float, float]:
    """Standard 20-period Bollinger Bands"""
    return calculate_bollinger_bands(prices, 20, 2.0)


def bb_width_20_period(prices: List[float]) -> float:
    """Standard 20-period Bollinger Band Width"""
    return calculate_bollinger_band_width(prices, 20, 2.0)


def is_low_volatility(prices: List[float], bbw_threshold: float = 0.1) -> bool:
    """
    Check if current volatility (BBW) is below threshold
    Args:
        prices: Historical prices
        bbw_threshold: Threshold for low volatility (default 0.1 = 10%)
    Returns:
        True if volatility is low
    """
    if not is_bollinger_ready(prices):
        return False
    
    bbw = bb_width_20_period(prices)
    return bbw < bbw_threshold


def price_breaks_above_bb_upper(current_price: float, prices: List[float]) -> bool:
    """
    Check if price breaks above upper Bollinger Band
    Args:
        current_price: Current price
        prices: Historical prices
    Returns:
        True if price breaks above upper band
    """
    if not is_bollinger_ready(prices):
        return False
    
    upper_band, _, _ = bb_bands_20_period(prices)
    return current_price > upper_band
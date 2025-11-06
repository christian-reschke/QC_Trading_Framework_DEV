"""
Vola Breakout entry module
Implements the volatility breakout strategy entry conditions
"""
from framework.interfaces import IEntryModule
from modules.indicators import (
    ema_is_rising, calculate_ema, 
    is_bollinger_ready, bb_width_20_period, bb_bands_20_period,
    is_break_above_recent_high
)
from typing import Dict, Any, List


class VolaBreakoutEntry(IEntryModule):
    """
    Volatility Breakout Entry Strategy
    
    Entry conditions:
    1. inTrend = price > ema and ema > ema[1]  (trend filter)
    2. isLowBBW = isReady and bbw < bbwThreshold  (low volatility)
    3. breakAboveBB = close > bbUpper  (breakout signal)
    4. breakAboveRecentHigh = close > ta.highest(high, 5)[1]  (momentum confirmation)
    """
    
    def __init__(self, ema_period: int = 50, bbw_threshold: float = 0.1, 
                 bb_period: int = 20, recent_high_lookback: int = 5):
        """
        Initialize Vola Breakout entry module
        Args:
            ema_period: EMA period for trend filter (default 50)
            bbw_threshold: BBW threshold for low volatility (default 0.1 = 10%)
            bb_period: Bollinger Bands period (default 20)
            recent_high_lookback: Lookback period for recent high (default 5)
        """
        self.ema_period = ema_period
        self.bbw_threshold = bbw_threshold
        self.bb_period = bb_period
        self.recent_high_lookback = recent_high_lookback
        self.name = f"VolaBreakout_EMA{ema_period}_BBW{int(bbw_threshold*100)}"
    
    def should_enter(self, data: Dict[str, Any]) -> bool:
        """
        Check if all Vola Breakout entry conditions are met
        Args:
            data: Dictionary containing:
                - prices: List[float] (historical prices including current)
                - current_price: float
                - highs: List[float] (optional, historical high prices)
        Returns:
            True if all entry conditions are met
        """
        prices = data.get('prices', [])
        current_price = data.get('current_price', 0.0)
        highs = data.get('highs', prices)  # Use prices as highs if not provided
        
        if len(prices) < max(self.ema_period, self.bb_period):
            return False
        
        # Condition 1: inTrend = price > ema and ema > ema[1]
        in_trend = self._check_trend_condition(prices, current_price)
        
        # Condition 2: isLowBBW = isReady and bbw < bbwThreshold
        is_low_bbw = self._check_low_volatility_condition(prices)
        
        # Condition 3: breakAboveBB = close > bbUpper
        break_above_bb = self._check_bb_breakout_condition(prices, current_price)
        
        # Condition 4: breakAboveRecentHigh = close > ta.highest(high, 5)[1]
        break_above_recent_high = self._check_recent_high_condition(highs, current_price)
        
        # All conditions must be true
        all_conditions_met = (in_trend and is_low_bbw and 
                            break_above_bb and break_above_recent_high)
        
        return all_conditions_met
    
    def get_module_name(self) -> str:
        return self.name
    
    def _check_trend_condition(self, prices: List[float], current_price: float) -> bool:
        """
        Check trend condition: price > ema and ema > ema[1]
        """
        if len(prices) < self.ema_period + 1:
            return False
        
        # Current EMA
        current_ema = calculate_ema(prices, self.ema_period)
        
        # Previous EMA (using prices excluding the current one)
        previous_ema = calculate_ema(prices[:-1], self.ema_period)
        
        # Check both conditions
        price_above_ema = current_price > current_ema
        ema_rising = current_ema > previous_ema
        
        return price_above_ema and ema_rising
    
    def _check_low_volatility_condition(self, prices: List[float]) -> bool:
        """
        Check low volatility condition: isReady and bbw < bbwThreshold
        """
        # Check if we have enough data
        if not is_bollinger_ready(prices, self.bb_period):
            return False
        
        # Calculate current BBW
        bbw = bb_width_20_period(prices)
        
        return bbw < self.bbw_threshold
    
    def _check_bb_breakout_condition(self, prices: List[float], current_price: float) -> bool:
        """
        Check Bollinger Band breakout condition: close > bbUpper
        """
        if not is_bollinger_ready(prices, self.bb_period):
            return False
        
        upper_band, _, _ = bb_bands_20_period(prices)
        
        return current_price > upper_band
    
    def _check_recent_high_condition(self, highs: List[float], current_price: float) -> bool:
        """
        Check recent high breakout condition: close > highest(high, 5)[1]
        """
        if len(highs) < self.recent_high_lookback + 1:
            return False
        
        # Get recent highs excluding current price
        recent_highs = highs[:-1]  # Exclude current
        
        if len(recent_highs) < self.recent_high_lookback:
            recent_high = max(recent_highs) if recent_highs else 0
        else:
            recent_high = max(recent_highs[-self.recent_high_lookback:])
        
        return current_price > recent_high
    
    def get_entry_details(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get detailed breakdown of entry conditions for debugging
        Args:
            data: Market data dictionary
        Returns:
            Dictionary with condition details
        """
        prices = data.get('prices', [])
        current_price = data.get('current_price', 0.0)
        highs = data.get('highs', prices)
        
        details = {
            'trend_condition': self._check_trend_condition(prices, current_price),
            'low_volatility_condition': self._check_low_volatility_condition(prices),
            'bb_breakout_condition': self._check_bb_breakout_condition(prices, current_price),
            'recent_high_condition': self._check_recent_high_condition(highs, current_price),
            'overall_signal': self.should_enter(data)
        }
        
        # Add current values for reference
        if len(prices) >= self.ema_period:
            details['current_ema'] = calculate_ema(prices, self.ema_period)
        if is_bollinger_ready(prices, self.bb_period):
            details['current_bbw'] = bb_width_20_period(prices)
            upper, middle, lower = bb_bands_20_period(prices)
            details['bb_upper'] = upper
            details['bb_middle'] = middle
            details['bb_lower'] = lower
        
        return details


# Convenient wrapper functions
def create_vola_breakout_entry(ema_period: int = 50, bbw_threshold: float = 0.1) -> VolaBreakoutEntry:
    """
    Create standard Vola Breakout entry module
    Args:
        ema_period: EMA period for trend filter
        bbw_threshold: BBW threshold for low volatility detection
    Returns:
        Configured VolaBreakoutEntry instance
    """
    return VolaBreakoutEntry(ema_period=ema_period, bbw_threshold=bbw_threshold)


def create_aggressive_vola_breakout() -> VolaBreakoutEntry:
    """Create more aggressive Vola Breakout with lower BBW threshold"""
    return VolaBreakoutEntry(ema_period=20, bbw_threshold=0.08)


def create_conservative_vola_breakout() -> VolaBreakoutEntry:
    """Create more conservative Vola Breakout with higher BBW threshold"""
    return VolaBreakoutEntry(ema_period=100, bbw_threshold=0.12)
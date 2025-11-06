"""
EMA50-based entry module
Entry signal when price crosses above 50-period EMA and EMA is rising
"""
from framework.interfaces import IEntryModule
from modules.indicators import price_above_ema50, ema50_rising
from typing import Dict, Any


class EMA50Entry(IEntryModule):
    """Entry signal based on EMA50 crossover and direction"""
    
    def __init__(self):
        self.module_name = "EMA50Entry"
    
    def should_enter(self, data: Dict[str, Any]) -> bool:
        """
        Entry when price crosses above EMA50 and EMA50 is rising
        Args:
            data: Must contain 'price' (current price) and 'prices' (historical prices list)
        Returns:
            True if entry condition is met
        """
        if 'price' not in data or 'prices' not in data:
            return False
        
        price = data['price']
        prices = data['prices']
        
        # Entry conditions:
        # 1. Price crosses above EMA50
        # 2. EMA50 is rising (uptrend confirmation)
        return (price_above_ema50(price, prices) and 
                ema50_rising(prices))
    
    def get_module_name(self) -> str:
        """Return module name for identification"""
        return self.module_name
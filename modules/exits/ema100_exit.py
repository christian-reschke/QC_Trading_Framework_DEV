"""
EMA100-based exit module
Exit signal when price crosses below 100-period EMA
"""
from framework.interfaces import IExitModule
from modules.indicators import price_below_ema100
from typing import Dict, Any


class EMA100Exit(IExitModule):
    """Exit signal based on EMA100 crossover"""
    
    def __init__(self):
        self.module_name = "EMA100Exit"
    
    def should_exit(self, data: Dict[str, Any]) -> bool:
        """
        Exit when price crosses below EMA100
        Args:
            data: Must contain 'price' (current price) and 'prices' (historical prices list)
        Returns:
            True if exit condition is met
        """
        if 'price' not in data or 'prices' not in data:
            return False
        
        price = data['price']
        prices = data['prices']
        
        return price_below_ema100(price, prices)
    
    def get_module_name(self) -> str:
        """Return module name for identification"""
        return self.module_name
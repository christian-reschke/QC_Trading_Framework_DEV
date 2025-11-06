"""
Golden Cross entry module
Entry signal when 50-period EMA crosses above 100-period EMA
"""
from framework.interfaces import IEntryModule
from modules.indicators import golden_cross
from typing import Dict, Any


class GoldenCrossEntry(IEntryModule):
    """Entry signal based on Golden Cross (EMA50 > EMA100)"""
    
    def __init__(self):
        self.module_name = "GoldenCrossEntry"
    
    def should_enter(self, data: Dict[str, Any]) -> bool:
        """
        Entry when 50-period EMA crosses above 100-period EMA
        Args:
            data: Must contain 'prices' (historical prices list)
        Returns:
            True if Golden Cross occurred
        """
        if 'prices' not in data:
            return False
        
        prices = data['prices']
        return golden_cross(prices)
    
    def get_module_name(self) -> str:
        """Return module name for identification"""
        return self.module_name
"""
Death Cross exit module
Exit signal when 50-period EMA crosses below 100-period EMA
"""
from framework.interfaces import IExitModule
from modules.indicators import death_cross
from typing import Dict, Any


class DeathCrossExit(IExitModule):
    """Exit signal based on Death Cross (EMA50 < EMA100)"""
    
    def __init__(self):
        self.module_name = "DeathCrossExit"
    
    def should_exit(self, data: Dict[str, Any]) -> bool:
        """
        Exit when 50-period EMA crosses below 100-period EMA
        Args:
            data: Must contain 'prices' (historical prices list)
        Returns:
            True if Death Cross occurred
        """
        if 'prices' not in data:
            return False
        
        prices = data['prices']
        return death_cross(prices)
    
    def get_module_name(self) -> str:
        """Return module name for identification"""
        return self.module_name
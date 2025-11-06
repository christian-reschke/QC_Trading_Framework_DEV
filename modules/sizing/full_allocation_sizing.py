"""
Full allocation position sizing module
Allocates 100% of available capital to position
"""
from framework.interfaces import IPositionSizingModule
from typing import Dict, Any


class FullAllocationSizing(IPositionSizingModule):
    """Position sizing that uses 100% of available capital"""
    
    def __init__(self):
        self.module_name = "FullAllocationSizing"
    
    def calculate_size(self, data: Dict[str, Any]) -> float:
        """
        Calculate position size as 100% allocation
        Args:
            data: Dictionary containing account info (not used for full allocation)
        Returns:
            Position size as 1.0 (100% of portfolio)
        """
        return 1.0
    
    def get_module_name(self) -> str:
        """Return module name for identification"""
        return self.module_name
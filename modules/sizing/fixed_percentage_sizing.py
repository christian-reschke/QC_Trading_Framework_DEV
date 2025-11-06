"""
Fixed percentage position sizing module
Allocates fixed percentage of available capital
"""
from framework.interfaces import IPositionSizingModule
from typing import Dict, Any


class FixedPercentageSizing(IPositionSizingModule):
    """Position sizing that uses fixed percentage of capital"""
    
    def __init__(self, percentage: float = 0.5):
        """
        Initialize with fixed percentage
        Args:
            percentage: Percentage of capital to allocate (0.0 to 1.0)
        """
        self.percentage = max(0.0, min(1.0, percentage))  # Clamp between 0 and 1
        self.module_name = f"FixedPercentageSizing_{int(self.percentage * 100)}%"
    
    def calculate_size(self, data: Dict[str, Any]) -> float:
        """
        Calculate position size as fixed percentage
        Args:
            data: Dictionary containing account info (not used for fixed allocation)
        Returns:
            Position size as fixed percentage of portfolio
        """
        return self.percentage
    
    def get_module_name(self) -> str:
        """Return module name for identification"""
        return self.module_name
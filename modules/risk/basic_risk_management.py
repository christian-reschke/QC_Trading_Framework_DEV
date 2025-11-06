"""
Basic risk management module
Implements simple stop-loss and position size limits
"""
from framework.interfaces import IRiskModule
from typing import Dict, Any


class BasicRiskManagement(IRiskModule):
    """Basic risk management with configurable stop-loss"""
    
    def __init__(self, stop_loss_percent: float = 0.02, max_position_size: float = 1.0):
        """
        Initialize risk management parameters
        Args:
            stop_loss_percent: Stop loss as percentage below entry (0.02 = 2%)
            max_position_size: Maximum position size as percentage of portfolio
        """
        self.stop_loss_percent = stop_loss_percent
        self.max_position_size = max_position_size
        self.module_name = f"BasicRisk_SL{int(stop_loss_percent * 100)}%"
    
    def check_risk(self, data: Dict[str, Any]) -> bool:
        """
        Check if trade meets risk criteria
        Args:
            data: Dictionary containing position_size, account_balance, etc.
        Returns:
            True if risk is acceptable
        """
        # Check position size limit
        position_size = data.get('position_size', 0.0)
        if position_size > self.max_position_size:
            return False
        
        # Add additional risk checks here as needed
        # (e.g., correlation limits, sector exposure, etc.)
        
        return True
    
    def get_stop_loss(self, data: Dict[str, Any]) -> float:
        """
        Calculate stop loss level
        Args:
            data: Dictionary containing 'entry_price'
        Returns:
            Stop loss price level
        """
        entry_price = data.get('entry_price', 0.0)
        if entry_price <= 0:
            return 0.0
        
        return entry_price * (1.0 - self.stop_loss_percent)
    
    def get_module_name(self) -> str:
        """Return module name for identification"""
        return self.module_name
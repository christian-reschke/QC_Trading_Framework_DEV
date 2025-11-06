"""
Trailing stop exit module
Implements dynamic trailing stop loss functionality
"""
from framework.interfaces import IExitModule
from typing import Dict, Any


class TrailingStopExit(IExitModule):
    """
    Trailing Stop Loss Exit Strategy
    
    Maintains a stop loss that follows the price upward but never moves down.
    Exit when price falls below the trailing stop level.
    """
    
    def __init__(self, trail_percent: float = 0.05, initial_stop_percent: float = 0.03):
        """
        Initialize trailing stop exit module
        Args:
            trail_percent: Trailing percentage (0.05 = 5%)
            initial_stop_percent: Initial stop loss percentage (0.03 = 3%)
        """
        self.trail_percent = trail_percent
        self.initial_stop_percent = initial_stop_percent
        self.name = f"TrailingStop{int(trail_percent*100)}%"
        
        # Track the highest price since entry and current stop level
        self._highest_price = 0.0
        self._current_stop_level = 0.0
        self._position_active = False
    
    def should_exit(self, data: Dict[str, Any]) -> bool:
        """
        Check if trailing stop exit condition is met
        Args:
            data: Dictionary containing:
                - current_price: float
                - entry_price: float
                - current_position: float (position size, 0 = no position)
        Returns:
            True if should exit position
        """
        current_price = data.get('current_price', 0.0)
        entry_price = data.get('entry_price', 0.0)
        current_position = data.get('current_position', 0.0)
        
        # No position, no exit
        if current_position == 0:
            self._reset_tracking()
            return False
        
        # Initialize tracking if new position
        if not self._position_active:
            self._initialize_position(entry_price)
        
        # Update trailing stop
        self._update_trailing_stop(current_price)
        
        # Check if price has fallen below trailing stop
        should_exit = current_price <= self._current_stop_level
        
        if should_exit:
            self._reset_tracking()
        
        return should_exit
    
    def get_module_name(self) -> str:
        return self.name
    
    def get_current_stop_level(self) -> float:
        """Get the current trailing stop level"""
        return self._current_stop_level
    
    def get_highest_price(self) -> float:
        """Get the highest price seen since position entry"""
        return self._highest_price
    
    def _initialize_position(self, entry_price: float):
        """
        Initialize tracking for a new position
        Args:
            entry_price: Price at which position was entered
        """
        self._highest_price = entry_price
        self._current_stop_level = entry_price * (1 - self.initial_stop_percent)
        self._position_active = True
    
    def _update_trailing_stop(self, current_price: float):
        """
        Update the trailing stop based on current price
        Args:
            current_price: Current market price
        """
        # Update highest price if current price is higher
        if current_price > self._highest_price:
            self._highest_price = current_price
            
            # Calculate new trailing stop level
            new_stop_level = self._highest_price * (1 - self.trail_percent)
            
            # Only move stop level up, never down
            if new_stop_level > self._current_stop_level:
                self._current_stop_level = new_stop_level
    
    def _reset_tracking(self):
        """Reset tracking variables when position is closed"""
        self._highest_price = 0.0
        self._current_stop_level = 0.0
        self._position_active = False
    
    def get_exit_details(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get detailed information about the trailing stop state
        Args:
            data: Market data dictionary
        Returns:
            Dictionary with trailing stop details
        """
        current_price = data.get('current_price', 0.0)
        entry_price = data.get('entry_price', 0.0)
        
        return {
            'current_price': current_price,
            'entry_price': entry_price,
            'highest_price': self._highest_price,
            'current_stop_level': self._current_stop_level,
            'distance_from_stop': current_price - self._current_stop_level if self._current_stop_level > 0 else 0,
            'distance_from_stop_percent': ((current_price - self._current_stop_level) / current_price) if current_price > 0 and self._current_stop_level > 0 else 0,
            'unrealized_gain': current_price - entry_price if entry_price > 0 else 0,
            'unrealized_gain_percent': ((current_price - entry_price) / entry_price) if entry_price > 0 else 0,
            'position_active': self._position_active,
            'should_exit': self.should_exit(data)
        }


class PercentageStopExit(IExitModule):
    """
    Simple percentage-based stop loss exit
    Exit when price falls a certain percentage below entry
    """
    
    def __init__(self, stop_percent: float = 0.05):
        """
        Initialize percentage stop exit
        Args:
            stop_percent: Stop loss percentage (0.05 = 5%)
        """
        self.stop_percent = stop_percent
        self.name = f"Stop{int(stop_percent*100)}%"
    
    def should_exit(self, data: Dict[str, Any]) -> bool:
        """
        Check if percentage stop loss is hit
        Args:
            data: Dictionary containing current_price, entry_price, current_position
        Returns:
            True if should exit
        """
        current_price = data.get('current_price', 0.0)
        entry_price = data.get('entry_price', 0.0)
        current_position = data.get('current_position', 0.0)
        
        # No position, no exit
        if current_position == 0 or entry_price <= 0:
            return False
        
        # Calculate loss percentage
        loss_percent = (entry_price - current_price) / entry_price
        
        return loss_percent >= self.stop_percent
    
    def get_module_name(self) -> str:
        return self.name


# Convenient wrapper functions
def create_trailing_stop(trail_percent: float = 0.05) -> TrailingStopExit:
    """
    Create trailing stop exit with specified trail percentage
    Args:
        trail_percent: Trailing percentage (default 5%)
    Returns:
        Configured TrailingStopExit instance
    """
    return TrailingStopExit(trail_percent=trail_percent)


def create_tight_trailing_stop() -> TrailingStopExit:
    """Create tight trailing stop (3% trail, 2% initial stop)"""
    return TrailingStopExit(trail_percent=0.03, initial_stop_percent=0.02)


def create_loose_trailing_stop() -> TrailingStopExit:
    """Create loose trailing stop (8% trail, 5% initial stop)"""
    return TrailingStopExit(trail_percent=0.08, initial_stop_percent=0.05)


def create_percentage_stop(stop_percent: float = 0.05) -> PercentageStopExit:
    """
    Create simple percentage stop loss
    Args:
        stop_percent: Stop loss percentage (default 5%)
    Returns:
        Configured PercentageStopExit instance
    """
    return PercentageStopExit(stop_percent=stop_percent)
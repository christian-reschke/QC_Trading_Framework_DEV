"""
Risk management modules
Converts C# BasicRiskManagement patterns to flexible Python
"""
from framework.interfaces import IRiskModule
from typing import Dict, Any


class BasicRiskManagement(IRiskModule):
    """
    Basic risk management - prevents over-leverage and validates basic trade constraints
    Converts C# BasicRiskManagement.cs to Python
    """
    
    def __init__(self, max_leverage: float = 1.0, min_cash_buffer: float = 1000.0):
        """
        Initialize basic risk management
        Args:
            max_leverage: Maximum leverage allowed (1.0 = no leverage)
            min_cash_buffer: Minimum cash buffer to maintain
        """
        self.max_leverage = max_leverage
        self.min_cash_buffer = min_cash_buffer
        self.name = "BasicRisk"
    
    def check_risk(self, data: Dict[str, Any]) -> bool:
        """
        Check if trade meets basic risk criteria
        Args:
            data: Dictionary containing trade and portfolio info
        Returns:
            True if risk is acceptable
        """
        proposed_quantity = data.get('proposed_quantity', 0.0)
        current_position = data.get('current_position', 0.0)
        portfolio_value = data.get('portfolio_value', 0.0)
        available_cash = data.get('available_cash', 0.0)
        current_price = data.get('current_price', 0.0)
        
        # Always allow exit trades
        if current_position != 0 and self._is_exit_trade(proposed_quantity, current_position):
            return True
        
        # For entry trades, check basic constraints
        trade_value = abs(proposed_quantity * current_price)
        
        # Don't allow trades that exceed portfolio value (no leverage check)
        if trade_value > portfolio_value:
            return False
        
        # Allow trades up to 99% of available cash (realistic for 100% allocation)
        if trade_value > available_cash * 0.99:
            return False
        
        return True
    
    def get_stop_loss(self, data: Dict[str, Any]) -> float:
        """
        Calculate basic stop loss level
        Args:
            data: Dictionary containing entry price and risk parameters
        Returns:
            Stop loss price level
        """
        entry_price = data.get('entry_price', 0.0)
        stop_loss_percent = data.get('stop_loss_percent', 0.05)  # Default 5%
        
        if entry_price <= 0:
            return 0.0
        
        return entry_price * (1.0 - stop_loss_percent)
    
    def get_module_name(self) -> str:
        return self.name
    
    def _is_exit_trade(self, proposed_quantity: float, current_position: float) -> bool:
        """Check if proposed trade is an exit (opposite sign from current position)"""
        if current_position == 0:
            return False
        return (proposed_quantity > 0) != (current_position > 0)


class AdvancedRiskManagement(IRiskModule):
    """
    Advanced risk management with position sizing limits and drawdown protection
    """
    
    def __init__(self, max_position_size: float = 0.20, max_sector_exposure: float = 0.50, 
                 max_drawdown: float = 0.15):
        """
        Initialize advanced risk management
        Args:
            max_position_size: Maximum position size as % of portfolio (0.20 = 20%)
            max_sector_exposure: Maximum sector exposure as % of portfolio
            max_drawdown: Maximum drawdown before risk reduction (0.15 = 15%)
        """
        self.max_position_size = max_position_size
        self.max_sector_exposure = max_sector_exposure
        self.max_drawdown = max_drawdown
        self.name = "AdvancedRisk"
    
    def check_risk(self, data: Dict[str, Any]) -> bool:
        """
        Check advanced risk criteria including position limits and drawdown
        Args:
            data: Dictionary containing detailed portfolio and market info
        Returns:
            True if risk is acceptable
        """
        # Basic checks first
        basic_risk = BasicRiskManagement()
        if not basic_risk.check_risk(data):
            return False
        
        # Additional advanced checks
        proposed_quantity = data.get('proposed_quantity', 0.0)
        current_price = data.get('current_price', 0.0)
        portfolio_value = data.get('portfolio_value', 0.0)
        current_drawdown = data.get('current_drawdown', 0.0)
        
        trade_value = abs(proposed_quantity * current_price)
        position_size_percent = trade_value / portfolio_value if portfolio_value > 0 else 0
        
        # Check position size limit
        if position_size_percent > self.max_position_size:
            return False
        
        # Check drawdown limit
        if current_drawdown > self.max_drawdown:
            return False
        
        return True
    
    def get_stop_loss(self, data: Dict[str, Any]) -> float:
        """
        Calculate dynamic stop loss based on volatility
        Args:
            data: Dictionary containing price data and volatility info
        Returns:
            Stop loss price level
        """
        entry_price = data.get('entry_price', 0.0)
        volatility = data.get('volatility', 0.02)  # Default 2% daily volatility
        
        if entry_price <= 0:
            return 0.0
        
        # Dynamic stop loss: 2x daily volatility, minimum 3%, maximum 8%
        stop_loss_percent = max(0.03, min(0.08, volatility * 2))
        
        return entry_price * (1.0 - stop_loss_percent)
    
    def get_module_name(self) -> str:
        return self.name


class VolatilityBasedRisk(IRiskModule):
    """
    Risk management based on market volatility
    Reduces position sizes during high volatility periods
    """
    
    def __init__(self, base_max_position: float = 0.95, volatility_threshold: float = 0.03):
        """
        Initialize volatility-based risk management
        Args:
            base_max_position: Base maximum position size in normal conditions
            volatility_threshold: Volatility threshold above which to reduce positions
        """
        self.base_max_position = base_max_position
        self.volatility_threshold = volatility_threshold
        self.name = "VolatilityRisk"
    
    def check_risk(self, data: Dict[str, Any]) -> bool:
        """
        Check risk with volatility adjustment
        """
        # Get volatility-adjusted maximum position size
        volatility = data.get('volatility', 0.02)
        adjusted_max_position = self._get_volatility_adjusted_max_position(volatility)
        
        # Update data with adjusted position limit
        data_copy = data.copy()
        data_copy['max_position_size'] = adjusted_max_position
        
        # Use basic risk management with adjusted limits
        return BasicRiskManagement().check_risk(data_copy)
    
    def get_stop_loss(self, data: Dict[str, Any]) -> float:
        """
        Calculate volatility-adjusted stop loss
        """
        entry_price = data.get('entry_price', 0.0)
        volatility = data.get('volatility', 0.02)
        
        if entry_price <= 0:
            return 0.0
        
        # Stop loss based on volatility: 1.5x to 3x daily volatility
        volatility_multiplier = 1.5 + (volatility / self.volatility_threshold)
        stop_loss_percent = min(0.10, volatility * volatility_multiplier)  # Cap at 10%
        
        return entry_price * (1.0 - stop_loss_percent)
    
    def get_module_name(self) -> str:
        return self.name
    
    def _get_volatility_adjusted_max_position(self, volatility: float) -> float:
        """Calculate maximum position size adjusted for current volatility"""
        if volatility <= self.volatility_threshold:
            return self.base_max_position
        
        # Reduce position size linearly with excess volatility
        volatility_ratio = volatility / self.volatility_threshold
        adjustment_factor = max(0.3, 1.0 / volatility_ratio)  # Never go below 30% of base
        
        return self.base_max_position * adjustment_factor


# Convenient wrapper functions
def create_basic_risk() -> BasicRiskManagement:
    """Create basic risk management (matches C# BasicRiskManagement.cs)"""
    return BasicRiskManagement()


def create_advanced_risk() -> AdvancedRiskManagement:
    """Create advanced risk management with position limits"""
    return AdvancedRiskManagement()


def create_volatility_risk() -> VolatilityBasedRisk:
    """Create volatility-based risk management"""
    return VolatilityBasedRisk()
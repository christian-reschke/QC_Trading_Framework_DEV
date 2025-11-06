"""
Strategy builder for creating modular trading strategies
Converts C# SimpleStrategyBuilder to Python with fluent API
"""
from framework.interfaces import IEntryModule, IExitModule, IPositionSizingModule, IRiskModule, ISimpleStrategy
from typing import Dict, Any, List, Optional
from datetime import datetime


class SimpleStrategyBuilder:
    """
    Builder class for creating modular trading strategies with fluent API
    Usage: SimpleStrategyBuilder().with_entry(entry_module).with_exit(exit_module).build()
    """
    
    def __init__(self):
        self._entry_module: Optional[IEntryModule] = None
        self._exit_module: Optional[IExitModule] = None
        self._position_sizing_module: Optional[IPositionSizingModule] = None
        self._risk_module: Optional[IRiskModule] = None
        self._strategy_name: Optional[str] = None
    
    def with_entry(self, entry_module: IEntryModule) -> 'SimpleStrategyBuilder':
        """
        Sets the entry module for the strategy
        Args:
            entry_module: Module implementing IEntryModule interface
        Returns:
            Self for fluent chaining
        """
        if entry_module is None:
            raise ValueError("Entry module cannot be None")
        self._entry_module = entry_module
        return self
    
    def with_exit(self, exit_module: IExitModule) -> 'SimpleStrategyBuilder':
        """
        Sets the exit module for the strategy
        Args:
            exit_module: Module implementing IExitModule interface
        Returns:
            Self for fluent chaining
        """
        if exit_module is None:
            raise ValueError("Exit module cannot be None")
        self._exit_module = exit_module
        return self
    
    def with_position_sizing(self, position_sizing_module: IPositionSizingModule) -> 'SimpleStrategyBuilder':
        """
        Sets the position sizing module for the strategy
        Args:
            position_sizing_module: Module implementing IPositionSizingModule interface
        Returns:
            Self for fluent chaining
        """
        if position_sizing_module is None:
            raise ValueError("Position sizing module cannot be None")
        self._position_sizing_module = position_sizing_module
        return self
    
    def with_risk_management(self, risk_module: IRiskModule) -> 'SimpleStrategyBuilder':
        """
        Sets the risk management module for the strategy
        Args:
            risk_module: Module implementing IRiskModule interface
        Returns:
            Self for fluent chaining
        """
        if risk_module is None:
            raise ValueError("Risk management module cannot be None")
        self._risk_module = risk_module
        return self
    
    def with_name(self, name: str) -> 'SimpleStrategyBuilder':
        """
        Sets the strategy name for identification
        Args:
            name: Strategy name string
        Returns:
            Self for fluent chaining
        """
        if not name:
            raise ValueError("Strategy name cannot be empty")
        self._strategy_name = name
        return self
    
    def build(self) -> ISimpleStrategy:
        """
        Builds and validates the complete strategy
        Returns:
            A configured ISimpleStrategy instance
        Raises:
            ValueError: When required modules are missing
        """
        self._validate_configuration()
        
        return SimpleStrategy(
            name=self._strategy_name or self._generate_default_name(),
            entry_module=self._entry_module,
            exit_module=self._exit_module,
            position_sizing_module=self._position_sizing_module,
            risk_module=self._risk_module
        )
    
    def _validate_configuration(self):
        """Validate that all required modules are set"""
        if self._entry_module is None:
            raise ValueError("Entry module is required. Use with_entry() to set it.")
        
        if self._exit_module is None:
            raise ValueError("Exit module is required. Use with_exit() to set it.")
        
        if self._position_sizing_module is None:
            raise ValueError("Position sizing module is required. Use with_position_sizing() to set it.")
        
        if self._risk_module is None:
            raise ValueError("Risk management module is required. Use with_risk_management() to set it.")
    
    def _generate_default_name(self) -> str:
        """Generate default strategy name from module names"""
        return f"{self._entry_module.get_module_name()}_{self._exit_module.get_module_name()}_{self._position_sizing_module.get_module_name()}_{self._risk_module.get_module_name()}"


class TradeOrder:
    """
    Represents a trading order
    """
    def __init__(self, symbol: str, quantity: float, order_type: str = "Market", 
                 tag: str = "", timestamp: datetime = None):
        self.symbol = symbol
        self.quantity = quantity
        self.order_type = order_type
        self.tag = tag
        self.timestamp = timestamp or datetime.utcnow()


class SimpleStrategy(ISimpleStrategy):
    """
    Default implementation of ISimpleStrategy that coordinates all modules
    Converts C# SimpleStrategy to Python
    """
    
    def __init__(self, name: str, entry_module: IEntryModule, exit_module: IExitModule,
                 position_sizing_module: IPositionSizingModule, risk_module: IRiskModule):
        self.name = name
        self.entry_module = entry_module
        self.exit_module = exit_module
        self.position_sizing_module = position_sizing_module
        self.risk_module = risk_module
        
        # Track entry prices and times for exit decisions
        self._entry_prices: Dict[str, float] = {}
        self._entry_times: Dict[str, datetime] = {}
    
    def initialize(self, data: Dict[str, Any]) -> None:
        """Initialize strategy with configuration"""
        # Any initialization logic can go here
        pass
    
    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process market data and generate signals
        Args:
            data: Market data dictionary containing:
                - symbol: str
                - current_price: float
                - prices: List[float] (historical prices)
                - current_positions: Dict[str, float]
                - portfolio_value: float
                - available_cash: float
        Returns:
            Dictionary containing orders and signals
        """
        orders = []
        symbol = data.get('symbol', '')
        current_price = data.get('current_price', 0.0)
        current_positions = data.get('current_positions', {})
        portfolio_value = data.get('portfolio_value', 0.0)
        available_cash = data.get('available_cash', 0.0)
        
        current_position = current_positions.get(symbol, 0.0)
        
        try:
            # Check for exit signals first (if we have a position)
            if current_position != 0:
                entry_price = self._entry_prices.get(symbol, current_price)
                entry_time = self._entry_times.get(symbol, datetime.utcnow())
                
                # Prepare exit data
                exit_data = data.copy()
                exit_data.update({
                    'current_position': current_position,
                    'entry_price': entry_price,
                    'entry_time': entry_time
                })
                
                if self.exit_module.should_exit(exit_data):
                    # Exit the entire position
                    exit_quantity = -current_position  # Opposite sign to close
                    
                    # Validate exit trade
                    risk_data = data.copy()
                    risk_data.update({
                        'proposed_quantity': exit_quantity,
                        'current_position': current_position
                    })
                    
                    if self.risk_module.check_risk(risk_data):
                        orders.append(TradeOrder(
                            symbol=symbol,
                            quantity=exit_quantity,
                            order_type="Market",
                            tag=f"Exit-{self.exit_module.get_module_name()}",
                            timestamp=datetime.utcnow()
                        ))
                        
                        # Clear tracking data after exit
                        self._entry_prices.pop(symbol, None)
                        self._entry_times.pop(symbol, None)
            
            # Check for entry signals (if we don't have a position or after exit)
            elif self.entry_module.should_enter(data):
                # Calculate position size
                sizing_data = data.copy()
                position_size = self.position_sizing_module.calculate_size(sizing_data)
                
                # Convert position size to actual quantity
                if portfolio_value > 0 and current_price > 0:
                    dollar_amount = portfolio_value * position_size
                    quantity = dollar_amount / current_price
                    
                    # Validate entry trade
                    risk_data = data.copy()
                    risk_data.update({
                        'proposed_quantity': quantity,
                        'current_position': current_position
                    })
                    
                    if quantity > 0 and self.risk_module.check_risk(risk_data):
                        orders.append(TradeOrder(
                            symbol=symbol,
                            quantity=quantity,
                            order_type="Market",
                            tag=f"Entry-{self.entry_module.get_module_name()}",
                            timestamp=datetime.utcnow()
                        ))
                        
                        # Track entry for future exit decisions
                        self._entry_prices[symbol] = current_price
                        self._entry_times[symbol] = datetime.utcnow()
        
        except Exception as e:
            # Log error but don't crash the strategy
            print(f"Strategy {self.name} error: {str(e)}")
        
        return {
            'orders': orders,
            'entry_signal': len([o for o in orders if 'Entry' in o.tag]) > 0,
            'exit_signal': len([o for o in orders if 'Exit' in o.tag]) > 0,
            'strategy_name': self.name
        }
    
    def get_strategy_name(self) -> str:
        """Return strategy name for identification"""
        return self.name


# Convenient builder functions
def create_simple_strategy(entry_module: IEntryModule, exit_module: IExitModule,
                          sizing_module: IPositionSizingModule, risk_module: IRiskModule,
                          name: str = None) -> ISimpleStrategy:
    """
    Create a simple strategy with all modules
    Args:
        entry_module: Entry signal module
        exit_module: Exit signal module  
        sizing_module: Position sizing module
        risk_module: Risk management module
        name: Optional strategy name
    Returns:
        Configured strategy instance
    """
    builder = SimpleStrategyBuilder()
    builder.with_entry(entry_module)
    builder.with_exit(exit_module)
    builder.with_position_sizing(sizing_module)
    builder.with_risk_management(risk_module)
    
    if name:
        builder.with_name(name)
    
    return builder.build()
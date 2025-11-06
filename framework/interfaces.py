"""
Base interfaces for all modules
Establishes standard pattern for entries, exits, sizing, and risk management
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class IEntryModule(ABC):
    """Interface for entry signal modules"""
    
    @abstractmethod
    def should_enter(self, data: Dict[str, Any]) -> bool:
        """
        Determine if entry signal is triggered
        Args:
            data: Dictionary containing price data, indicators, etc.
        Returns:
            True if entry condition is met
        """
        pass
    
    @abstractmethod
    def get_module_name(self) -> str:
        """Return module name for logging and identification"""
        pass


class IExitModule(ABC):
    """Interface for exit signal modules"""
    
    @abstractmethod
    def should_exit(self, data: Dict[str, Any]) -> bool:
        """
        Determine if exit signal is triggered
        Args:
            data: Dictionary containing price data, indicators, position info, etc.
        Returns:
            True if exit condition is met
        """
        pass
    
    @abstractmethod
    def get_module_name(self) -> str:
        """Return module name for logging and identification"""
        pass


class IPositionSizingModule(ABC):
    """Interface for position sizing modules"""
    
    @abstractmethod
    def calculate_size(self, data: Dict[str, Any]) -> float:
        """
        Calculate position size
        Args:
            data: Dictionary containing account info, risk parameters, etc.
        Returns:
            Position size as percentage of portfolio (0.0 to 1.0)
        """
        pass
    
    @abstractmethod
    def get_module_name(self) -> str:
        """Return module name for logging and identification"""
        pass


class IRiskModule(ABC):
    """Interface for risk management modules"""
    
    @abstractmethod
    def check_risk(self, data: Dict[str, Any]) -> bool:
        """
        Check if trade meets risk criteria
        Args:
            data: Dictionary containing position info, account balance, etc.
        Returns:
            True if risk is acceptable
        """
        pass
    
    @abstractmethod
    def get_stop_loss(self, data: Dict[str, Any]) -> float:
        """
        Calculate stop loss level
        Args:
            data: Dictionary containing entry price, risk parameters, etc.
        Returns:
            Stop loss price level
        """
        pass
    
    @abstractmethod
    def get_module_name(self) -> str:
        """Return module name for logging and identification"""
        pass


class ISimpleStrategy(ABC):
    """Interface for complete trading strategies"""
    
    @abstractmethod
    def initialize(self, data: Dict[str, Any]) -> None:
        """Initialize strategy with configuration"""
        pass
    
    @abstractmethod
    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process market data and generate signals
        Args:
            data: Market data dictionary
        Returns:
            Dictionary containing entry/exit signals and position info
        """
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """Return strategy name for identification"""
        pass
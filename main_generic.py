# region imports
from AlgorithmImports import *
from active_strategy import ActiveStrategy
# endregion

class QCTradingFramework(QCAlgorithm):
    """
    QC Trading Framework - Generic Algorithm Wrapper
    
    This algorithm is strategy-agnostic and delegates all trading logic
    to the strategy defined in active_strategy.py
    
    To switch strategies:
    1. Copy desired strategy from strategies/ folder to active_strategy.py
    2. Deploy and run
    
    Framework Features:
    - Modular strategy architecture
    - Easy strategy switching via file copy
    - Consistent performance tracking
    - QuantConnect compatible
    """
    
    def initialize(self):
        """Initialize the framework and delegate to active strategy"""
        # Initialize the active strategy
        self.strategy = ActiveStrategy()
        self.strategy.initialize(self)
        
        # Log framework information
        self.log(f"QC TRADING FRAMEWORK INITIALIZED")
        self.log(f"  Strategy: {type(self.strategy).__name__}")
        self.log(f"  Framework Version: 1.0")

    def on_data(self, data: Slice):
        """Delegate data processing to active strategy"""
        self.strategy.on_data(self, data)

    def on_end_of_algorithm(self):
        """Delegate end-of-algorithm processing to active strategy"""
        self.strategy.on_end_of_algorithm(self)
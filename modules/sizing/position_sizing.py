"""
Position sizing modules
Converts C# FullAllocationSizing patterns to flexible Python
"""
from framework.interfaces import IPositionSizingModule
from typing import Dict, Any


class FullAllocationSizing(IPositionSizingModule):
    """
    Full allocation sizing - invests entire available capital
    Matches the C# FullAllocationSizing.cs behavior
    """
    
    def __init__(self):
        self.name = "FullAllocation"
    
    def calculate_size(self, data: Dict[str, Any]) -> float:
        """
        Calculate position size as full allocation
        Args:
            data: Dictionary containing account info
        Returns:
            1.0 (100% allocation)
        """
        return 1.0
    
    def get_module_name(self) -> str:
        return self.name


class PercentageAllocationSizing(IPositionSizingModule):
    """
    Fixed percentage allocation sizing
    More flexible than full allocation
    """
    
    def __init__(self, allocation_percent: float = 0.95):
        """
        Initialize percentage allocation
        Args:
            allocation_percent: Percentage to allocate (0.0 to 1.0)
        """
        self.allocation_percent = max(0.0, min(1.0, allocation_percent))
        self.name = f"Allocation{int(self.allocation_percent * 100)}%"
    
    def calculate_size(self, data: Dict[str, Any]) -> float:
        """
        Calculate position size as fixed percentage
        Args:
            data: Dictionary containing account info
        Returns:
            Fixed percentage allocation
        """
        return self.allocation_percent
    
    def get_module_name(self) -> str:
        return self.name


class VolatilityAdjustedSizing(IPositionSizingModule):
    """
    Volatility-adjusted position sizing
    Reduces size during high volatility periods
    """
    
    def __init__(self, base_allocation: float = 0.95, volatility_lookback: int = 20):
        """
        Initialize volatility-adjusted sizing
        Args:
            base_allocation: Base allocation percentage
            volatility_lookback: Days to look back for volatility calculation
        """
        self.base_allocation = base_allocation
        self.volatility_lookback = volatility_lookback
        self.name = f"VolAdjusted{int(base_allocation * 100)}%"
    
    def calculate_size(self, data: Dict[str, Any]) -> float:
        """
        Calculate position size adjusted for volatility
        Args:
            data: Dictionary containing 'prices' list for volatility calculation
        Returns:
            Volatility-adjusted allocation
        """
        prices = data.get('prices', [])
        
        if len(prices) < self.volatility_lookback:
            return self.base_allocation * 0.5  # Conservative if not enough data
        
        # Calculate simple volatility (standard deviation of returns)
        recent_prices = prices[-self.volatility_lookback:]
        returns = []
        for i in range(1, len(recent_prices)):
            returns.append((recent_prices[i] - recent_prices[i-1]) / recent_prices[i-1])
        
        if not returns:
            return self.base_allocation
        
        # Simple volatility calculation
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        volatility = variance ** 0.5
        
        # Adjust allocation based on volatility
        # Higher volatility = lower allocation
        volatility_adjustment = max(0.3, min(1.0, 1.0 - (volatility * 10)))
        
        return self.base_allocation * volatility_adjustment
    
    def get_module_name(self) -> str:
        return self.name


class KellyCriterionSizing(IPositionSizingModule):
    """
    Kelly Criterion position sizing
    Based on win rate and average win/loss ratios
    """
    
    def __init__(self, win_rate: float = 0.55, avg_win: float = 0.02, avg_loss: float = 0.015):
        """
        Initialize Kelly Criterion sizing
        Args:
            win_rate: Historical win rate (0.0 to 1.0)
            avg_win: Average win as decimal (0.02 = 2%)
            avg_loss: Average loss as decimal (0.015 = 1.5%)
        """
        self.win_rate = win_rate
        self.avg_win = avg_win
        self.avg_loss = avg_loss
        self.name = "KellyCriterion"
    
    def calculate_size(self, data: Dict[str, Any]) -> float:
        """
        Calculate Kelly Criterion position size
        Formula: f = (bp - q) / b
        Where: f = fraction to bet, b = odds, p = win probability, q = loss probability
        """
        if self.avg_loss <= 0:
            return 0.0
        
        b = self.avg_win / self.avg_loss  # Odds ratio
        p = self.win_rate
        q = 1 - self.win_rate
        
        kelly_fraction = (b * p - q) / b
        
        # Apply safety limits (never risk more than 25% even if Kelly suggests it)
        kelly_fraction = max(0.0, min(0.25, kelly_fraction))
        
        return kelly_fraction
    
    def get_module_name(self) -> str:
        return self.name


# Convenient wrapper functions
def create_full_allocation() -> FullAllocationSizing:
    """Create full allocation sizing (matches C# FullAllocationSizing.cs)"""
    return FullAllocationSizing()


def create_95_percent_allocation() -> PercentageAllocationSizing:
    """Create 95% allocation sizing"""
    return PercentageAllocationSizing(0.95)


def create_volatility_adjusted() -> VolatilityAdjustedSizing:
    """Create volatility-adjusted sizing with 95% base allocation"""
    return VolatilityAdjustedSizing(base_allocation=0.95)


def create_kelly_sizing() -> KellyCriterionSizing:
    """Create Kelly Criterion sizing with default parameters"""
    return KellyCriterionSizing()
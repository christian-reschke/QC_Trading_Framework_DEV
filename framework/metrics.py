"""
Performance metrics and analysis tools
Converts C# QuickResults.cs to Python
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import math


class TradeResult:
    """
    Represents a single completed trade with all relevant metrics
    Converts C# TradeResult class
    """
    
    def __init__(self, symbol: str, entry_time: datetime, exit_time: datetime,
                 entry_price: float, exit_price: float, quantity: float, tag: str = ""):
        self.symbol = symbol
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.entry_price = entry_price
        self.exit_price = exit_price
        self.quantity = quantity
        self.tag = tag
        
        # Calculate derived metrics
        self.pnl = (exit_price - entry_price) * quantity
        self.pnl_percent = self.pnl / (entry_price * abs(quantity)) if entry_price > 0 and quantity != 0 else 0
        self.is_win = self.pnl > 0
        self.duration = exit_time - entry_time


class QuickResults:
    """
    Lightweight performance metrics calculator for rapid strategy feedback
    Converts C# QuickResults.cs to Python
    """
    
    def __init__(self, starting_capital: float = 100000.0):
        self.starting_capital = starting_capital
        self._trades: List[TradeResult] = []
        self._daily_returns: List[float] = []
        
        # Initialize metrics
        self.total_return = 0.0
        self.sharpe_ratio = 0.0
        self.max_drawdown = 0.0
        self.win_rate = 0.0
        self.total_trades = 0
        self.profit_factor = 0.0
        self.average_win = 0.0
        self.average_loss = 0.0
        self.backtest_period = timedelta()
        self.annualized_return = 0.0
    
    def add_trade(self, symbol: str, entry_time: datetime, exit_time: datetime,
                  entry_price: float, exit_price: float, quantity: float, tag: str = ""):
        """
        Add a completed trade to the performance calculation
        Args:
            symbol: Security symbol
            entry_time: Trade entry timestamp
            exit_time: Trade exit timestamp
            entry_price: Entry price
            exit_price: Exit price
            quantity: Number of shares/contracts
            tag: Optional trade tag for identification
        """
        trade = TradeResult(symbol, entry_time, exit_time, entry_price, exit_price, quantity, tag)
        self._trades.append(trade)
        self._recalculate_metrics()
    
    def add_daily_return(self, daily_return: float):
        """
        Add daily portfolio returns for Sharpe ratio calculation
        Args:
            daily_return: Daily return as decimal (0.01 = 1%)
        """
        self._daily_returns.append(daily_return)
        self._recalculate_metrics()
    
    def get_summary(self) -> str:
        """
        Get a formatted summary of key metrics
        Returns:
            Formatted string with performance summary
        """
        return f"""
=== QUICK RESULTS SUMMARY ===
Total Return: {self.total_return:.2%}
Annualized Return: {self.annualized_return:.2%}
Sharpe Ratio: {self.sharpe_ratio:.2f}
Max Drawdown: {self.max_drawdown:.2%}
Win Rate: {self.win_rate:.1%}
Total Trades: {self.total_trades}
Profit Factor: {self.profit_factor:.2f}
Average Win: ${self.average_win:,.2f}
Average Loss: ${self.average_loss:,.2f}
Backtest Period: {self.backtest_period.days:.0f} days
==========================="""
    
    def get_trades(self) -> List[TradeResult]:
        """
        Get individual trade details for analysis
        Returns:
            List of completed trades
        """
        return self._trades.copy()
    
    def get_metrics_dict(self) -> Dict[str, Any]:
        """
        Get all metrics as a dictionary for programmatic access
        Returns:
            Dictionary containing all calculated metrics
        """
        return {
            'total_return': self.total_return,
            'annualized_return': self.annualized_return,
            'sharpe_ratio': self.sharpe_ratio,
            'max_drawdown': self.max_drawdown,
            'win_rate': self.win_rate,
            'total_trades': self.total_trades,
            'profit_factor': self.profit_factor,
            'average_win': self.average_win,
            'average_loss': self.average_loss,
            'backtest_period_days': self.backtest_period.days,
            'starting_capital': self.starting_capital
        }
    
    def _recalculate_metrics(self):
        """Recalculate all performance metrics"""
        if not self._trades:
            self._reset_metrics()
            return
        
        self.total_trades = len(self._trades)
        
        # Calculate total return
        total_pnl = sum(trade.pnl for trade in self._trades)
        self.total_return = total_pnl / self.starting_capital
        
        # Calculate win rate
        wins = sum(1 for trade in self._trades if trade.is_win)
        self.win_rate = wins / self.total_trades
        
        # Calculate average win/loss
        winning_trades = [trade for trade in self._trades if trade.is_win]
        losing_trades = [trade for trade in self._trades if not trade.is_win]
        
        self.average_win = sum(trade.pnl for trade in winning_trades) / len(winning_trades) if winning_trades else 0
        self.average_loss = sum(abs(trade.pnl) for trade in losing_trades) / len(losing_trades) if losing_trades else 0
        
        # Calculate profit factor
        gross_profit = sum(trade.pnl for trade in winning_trades)
        gross_loss = abs(sum(trade.pnl for trade in losing_trades))
        self.profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
        
        # Calculate backtest period
        if len(self._trades) > 1:
            self.backtest_period = max(trade.exit_time for trade in self._trades) - min(trade.entry_time for trade in self._trades)
            
            # Calculate annualized return
            if self.backtest_period.days > 0:
                annual_multiplier = 365.25 / self.backtest_period.days
                self.annualized_return = (1 + self.total_return) ** annual_multiplier - 1
        
        # Calculate Sharpe ratio
        if len(self._daily_returns) > 1:
            avg_daily_return = sum(self._daily_returns) / len(self._daily_returns)
            daily_std_dev = self._calculate_standard_deviation(self._daily_returns)
            if daily_std_dev > 0:
                self.sharpe_ratio = (avg_daily_return * math.sqrt(252)) / (daily_std_dev * math.sqrt(252))
        
        # Calculate max drawdown
        self.max_drawdown = self._calculate_max_drawdown()
    
    def _calculate_max_drawdown(self) -> float:
        """Calculate maximum drawdown using trade PnL"""
        if not self._trades:
            return 0.0
        
        running_capital = self.starting_capital
        peak = self.starting_capital
        max_drawdown = 0.0
        
        # Sort trades by exit time
        sorted_trades = sorted(self._trades, key=lambda t: t.exit_time)
        
        for trade in sorted_trades:
            running_capital += trade.pnl
            
            if running_capital > peak:
                peak = running_capital
            
            drawdown = (peak - running_capital) / peak if peak > 0 else 0
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        return max_drawdown
    
    def _calculate_standard_deviation(self, values: List[float]) -> float:
        """Calculate standard deviation of a list of values"""
        if len(values) < 2:
            return 0.0
        
        avg = sum(values) / len(values)
        sum_squared_diffs = sum((value - avg) ** 2 for value in values)
        return math.sqrt(sum_squared_diffs / (len(values) - 1))
    
    def _reset_metrics(self):
        """Reset all metrics to zero"""
        self.total_return = 0.0
        self.sharpe_ratio = 0.0
        self.max_drawdown = 0.0
        self.win_rate = 0.0
        self.total_trades = 0
        self.profit_factor = 0.0
        self.average_win = 0.0
        self.average_loss = 0.0
        self.backtest_period = timedelta()
        self.annualized_return = 0.0


def create_quick_results(starting_capital: float = 100000.0) -> QuickResults:
    """
    Create a QuickResults instance
    Args:
        starting_capital: Starting portfolio value
    Returns:
        Configured QuickResults instance
    """
    return QuickResults(starting_capital)
"""
SPY EMA Strategy - Python conversion from C# SPYEMAStrategy.cs
Entry: Price > EMA50
Exit: Price < EMA100
Allocation: 100% of portfolio
"""
from framework.strategy_builder import SimpleStrategyBuilder, TradeOrder
from modules.entries import create_ema50_entry
from modules.exits import create_ema100_exit
from modules.sizing import create_full_allocation
from modules.risk import create_basic_risk
from typing import Dict, List, Any
from datetime import datetime, timedelta
import random


class SPYEMAStrategy:
    """
    SPY EMA Crossover Strategy
    Converts C# SPYEMAStrategy.cs to Python
    """
    
    def __init__(self):
        # Build the strategy using modules
        self.strategy = (SimpleStrategyBuilder()
                        .with_name("SPY EMA50/100 Crossover")
                        .with_entry(create_ema50_entry())
                        .with_exit(create_ema100_exit())
                        .with_position_sizing(create_full_allocation())
                        .with_risk_management(create_basic_risk())
                        .build())
        
        # Track portfolio state
        self.starting_capital = 1_000_000.0
        self.positions = {}
        self.portfolio_value = self.starting_capital
        self.available_cash = self.starting_capital
        self.completed_trades = []
    
    def run_backtest(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, Any]:
        """
        Run the SPY EMA strategy backtest
        Args:
            start_date: Backtest start date (defaults to Q3 2025)
            end_date: Backtest end date (defaults to Q3 2025)
        Returns:
            Dictionary with backtest results
        """
        if start_date is None:
            start_date = datetime(2025, 7, 1)
        if end_date is None:
            end_date = datetime(2025, 9, 30)
        
        print("SPY EMA CROSSOVER STRATEGY - Q3 2025 BACKTEST")
        print("=" * 48)
        print("Strategy Rules:")
        print("   * BUY SPY when close > EMA50")
        print("   * SELL SPY when close < EMA100")
        print("   * Allocation: 100% of portfolio")
        print("   * Timeframe: Daily")
        print("   * Period: Q3 2025 (Jul-Sep)")
        print(f"   * Starting Capital: ${self.starting_capital:,.0f}")
        print()
        
        print(f"Strategy Built: {self.strategy.get_strategy_name()}")
        print(f"   Entry: {self.strategy.entry_module.get_module_name()}")
        print(f"   Exit: {self.strategy.exit_module.get_module_name()}")
        print(f"   Sizing: {self.strategy.position_sizing_module.get_module_name()}")
        print(f"   Risk: {self.strategy.risk_module.get_module_name()}")
        print()
        
        # Generate Q3 2025 SPY data with warm-up period
        spy_data = self._generate_q3_2025_spy_data()
        
        print("Running Backtest...")
        print("Date        | Close   | Action")
        print("------------|---------|------------------")
        
        # Track entry details
        entry_price = 0.0
        entry_time = None
        
        for data_point in spy_data:
            current_position = self.positions.get("SPY", 0.0)
            
            # Update portfolio value
            if current_position != 0:
                self.portfolio_value = self.available_cash + (current_position * data_point['close'])
            
            # Prepare data for strategy
            strategy_data = {
                'symbol': 'SPY',
                'current_price': data_point['close'],
                'prices': data_point['price_history'],
                'current_positions': self.positions.copy(),
                'portfolio_value': self.portfolio_value,
                'available_cash': self.available_cash
            }
            
            # Process strategy
            result = self.strategy.process_data(strategy_data)
            orders = result.get('orders', [])
            
            action = "HOLD"
            for order in orders:
                if 'Entry' in order.tag:
                    # Entry trade
                    self.positions["SPY"] = order.quantity
                    self.available_cash -= order.quantity * data_point['close']
                    entry_price = data_point['close']
                    entry_time = data_point['timestamp']
                    action = f"BUY {order.quantity:.0f} shares"
                    
                elif 'Exit' in order.tag:
                    # Exit trade
                    self.available_cash += current_position * data_point['close']
                    
                    # Record completed trade
                    if entry_time:
                        self.completed_trades.append({
                            'symbol': 'SPY',
                            'entry_time': entry_time,
                            'exit_time': data_point['timestamp'],
                            'entry_price': entry_price,
                            'exit_price': data_point['close'],
                            'quantity': current_position,
                            'pnl': (data_point['close'] - entry_price) * current_position
                        })
                    
                    self.positions["SPY"] = 0
                    action = f"SELL {current_position:.0f} shares"
            
            # Only show Q3 data in output
            if data_point['timestamp'] >= start_date:
                print(f"{data_point['timestamp'].strftime('%m/%d/%Y')} | ${data_point['close']:.2f}  | {action}")
        
        # Calculate final results
        final_position = self.positions.get("SPY", 0.0)
        if final_position != 0:
            final_price = spy_data[-1]['close']
            self.portfolio_value = self.available_cash + (final_position * final_price)
        else:
            self.portfolio_value = self.available_cash
        
        return self._generate_results()
    
    def _generate_results(self) -> Dict[str, Any]:
        """Generate backtest results summary"""
        total_return = (self.portfolio_value - self.starting_capital) / self.starting_capital
        
        results = {
            'starting_capital': self.starting_capital,
            'ending_portfolio': self.portfolio_value,
            'total_return': total_return,
            'total_trades': len(self.completed_trades),
            'completed_trades': self.completed_trades
        }
        
        # Calculate trade statistics if we have trades
        if self.completed_trades:
            winning_trades = [t for t in self.completed_trades if t['pnl'] > 0]
            losing_trades = [t for t in self.completed_trades if t['pnl'] <= 0]
            
            results.update({
                'winning_trades': len(winning_trades),
                'losing_trades': len(losing_trades),
                'win_rate': len(winning_trades) / len(self.completed_trades) if self.completed_trades else 0,
                'avg_win': sum(t['pnl'] for t in winning_trades) / len(winning_trades) if winning_trades else 0,
                'avg_loss': sum(t['pnl'] for t in losing_trades) / len(losing_trades) if losing_trades else 0,
                'total_pnl': sum(t['pnl'] for t in self.completed_trades)
            })
        
        return results
    
    def _generate_q3_2025_spy_data(self) -> List[Dict[str, Any]]:
        """
        Generate realistic SPY data for Q3 2025 with warm-up period
        Converts C# GenerateQ3_2025_SPYData method
        """
        data = []
        
        # Start earlier to warm up EMAs (need 100+ days for EMA100)
        start_date = datetime(2025, 3, 1)  # Start in March for warm-up
        end_date = datetime(2025, 9, 30)   # Q3 end
        
        base_price = 450.0  # Realistic SPY price for 2025
        current_date = start_date
        price = base_price
        random.seed(42)  # Fixed seed for reproducible results
        
        # Track price history for EMA calculations
        price_history = []
        
        # Create trending market with volatility to generate crossovers
        trend_phase = 0  # 0 = down, 1 = up, 2 = sideways
        days_since_phase_change = 0
        
        while current_date <= end_date:
            # Skip weekends
            if current_date.weekday() < 5:  # Monday=0, Sunday=6
                days_since_phase_change += 1
                
                # Change trend phases to create crossovers
                if days_since_phase_change > 30:
                    trend_phase = (trend_phase + 1) % 3
                    days_since_phase_change = 0
                
                # Generate price movement based on trend phase
                if trend_phase == 0:  # Down trend
                    trend_component = -0.005  # -0.5% daily trend
                elif trend_phase == 1:  # Up trend
                    trend_component = 0.006   # +0.6% daily trend
                else:  # Sideways
                    trend_component = 0.0
                
                # Add random daily movement
                random_component = (random.random() * 0.04 - 0.02)  # +/- 2% random
                daily_return = trend_component + random_component
                
                price = price * (1 + daily_return)
                
                # Keep price in reasonable range
                price = max(350.0, min(550.0, price))
                price = round(price, 2)
                
                # Add to price history
                price_history.append(price)
                
                data.append({
                    'symbol': 'SPY',
                    'close': price,
                    'open': round(price * 0.999, 2),
                    'high': round(price * 1.005, 2),
                    'low': round(price * 0.995, 2),
                    'volume': 50_000_000 + random.randint(0, 20_000_000),
                    'timestamp': current_date,
                    'price_history': price_history.copy()  # Full history for EMA calculation
                })
            
            current_date += timedelta(days=1)
        
        return data
    
    def print_results(self, results: Dict[str, Any]):
        """Print formatted backtest results"""
        print()
        print("BACKTEST RESULTS:")
        print("=" * 19)
        print(f"Starting Capital: ${results['starting_capital']:,.0f}")
        print(f"Ending Portfolio: ${results['ending_portfolio']:,.0f}")
        print(f"Total Return: {results['total_return']:.2%}")
        print()
        
        if results['total_trades'] > 0:
            print(f"Total Trades: {results['total_trades']}")
            print(f"Winning Trades: {results['winning_trades']}")
            print(f"Losing Trades: {results['losing_trades']}")
            print(f"Win Rate: {results['win_rate']:.1%}")
            if results['avg_win'] > 0:
                print(f"Average Win: ${results['avg_win']:,.2f}")
            if results['avg_loss'] < 0:
                print(f"Average Loss: ${results['avg_loss']:,.2f}")
            print(f"Total P&L: ${results['total_pnl']:,.2f}")
        else:
            print("No completed trades during the period.")
            print("(This could mean the strategy stayed in a position through Q3)")
        
        print()
        print("STRATEGY TEST COMPLETE!")
        print("Ready to implement in QuantConnect for real backtesting!")


def main():
    """Run the SPY EMA strategy backtest"""
    strategy = SPYEMAStrategy()
    results = strategy.run_backtest()
    strategy.print_results(results)


if __name__ == "__main__":
    main()
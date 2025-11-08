"""
Demo script showing the new class-based QCOutputParser API
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import QCOutputParser
from examples.backtest_outputs_from_qc import get_backtest_output, get_negative_backtest_output

def demo_positive_case():
    """Demo the positive performance case"""
    print("=" * 60)
    print("POSITIVE PERFORMANCE CASE")
    print("=" * 60)
    
    parser = QCOutputParser(get_backtest_output())
    
    print(f"Backtest Name:     {parser.get_backtest_name()}")
    print(f"Strategy Version:  {parser.get_strategy_version()}")
    print(f"Return:           {parser.get_return_percent():.2f}%")
    
    annual_return = parser.get_annual_return_percent()
    print(f"Annual Return:    {annual_return:.3f}%" if annual_return else "Annual Return:    N/A")
    
    print(f"Max Drawdown:     {parser.get_max_drawdown_percent():.1f}%")
    print(f"Sharpe Ratio:     {parser.get_sharpe_ratio():.3f}")
    print(f"Sortino Ratio:    {parser.get_sortino_ratio():.3f}")
    print(f"Total Orders:     {parser.get_total_orders()}")
    print(f"Win Rate:         {parser.get_win_rate_percent()}%")
    print(f"Loss Rate:        {parser.get_loss_rate_percent()}%")
    print(f"P/L Ratio:        {parser.get_profit_loss_ratio():.2f}")
    print(f"Expectancy:       {parser.get_expectancy():.3f}")
    print(f"Total Fees:       ${parser.get_total_fees():.2f}")
    print(f"Final Equity:     ${parser.get_final_equity():,.2f}")

def demo_negative_case():
    """Demo the negative performance case"""
    print("\n" + "=" * 60)
    print("NEGATIVE PERFORMANCE CASE")
    print("=" * 60)
    
    parser = QCOutputParser(get_negative_backtest_output())
    
    print(f"Backtest Name:     {parser.get_backtest_name()}")
    print(f"Strategy Version:  {parser.get_strategy_version()}")
    print(f"Return:           {parser.get_return_percent():.2f}%")
    
    annual_return = parser.get_annual_return_percent()
    print(f"Annual Return:    {annual_return:.3f}%" if annual_return else "Annual Return:    N/A")
    
    print(f"Max Drawdown:     {parser.get_max_drawdown_percent():.1f}%")
    print(f"Sharpe Ratio:     {parser.get_sharpe_ratio():.3f}")
    print(f"Sortino Ratio:    {parser.get_sortino_ratio():.3f}")
    print(f"Total Orders:     {parser.get_total_orders()}")
    print(f"Win Rate:         {parser.get_win_rate_percent()}%")
    print(f"Loss Rate:        {parser.get_loss_rate_percent()}%")
    print(f"P/L Ratio:        {parser.get_profit_loss_ratio():.2f}")
    print(f"Expectancy:       {parser.get_expectancy():.3f}")
    print(f"Total Fees:       ${parser.get_total_fees():.2f}")
    print(f"Final Equity:     ${parser.get_final_equity():,.2f}")

def demo_comparison():
    """Demo comparing both cases"""
    print("\n" + "=" * 60)
    print("COMPARISON")
    print("=" * 60)
    
    pos_parser = QCOutputParser(get_backtest_output())
    neg_parser = QCOutputParser(get_negative_backtest_output())
    
    print(f"{'Metric':<20} {'Positive Case':<15} {'Negative Case':<15}")
    print("-" * 50)
    print(f"{'Return %':<20} {pos_parser.get_return_percent():<15.2f} {neg_parser.get_return_percent():<15.2f}")
    print(f"{'Sharpe Ratio':<20} {pos_parser.get_sharpe_ratio():<15.3f} {neg_parser.get_sharpe_ratio():<15.3f}")
    print(f"{'Max Drawdown %':<20} {pos_parser.get_max_drawdown_percent():<15.1f} {neg_parser.get_max_drawdown_percent():<15.1f}")
    print(f"{'Win Rate %':<20} {pos_parser.get_win_rate_percent():<15} {neg_parser.get_win_rate_percent():<15}")
    print(f"{'Expectancy':<20} {pos_parser.get_expectancy():<15.3f} {neg_parser.get_expectancy():<15.3f}")

if __name__ == "__main__":
    demo_positive_case()
    demo_negative_case()
    demo_comparison()
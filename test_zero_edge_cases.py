"""
Test to check potential type issues with zero values
"""
from utils import QCOutputParser

# Use the zero values output
zero_values_output = """Started backtest named 'Crawling Brown Badger' for project 'Test'
+-----------------------------------------------------------------------------+
| Return                   | 0.00 %      | Sharpe Ratio              | 0      |
| Drawdown                 | 0%          | Total Orders              | 0      |
+-----------------------------------------------------------------------------+
Backtest id: test"""

parser = QCOutputParser(zero_values_output)

print("Testing potential issues with zero values...")
print("=" * 50)

# Test what might be problematic
return_val = parser.get_return_percent()
sharpe_val = parser.get_sharpe_ratio()
drawdown_val = parser.get_max_drawdown_percent()
orders_val = parser.get_total_orders()

print(f"Return: {return_val} (type: {type(return_val)}, truthiness: {bool(return_val)})")
print(f"Sharpe: {sharpe_val} (type: {type(sharpe_val)}, truthiness: {bool(sharpe_val)})")
print(f"Drawdown: {drawdown_val} (type: {type(drawdown_val)}, truthiness: {bool(drawdown_val)})")
print(f"Orders: {orders_val} (type: {type(orders_val)}, truthiness: {bool(orders_val)})")

print("\nChecking if values are exactly zero:")
print(f"Return == 0: {return_val == 0}")
print(f"Return == 0.0: {return_val == 0.0}")
print(f"Sharpe == 0: {sharpe_val == 0}")
print(f"Orders == 0: {orders_val == 0}")

print("\nChecking for potential None values:")
print(f"Return is None: {return_val is None}")
print(f"Sharpe is None: {sharpe_val is None}")

# Test some edge cases that might be problematic
print("\nChecking parsed data directly:")
data = parser.to_dict()
print(f"Raw performance_metrics: {data['performance_metrics']}")
print(f"Raw risk_metrics: {data['risk_metrics']}")
print(f"Raw trade_metrics: {data['trade_metrics']}")

# Check if any values are None
def check_for_none_values(data_dict, path=""):
    for key, value in data_dict.items():
        current_path = f"{path}.{key}" if path else key
        if isinstance(value, dict):
            check_for_none_values(value, current_path)
        elif value is None:
            print(f"Found None value at: {current_path}")

print("\nChecking for None values in parsed data:")
check_for_none_values(data)
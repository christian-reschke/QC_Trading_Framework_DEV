"""
Deep test of parser's _parse_metric_value method with various zero formats
"""
from utils import QCOutputParser

# Create a test parser instance using the working zero values output
zero_values_output = """Started backtest named 'Test' for project 'Test'
+-----------------------------------------------------------------------------+
| Return                   | 0.00 %      | Sharpe Ratio              | 0      |
| Drawdown                 | 0%          |                           |        |
+-----------------------------------------------------------------------------+
Backtest id: test"""

parser = QCOutputParser(zero_values_output)

# Test various zero value formats
test_values = [
    "0",           # Simple zero
    "0.0",         # Zero with decimal
    "0.00",        # Zero with two decimals
    "0%",          # Zero percent
    "0.0%",        # Zero percent with decimal
    "0.00%",       # Zero percent with two decimals
    "0.00 %",      # Zero percent with space
    "$0",          # Zero dollars
    "$0.0",        # Zero dollars with decimal
    "$0.00",       # Zero dollars with two decimals
    "-$0.00",      # Negative zero dollars
    "",            # Empty string
    "-",           # Dash
    "   ",         # Spaces
    "0 ",          # Zero with trailing space
    " 0",          # Zero with leading space
]

print("Testing _parse_metric_value with various zero formats:")
print("=" * 60)

for test_val in test_values:
    try:
        result = parser._parse_metric_value(test_val)
        print(f"'{test_val}' -> {result} (type: {type(result).__name__})")
    except Exception as e:
        print(f"'{test_val}' -> ERROR: {e}")

print("\n" + "=" * 60)
print("Testing problematic regex patterns...")

# Test if the regex patterns are matching zero values correctly
import re

test_output = """
| Total Orders             | 0           | Average Win               | 0%     |
| Return                   | 0.00 %      | Sharpe Ratio              | 0      |
| Fees                     | -$0.00      | Net Profit                | $0.00  |
"""

# Test the regex pattern used in the parser
metrics_to_test = ["Total Orders", "Average Win", "Return", "Sharpe Ratio", "Fees", "Net Profit"]

for metric in metrics_to_test:
    pattern = rf"{re.escape(metric)}\s*\|\s*([^\|]+?)(?:\s*\||\s*$)"
    match = re.search(pattern, test_output, re.MULTILINE)
    
    if match:
        raw_value = match.group(1).strip()
        parsed = parser._parse_metric_value(raw_value)
        print(f"{metric}: '{raw_value}' -> {parsed} (type: {type(parsed).__name__})")
    else:
        print(f"{metric}: NO MATCH FOUND")
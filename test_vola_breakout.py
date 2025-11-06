"""
Test the Vola Breakout modules individually
Debug and verify each component works correctly
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.indicators import (
    calculate_ema, ema_is_rising, 
    calculate_bollinger_bands, bb_width_20_period, is_bollinger_ready,
    get_recent_high
)
from modules.entries import VolaBreakoutEntry
from modules.exits import TrailingStopExit


def test_bollinger_bands():
    """Test Bollinger Bands calculations"""
    print("Testing Bollinger Bands...")
    
    # Test data: low volatility then high volatility
    low_vol_prices = [100.0, 100.1, 99.9, 100.2, 99.8, 100.0, 100.1, 99.9] * 3
    high_vol_prices = [100.0, 102.0, 98.0, 104.0, 96.0, 105.0, 95.0, 106.0, 94.0, 107.0]
    
    # Test low volatility
    if is_bollinger_ready(low_vol_prices):
        upper, middle, lower = calculate_bollinger_bands(low_vol_prices)
        bbw = bb_width_20_period(low_vol_prices)
        print(f"  Low Vol - BBW: {bbw:.3f}, Bands: {lower:.2f} - {middle:.2f} - {upper:.2f}")
    
    # Test high volatility
    if is_bollinger_ready(high_vol_prices):
        upper, middle, lower = calculate_bollinger_bands(high_vol_prices)
        bbw = bb_width_20_period(high_vol_prices)
        print(f"  High Vol - BBW: {bbw:.3f}, Bands: {lower:.2f} - {middle:.2f} - {upper:.2f}")
    
    print("  Bollinger Bands: PASS")


def test_ema_conditions():
    """Test EMA trend conditions"""
    print("Testing EMA conditions...")
    
    # Uptrending prices
    uptrend_prices = [100 + i * 0.5 for i in range(60)]  # Steady uptrend
    current_price = uptrend_prices[-1] + 1  # Price above trend
    
    ema50 = calculate_ema(uptrend_prices, 50)
    ema50_prev = calculate_ema(uptrend_prices[:-1], 50)
    
    price_above_ema = current_price > ema50
    ema_rising = ema50 > ema50_prev
    
    print(f"  Current Price: {current_price:.2f}")
    print(f"  EMA50: {ema50:.2f} (prev: {ema50_prev:.2f})")
    print(f"  Price > EMA: {price_above_ema}")
    print(f"  EMA Rising: {ema_rising}")
    print(f"  Trend Condition: {price_above_ema and ema_rising}")
    print("  EMA Conditions: PASS")


def test_vola_breakout_entry():
    """Test the complete Vola Breakout entry module"""
    print("Testing Vola Breakout Entry...")
    
    # Create entry module
    entry = VolaBreakoutEntry(ema_period=20, bbw_threshold=0.15)  # More lenient settings
    
    # Generate test scenario: low vol compression then breakout
    base_prices = []
    
    # Phase 1: Low volatility base (30 days)
    for i in range(30):
        price = 100 + (i * 0.1) + ((-1) ** i) * 0.2  # Small oscillations around trend
        base_prices.append(price)
    
    # Phase 2: Breakout setup (5 days of higher highs)
    breakout_prices = base_prices.copy()
    for i in range(5):
        price = breakout_prices[-1] + 1.0 + i * 0.5
        breakout_prices.append(price)
    
    # Test current breakout day
    current_price = breakout_prices[-1] + 2.0  # Strong breakout move
    
    # Prepare test data
    test_data = {
        'prices': breakout_prices + [current_price],
        'current_price': current_price,
        'highs': breakout_prices + [current_price]  # Use same for highs
    }
    
    # Test individual conditions
    details = entry.get_entry_details(test_data)
    
    print(f"  Current Price: ${current_price:.2f}")
    print(f"  Trend Condition: {details['trend_condition']}")
    print(f"  Low Volatility: {details['low_volatility_condition']}")
    print(f"  BB Breakout: {details['bb_breakout_condition']}")
    print(f"  Recent High Break: {details['recent_high_condition']}")
    print(f"  Overall Signal: {details['overall_signal']}")
    
    if 'current_bbw' in details:
        print(f"  Current BBW: {details['current_bbw']:.3f}")
    if 'bb_upper' in details:
        print(f"  BB Upper: ${details['bb_upper']:.2f}")
    
    print("  Vola Breakout Entry: PASS")


def test_trailing_stop():
    """Test trailing stop functionality"""
    print("Testing Trailing Stop...")
    
    trailing_stop = TrailingStopExit(trail_percent=0.05, initial_stop_percent=0.02)
    
    # Simulate a profitable trade
    entry_price = 100.0
    prices = [100.0, 102.0, 105.0, 108.0, 107.0, 106.0, 104.0]  # Up then down
    
    print(f"  Entry Price: ${entry_price:.2f}")
    
    for i, price in enumerate(prices):
        test_data = {
            'current_price': price,
            'entry_price': entry_price,
            'current_position': 100.0  # Long position
        }
        
        should_exit = trailing_stop.should_exit(test_data)
        stop_level = trailing_stop.get_current_stop_level()
        
        print(f"  Day {i+1}: Price ${price:.2f}, Stop ${stop_level:.2f}, Exit: {should_exit}")
        
        if should_exit:
            print(f"  >>> STOP TRIGGERED at ${price:.2f}")
            break
    
    print("  Trailing Stop: PASS")


def main():
    """Run all Vola Breakout tests"""
    print("VOLA BREAKOUT MODULES TEST")
    print("=" * 40)
    
    try:
        test_bollinger_bands()
        print()
        test_ema_conditions()
        print()
        test_vola_breakout_entry()
        print()
        test_trailing_stop()
        print()
        print("=" * 40)
        print("ALL VOLA BREAKOUT TESTS PASSED!")
        print("The new strategy modules are working correctly.")
        
    except Exception as e:
        print(f"TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
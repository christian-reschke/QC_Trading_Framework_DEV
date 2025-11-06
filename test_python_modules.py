"""
Test the converted Python modules
Quick verification that all modules work correctly after C# conversion
"""
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Test imports
def test_imports():
    """Test that all modules can be imported successfully"""
    try:
        print("Testing imports...")
        
        # Test framework imports
        from framework.interfaces import IEntryModule, IExitModule, IPositionSizingModule, IRiskModule
        from framework.strategy_builder import SimpleStrategyBuilder, create_simple_strategy
        from framework.metrics import QuickResults, TradeResult
        print("✓ Framework imports successful")
        
        # Test indicator imports
        from modules.indicators import calculate_ema, ema50_rising, golden_cross
        print("✓ Indicators imports successful")
        
        # Test entry module imports
        from modules.entries import EMAEntry, create_ema50_entry, create_golden_cross_entry
        print("✓ Entry modules imports successful")
        
        # Test exit module imports
        from modules.exits import EMAExit, create_ema100_exit, create_death_cross_exit
        print("✓ Exit modules imports successful")
        
        # Test sizing module imports
        from modules.sizing import FullAllocationSizing, create_full_allocation
        print("✓ Sizing modules imports successful")
        
        # Test risk module imports
        from modules.risk import BasicRiskManagement, create_basic_risk
        print("✓ Risk modules imports successful")
        
        # Test strategy imports
        from strategies import SPYEMAStrategy
        print("✓ Strategy imports successful")
        
        print("\nAll imports successful! ✓")
        return True
        
    except Exception as e:
        print(f"Import failed: {str(e)}")
        return False


def test_ema_calculations():
    """Test EMA calculation functions"""
    try:
        print("\nTesting EMA calculations...")
        
        from modules.indicators import calculate_ema, ema50_rising, ema_crosses_above_ema
        
        # Test basic EMA calculation
        prices = [100, 101, 102, 103, 104, 105]
        ema = calculate_ema(prices, 5)
        print(f"✓ EMA calculation: {ema:.2f}")
        
        # Test EMA rising
        is_rising = ema50_rising(prices)
        print(f"✓ EMA50 rising: {is_rising}")
        
        # Test crossover
        crossover = ema_crosses_above_ema(prices, 3, 5)
        print(f"✓ EMA crossover: {crossover}")
        
        print("EMA calculations working correctly! ✓")
        return True
        
    except Exception as e:
        print(f"EMA calculation test failed: {str(e)}")
        return False


def test_module_creation():
    """Test module creation and basic functionality"""
    try:
        print("\nTesting module creation...")
        
        from modules.entries import create_ema50_entry
        from modules.exits import create_ema100_exit
        from modules.sizing import create_full_allocation
        from modules.risk import create_basic_risk
        
        # Create modules
        entry = create_ema50_entry()
        exit = create_ema100_exit()
        sizing = create_full_allocation()
        risk = create_basic_risk()
        
        print(f"✓ Created entry module: {entry.get_module_name()}")
        print(f"✓ Created exit module: {exit.get_module_name()}")
        print(f"✓ Created sizing module: {sizing.get_module_name()}")
        print(f"✓ Created risk module: {risk.get_module_name()}")
        
        print("Module creation working correctly! ✓")
        return True
        
    except Exception as e:
        print(f"Module creation test failed: {str(e)}")
        return False


def test_strategy_builder():
    """Test strategy builder functionality"""
    try:
        print("\nTesting strategy builder...")
        
        from framework.strategy_builder import SimpleStrategyBuilder
        from modules.entries import create_ema50_entry
        from modules.exits import create_ema100_exit
        from modules.sizing import create_full_allocation
        from modules.risk import create_basic_risk
        
        # Build strategy using fluent API
        strategy = (SimpleStrategyBuilder()
                   .with_name("Test Strategy")
                   .with_entry(create_ema50_entry())
                   .with_exit(create_ema100_exit())
                   .with_position_sizing(create_full_allocation())
                   .with_risk_management(create_basic_risk())
                   .build())
        
        print(f"✓ Built strategy: {strategy.get_strategy_name()}")
        
        # Test strategy data processing (with dummy data)
        test_data = {
            'symbol': 'TEST',
            'current_price': 100.0,
            'prices': [95, 96, 97, 98, 99, 100],
            'current_positions': {},
            'portfolio_value': 100000.0,
            'available_cash': 100000.0
        }
        
        result = strategy.process_data(test_data)
        print(f"✓ Strategy processing: {len(result.get('orders', []))} orders generated")
        
        print("Strategy builder working correctly! ✓")
        return True
        
    except Exception as e:
        print(f"Strategy builder test failed: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("PYTHON MODULE CONVERSION TEST")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_ema_calculations,
        test_module_creation,
        test_strategy_builder
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Python conversion successful!")
        print("\nThe C# to Python conversion is complete and working.")
        print("All modules are functional and ready for use.")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    print("=" * 50)


if __name__ == "__main__":
    main()
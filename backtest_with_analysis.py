#!/usr/bin/env python3
"""
Enhanced backtest runner that captures and displays performance comparison
"""

import subprocess
import re
import sys
import os
from datetime import datetime

def run_backtest_with_capture():
    """
    Run the backtest and try to capture output for analysis
    """
    print("\n🚀 RUNNING BACKTEST WITH PERFORMANCE CAPTURE...")
    print("="*70)
    
    try:
        # Get project paths
        current_dir = os.getcwd()
        parent_dir = os.path.dirname(current_dir)
        project_name = os.path.basename(current_dir)
        deploy_name = project_name.replace('_DEV', '_DEPLOY')
        
        print(f"📁 Project: {deploy_name}")
        print(f"📍 Location: {parent_dir}")
        
        # Change to parent directory for lean command
        os.chdir(parent_dir)
        
        # Run the lean backtest command
        lean_exe = r"C:\Users\chris\pipx\venvs\lean\Scripts\lean.exe"
        cmd = [lean_exe, "cloud", "backtest", deploy_name]
        
        print(f"\n⚡ Executing: {' '.join(cmd)}")
        print("-"*50)
        
        # Run and capture output
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        # Display the output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:", result.stderr)
        
        # Try to extract backtest URL for logs
        backtest_url_match = re.search(r'Backtest url: (https://[^\s]+)', result.stdout)
        if backtest_url_match:
            backtest_url = backtest_url_match.group(1)
            print(f"\n🔗 BACKTEST URL: {backtest_url}")
            
            # Store URL for easy access
            with open('latest_backtest_url.txt', 'w') as f:
                f.write(f"{backtest_url}\n")
                f.write(f"Generated: {datetime.now()}\n")
        
        # Change back to original directory
        os.chdir(current_dir)
        
        return result.returncode == 0, backtest_url if backtest_url_match else None
        
    except subprocess.TimeoutExpired:
        print("❌ Backtest timed out after 5 minutes")
        return False, None
    except Exception as e:
        print(f"❌ Error running backtest: {e}")
        return False, None

def extract_performance_from_output(output_text):
    """
    Extract the actual performance comparison from algorithm logs
    """
    performance_data = {}
    
    # Look for our custom performance comparison section
    lines = output_text.split('\n')
    in_comparison_section = False
    
    for line in lines:
        if "BACKTEST COMPLETE - PERFORMANCE COMPARISON" in line:
            in_comparison_section = True
            continue
            
        if in_comparison_section and line.strip().startswith('='):
            in_comparison_section = False
            break
            
        if in_comparison_section:
            # Extract strategy performance
            if "Final Portfolio Value:" in line:
                match = re.search(r'\$([0-9,]+)', line)
                if match:
                    performance_data['strategy_final'] = match.group(1).replace(',', '')
            
            elif "Total Return:" in line and "STRATEGY" in lines[lines.index(line)-3:lines.index(line)]:
                match = re.search(r'([0-9.]+)%', line)
                if match:
                    performance_data['strategy_return'] = float(match.group(1))
            
            # Extract buy & hold performance
            elif "SPY Start Price:" in line:
                match = re.search(r'\$([0-9.]+)', line)
                if match:
                    performance_data['spy_start'] = float(match.group(1))
                    
            elif "SPY End Price:" in line:
                match = re.search(r'\$([0-9.]+)', line)
                if match:
                    performance_data['spy_end'] = float(match.group(1))
                    
            elif "Buy & Hold Return:" in line:
                match = re.search(r'([0-9.-]+)%', line)
                if match:
                    performance_data['buy_hold_return'] = float(match.group(1))
                    
            elif "Buy & Hold Final Value:" in line:
                match = re.search(r'\$([0-9,]+)', line)
                if match:
                    performance_data['buy_hold_final'] = match.group(1).replace(',', '')
            
            # Extract outperformance
            elif "OUTPERFORMED by" in line:
                match = re.search(r'([0-9.]+)%', line)
                if match:
                    performance_data['outperformance'] = float(match.group(1))
                    performance_data['outperformed'] = True
                    
            elif "UNDERPERFORMED by" in line:
                match = re.search(r'([0-9.]+)%', line)
                if match:
                    performance_data['outperformance'] = -float(match.group(1))
                    performance_data['outperformed'] = False
                    
            # Extract trading statistics
            elif "Trading Days:" in line:
                match = re.search(r'([0-9]+)', line)
                if match:
                    performance_data['trading_days'] = int(match.group(1))
                    
            elif "Annualized Strategy Return:" in line:
                match = re.search(r'([0-9.-]+)%', line)
                if match:
                    performance_data['annualized_strategy'] = float(match.group(1))
                    
            elif "Annualized Buy & Hold Return:" in line:
                match = re.search(r'([0-9.-]+)%', line)
                if match:
                    performance_data['annualized_buy_hold'] = float(match.group(1))
    
    return performance_data

def display_real_performance_comparison(performance_data):
    """
    Display the actual calculated performance comparison
    """
    print("\n" + "="*70)
    print("� ACTUAL PERFORMANCE COMPARISON (FROM ALGORITHM)")
    print("="*70)
    
    if not performance_data:
        print("❌ Could not extract performance data from logs")
        print("   The detailed comparison should be in the QuantConnect logs")
        return
    
    print(f"\n🎯 STRATEGY PERFORMANCE:")
    if 'strategy_final' in performance_data:
        print(f"   Final Portfolio Value: ${performance_data['strategy_final']:,}")
    if 'strategy_return' in performance_data:
        print(f"   Total Return: {performance_data['strategy_return']:.2f}%")
    
    print(f"\n📈 BUY & HOLD BENCHMARK:")
    if 'spy_start' in performance_data and 'spy_end' in performance_data:
        print(f"   SPY Start Price: ${performance_data['spy_start']:.2f}")
        print(f"   SPY End Price: ${performance_data['spy_end']:.2f}")
    if 'buy_hold_return' in performance_data:
        print(f"   Buy & Hold Return: {performance_data['buy_hold_return']:.2f}%")
    if 'buy_hold_final' in performance_data:
        print(f"   Buy & Hold Final Value: ${performance_data['buy_hold_final']:,}")
    
    print(f"\n⚡ COMPARISON RESULTS:")
    if 'outperformance' in performance_data:
        if performance_data.get('outperformed', False):
            print(f"   ✅ Strategy OUTPERFORMED by {performance_data['outperformance']:.2f}%")
        else:
            print(f"   ❌ Strategy UNDERPERFORMED by {abs(performance_data['outperformance']):.2f}%")
    
    if 'trading_days' in performance_data:
        print(f"\n� TRADING STATISTICS:")
        print(f"   Trading Days: {performance_data['trading_days']}")
        
        if 'annualized_strategy' in performance_data:
            print(f"   Annualized Strategy Return: {performance_data['annualized_strategy']:.2f}%")
        if 'annualized_buy_hold' in performance_data:
            print(f"   Annualized Buy & Hold Return: {performance_data['annualized_buy_hold']:.2f}%")
    
    print("="*70)

if __name__ == "__main__":
    success, url = run_backtest_with_capture()
    
    # Try to get the latest backtest logs to extract real performance data
    # For now, we'll need to access the QuantConnect logs directly
    # Let's provide guidance on how to get the real data
    
    print("\n" + "="*70)
    print("📊 REAL PERFORMANCE DATA EXTRACTION")
    print("="*70)
    print("\n⚠️  To get the ACTUAL buy & hold comparison:")
    print(f"   1. Open: {url if url else 'Latest backtest URL'}")
    print("   2. Go to 'Logs' tab")
    print("   3. Look for 'BACKTEST COMPLETE - PERFORMANCE COMPARISON'")
    print("   4. You'll see the REAL calculated values:")
    print("      • Exact SPY start/end prices")
    print("      • Precise buy & hold return %")
    print("      • Actual outperformance calculation")
    print("\n💡 This shows the REAL data from our price array calculation!")
    print("   No estimates - actual SPY price movement vs strategy performance")
    print("="*70)
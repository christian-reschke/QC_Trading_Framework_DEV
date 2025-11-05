using System;
using StrategyFramework.Metrics;

namespace StrategyFramework.Tests.Unit
{
    /// <summary>
    /// Unit tests for QuickResults metrics calculation
    /// </summary>
    public static class MetricsTests
    {
        public static void RunAllTests()
        {
            Console.WriteLine("=== RUNNING METRICS TESTS ===");
            
            TestBasicMetrics();
            TestWinLossCalculations();
            TestDrawdownCalculation();
            
            Console.WriteLine("=== ALL METRICS TESTS PASSED ===");
        }

        private static void TestBasicMetrics()
        {
            Console.WriteLine("Testing basic metrics calculation...");
            
            var results = new QuickResults(100000m);
            
            // Add some winning trades
            results.AddTrade("TEST", DateTime.Now.AddDays(-5), DateTime.Now.AddDays(-4), 
                           100m, 105m, 100, "Win1");
            results.AddTrade("TEST", DateTime.Now.AddDays(-3), DateTime.Now.AddDays(-2), 
                           100m, 110m, 100, "Win2");
            
            // Add a losing trade
            results.AddTrade("TEST", DateTime.Now.AddDays(-1), DateTime.Now, 
                           100m, 95m, 100, "Loss1");
            
            if (results.TotalTrades != 3)
                throw new Exception($"Expected 3 trades, got {results.TotalTrades}");
            
            if (results.WinRate != 2m/3m)
                throw new Exception($"Expected win rate 66.67%, got {results.WinRate:P}");
            
            // Total PnL should be +500 +1000 -500 = +1000
            var expectedReturn = 1000m / 100000m;
            if (Math.Abs(results.TotalReturn - expectedReturn) > 0.001m)
                throw new Exception($"Expected return {expectedReturn:P}, got {results.TotalReturn:P}");
            
            Console.WriteLine("Basic metrics calculation works correctly");
        }

        private static void TestWinLossCalculations()
        {
            Console.WriteLine("Testing win/loss calculations...");
            
            var results = new QuickResults(100000m);
            
            // Add trades with known PnL
            results.AddTrade("TEST", DateTime.Now.AddDays(-3), DateTime.Now.AddDays(-2), 
                           100m, 120m, 50, "BigWin");  // +1000
            results.AddTrade("TEST", DateTime.Now.AddDays(-2), DateTime.Now.AddDays(-1), 
                           100m, 110m, 50, "SmallWin"); // +500
            results.AddTrade("TEST", DateTime.Now.AddDays(-1), DateTime.Now, 
                           100m, 90m, 50, "Loss");      // -500
            
            // Average win should be (1000 + 500) / 2 = 750
            if (Math.Abs(results.AverageWin - 750m) > 0.01m)
                throw new Exception($"Expected average win 750, got {results.AverageWin}");
            
            // Average loss should be 500 (absolute value)
            if (Math.Abs(results.AverageLoss - 500m) > 0.01m)
                throw new Exception($"Expected average loss 500, got {results.AverageLoss}");
            
            // Profit factor should be 1500 / 500 = 3.0
            if (Math.Abs(results.ProfitFactor - 3.0m) > 0.01m)
                throw new Exception($"Expected profit factor 3.0, got {results.ProfitFactor}");
            
            Console.WriteLine("Win/loss calculations work correctly");
        }

        private static void TestDrawdownCalculation()
        {
            Console.WriteLine("Testing drawdown calculation...");
            
            var results = new QuickResults(100000m);
            
            // Create a scenario with drawdown
            results.AddTrade("TEST", DateTime.Now.AddDays(-4), DateTime.Now.AddDays(-3), 
                           100m, 110m, 100, "Win1");   // +1000, portfolio = 101000
            results.AddTrade("TEST", DateTime.Now.AddDays(-3), DateTime.Now.AddDays(-2), 
                           100m, 90m, 100, "Loss1");   // -1000, portfolio = 100000
            results.AddTrade("TEST", DateTime.Now.AddDays(-2), DateTime.Now.AddDays(-1), 
                           100m, 85m, 100, "Loss2");   // -1500, portfolio = 98500 (drawdown from 101000)
            results.AddTrade("TEST", DateTime.Now.AddDays(-1), DateTime.Now, 
                           100m, 105m, 100, "Win2");   // +500, portfolio = 99000
            
            // Max drawdown should be (101000 - 98500) / 101000 = approximately 2.48%
            var expectedDrawdown = 2500m / 101000m; // approximately 2.475%
            if (Math.Abs(results.MaxDrawdown - expectedDrawdown) > 0.01m)
                throw new Exception($"Expected drawdown {expectedDrawdown:P}, got {results.MaxDrawdown:P}");
            
            Console.WriteLine("Drawdown calculation works correctly");
        }
    }
}
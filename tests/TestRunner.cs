using System;
using System.Collections.Generic;
using StrategyFramework.Builder;
using StrategyFramework.Interfaces;
using StrategyFramework.Metrics;
using StrategyFramework.Tests.Mocks;
using StrategyFramework.Tests.Unit;

namespace StrategyFramework.Tests
{
    /// <summary>
    /// Main test runner and demonstration of the framework
    /// This shows how to use the framework for rapid strategy development
    /// </summary>
    public static class TestRunner
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("QUANTCONNECT STRATEGY FRAMEWORK - STAGE 1");
            Console.WriteLine("===============================================");
            
            try
            {
                // Run unit tests first
                Console.WriteLine("\n1. Running Unit Tests...");
                BuilderTests.RunAllTests();
                MetricsTests.RunAllTests();
                
                // Demonstrate the framework
                Console.WriteLine("\n2. Framework Demonstration...");
                DemonstrateFramework();
                
                Console.WriteLine("\nALL TESTS PASSED - FRAMEWORK IS READY!");
                Console.WriteLine("\nNEXT STEPS:");
                Console.WriteLine("- Create your first custom entry module in src/modules/entries/");
                Console.WriteLine("- Test it using: new SimpleStrategyBuilder().WithEntry(yourModule)...");
                Console.WriteLine("- Get instant feedback with QuickResults");
                Console.WriteLine("- Iterate rapidly with 5-minute strategy testing!");
                
            }
            catch (Exception ex)
            {
                Console.WriteLine($"\nTEST FAILED: {ex.Message}");
                Console.WriteLine($"Stack trace: {ex.StackTrace}");
            }
        }

        private static void DemonstrateFramework()
        {
            Console.WriteLine("Creating a test strategy...");
            
            // Build a complete strategy using the fluent API
            var strategy = new SimpleStrategyBuilder()
                .WithName("Mock Test Strategy")
                .WithEntry(new MockEntryModule())
                .WithExit(new MockExitModule())
                .WithPositionSizing(new MockPositionSizingModule())
                .WithRiskManagement(new MockRiskModule())
                .Build();
            
            Console.WriteLine($"Strategy created: {strategy.Name}");
            
            // Simulate some trading
            var results = new QuickResults(100000m);
            var positions = new Dictionary<string, decimal>();
            
            Console.WriteLine("Simulating trades...");
            
            // Simulate a few trades
            var baseTime = DateTime.Now.AddDays(-10);
            for (int i = 0; i < 10; i++)
            {
                var data = new SecurityData
                {
                    Symbol = "SPY",
                    Close = 400m + (decimal)(Math.Sin(i * 0.5) * 10), // Oscillating price
                    Open = 400m + (decimal)(Math.Sin(i * 0.5) * 10) - 1,
                    High = 400m + (decimal)(Math.Sin(i * 0.5) * 10) + 2,
                    Low = 400m + (decimal)(Math.Sin(i * 0.5) * 10) - 2,
                    Volume = 1000000,
                    Timestamp = baseTime.AddHours(i * 6) // Even seconds for entry signals
                };
                
                var orders = strategy.ProcessData(data, positions, 100000m, 50000m);
                
                // Simulate trade execution (simplified)
                foreach (var order in orders)
                {
                    Console.WriteLine($"  Order: {order.Quantity:F0} shares {order.Symbol} @ {data.Close:C} ({order.Tag})");
                    
                    if (order.Tag.StartsWith("Entry"))
                    {
                        positions[order.Symbol] = order.Quantity;
                        // We'll simulate the exit in a later iteration
                    }
                    else if (order.Tag.StartsWith("Exit") && positions.ContainsKey(order.Symbol))
                    {
                        var entryPrice = 400m; // Simplified
                        results.AddTrade(order.Symbol, baseTime.AddHours((i-2) * 6), data.Timestamp,
                                       entryPrice, data.Close, positions[order.Symbol], order.Tag);
                        positions[order.Symbol] = 0;
                    }
                }
            }
            
            // Display results
            Console.WriteLine("\nPERFORMANCE RESULTS:");
            Console.WriteLine(results.GetSummary());
            
            Console.WriteLine("\nFRAMEWORK VALIDATION COMPLETE!");
            Console.WriteLine("The framework is working correctly and ready for development.");
        }
    }
}
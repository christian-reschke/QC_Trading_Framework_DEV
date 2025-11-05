using System;
using System.Collections.Generic;
using StrategyFramework.Builder;
using StrategyFramework.Interfaces;
using StrategyFramework.Tests.Mocks;

namespace StrategyFramework.Tests.Unit
{
    /// <summary>
    /// Unit tests for SimpleStrategyBuilder
    /// Run these tests to ensure the framework is working correctly
    /// </summary>
    public static class BuilderTests
    {
        public static void RunAllTests()
        {
            Console.WriteLine("=== RUNNING BUILDER TESTS ===");
            
            TestBuilderValidation();
            TestBuilderFluentAPI();
            TestStrategyExecution();
            
            Console.WriteLine("=== ALL BUILDER TESTS PASSED ===");
        }

        private static void TestBuilderValidation()
        {
            Console.WriteLine("Testing builder validation...");
            
            var builder = new SimpleStrategyBuilder();
            
            // Test missing modules
            try
            {
                builder.Build();
                throw new Exception("Should have thrown exception for missing modules");
            }
            catch (InvalidOperationException ex)
            {
                if (!ex.Message.Contains("Entry module is required"))
                    throw new Exception($"Unexpected error message: {ex.Message}");
            }
            
            Console.WriteLine("Builder validation works correctly");
        }

        private static void TestBuilderFluentAPI()
        {
            Console.WriteLine("Testing fluent API...");
            
            var strategy = new SimpleStrategyBuilder()
                .WithEntry(new MockEntryModule())
                .WithExit(new MockExitModule())
                .WithPositionSizing(new MockPositionSizingModule())
                .WithRiskManagement(new MockRiskModule())
                .WithName("Test Strategy")
                .Build();
            
            if (strategy.Name != "Test Strategy")
                throw new Exception("Strategy name not set correctly");
            
            if (strategy.EntryModule.Name != "MockEntry")
                throw new Exception("Entry module not set correctly");
            
            Console.WriteLine("Fluent API works correctly");
        }

        private static void TestStrategyExecution()
        {
            Console.WriteLine("Testing strategy execution...");
            
            var strategy = new SimpleStrategyBuilder()
                .WithEntry(new MockEntryModule())
                .WithExit(new MockExitModule())
                .WithPositionSizing(new MockPositionSizingModule())
                .WithRiskManagement(new MockRiskModule())
                .Build();

            // Create test data
            var testData = new SecurityData
            {
                Symbol = "TEST",
                Close = 100m,
                Open = 99m,
                High = 101m,
                Low = 98m,
                Volume = 1000000,
                Timestamp = DateTime.Now // Even second should trigger entry
            };
            testData.Timestamp = testData.Timestamp.AddSeconds(-testData.Timestamp.Second % 2); // Make it even

            var currentPositions = new Dictionary<string, decimal>();
            var portfolioValue = 100000m;
            var availableCash = 50000m;

            // Test entry signal
            var orders = strategy.ProcessData(testData, currentPositions, portfolioValue, availableCash);
            
            if (orders.Count != 1)
                throw new Exception($"Expected 1 order, got {orders.Count}");
            
            if (orders[0].Symbol != "TEST")
                throw new Exception("Order symbol incorrect");
            
            if (orders[0].Quantity <= 0)
                throw new Exception("Order quantity should be positive for long entry");
            
            Console.WriteLine("Strategy execution works correctly");
        }
    }
}
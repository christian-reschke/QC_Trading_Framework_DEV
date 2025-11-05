using System;
using StrategyFramework.Builder;
using StrategyFramework.Modules.Entries;
using StrategyFramework.Tests.Mocks;

namespace StrategyFramework.Examples
{
    /// <summary>
    /// Example showing rapid strategy development and testing
    /// This is exactly what Stage 1 enables: 5-minute strategy ideas!
    /// </summary>
    public static class QuickStrategyExample
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("QUICK STRATEGY EXAMPLE - 5 MINUTE DEVELOPMENT");
            Console.WriteLine("=============================================");

            // STEP 1: Build a strategy in seconds using fluent API
            var strategy = new SimpleStrategyBuilder()
                .WithName("SMA Crossover Strategy")
                .WithEntry(new SimpleMovingAverageEntry(20))  // <-- NEW CUSTOM MODULE!
                .WithExit(new MockExitModule())               // <-- Use existing modules
                .WithPositionSizing(new MockPositionSizingModule())
                .WithRiskManagement(new MockRiskModule())
                .Build();

            Console.WriteLine($"Strategy built: {strategy.Name}");
            Console.WriteLine($"   Entry: {strategy.EntryModule.Name}");
            Console.WriteLine($"   Exit: {strategy.ExitModule.Name}");

            // STEP 2: Test it immediately
            Console.WriteLine("\nTesting strategy with sample data...");
            
            // This would be your QuantConnect backtest data in real use
            // For demo, we'll simulate some price data
            var testPrices = new decimal[] { 100, 101, 102, 101, 100, 99, 98, 99, 100, 101, 102, 103 };
            
            for (int i = 0; i < testPrices.Length; i++)
            {
                var data = new StrategyFramework.Interfaces.SecurityData
                {
                    Symbol = "SPY",
                    Close = testPrices[i],
                    Open = testPrices[i] - 0.5m,
                    High = testPrices[i] + 1,
                    Low = testPrices[i] - 1,
                    Volume = 1000000,
                    Timestamp = DateTime.Now.AddMinutes(i * 15)
                };

                var orders = strategy.ProcessData(data, new System.Collections.Generic.Dictionary<string, decimal>(), 
                                                100000m, 50000m);
                
                if (orders.Count > 0)
                {
                    Console.WriteLine($"   Day {i}: Price ${testPrices[i]} - {orders[0].Tag}");
                }
            }

            Console.WriteLine("\nDEVELOPMENT COMPLETE!");
            Console.WriteLine("Time taken: < 5 minutes to implement and test new strategy idea");
            Console.WriteLine("Ready to iterate: Modify parameters, test again instantly");
            Console.WriteLine("Ready for QuantConnect: Copy to QC algorithm and backtest with real data");
        }
    }
}
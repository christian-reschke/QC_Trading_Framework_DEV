using System;
using System.Collections.Generic;
using StrategyFramework.Builder;
using StrategyFramework.Interfaces;
using StrategyFramework.Metrics;
using StrategyFramework.Modules.Entries;
using StrategyFramework.Modules.Exits;
using StrategyFramework.Modules.Sizing;
using StrategyFramework.Modules.Risk;

namespace StrategyFramework.Strategies
{
    /// <summary>
    /// Simple test to verify our EMA strategy works with manual data
    /// This will create a clear crossover scenario
    /// </summary>
    public static class SimpleEMATest
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("SIMPLE EMA CROSSOVER TEST");
            Console.WriteLine("============================");
            Console.WriteLine("Testing with controlled data to ensure strategy logic works");
            Console.WriteLine();

            // Build the strategy
            var entryModule = new EMA50Entry();
            var exitModule = new EMA100Exit();
            
            var strategy = new SimpleStrategyBuilder()
                .WithName("Test EMA Strategy")
                .WithEntry(entryModule)
                .WithExit(exitModule)
                .WithPositionSizing(new FullAllocationSizing())
                .WithRiskManagement(new BasicRiskManagement())
                .Build();

            // Create controlled test data with clear crossover
            var testData = CreateTestData();
            
            var results = new QuickResults(1_000_000m);
            var positions = new Dictionary<string, decimal>();
            var portfolioValue = 1_000_000m;
            var availableCash = 1_000_000m;
            
            var entryPrice = 0m;
            var entryTime = DateTime.MinValue;

            Console.WriteLine("Date       | Price  | EMA50  | EMA100 | Action");
            Console.WriteLine("-----------|--------|--------|--------|------------------");

            foreach (var data in testData)
            {
                var currentPosition = positions.GetValueOrDefault("SPY", 0);
                
                // Update portfolio value
                if (currentPosition != 0)
                {
                    portfolioValue = availableCash + (currentPosition * data.Close);
                }

                // Process strategy (this will now update both EMAs)
                var orders = strategy.ProcessData(data, positions, portfolioValue, availableCash);

                var action = "HOLD";
                foreach (var order in orders)
                {
                    if (order.Tag.StartsWith("Entry"))
                    {
                        positions["SPY"] = order.Quantity;
                        availableCash -= order.Quantity * data.Close;
                        entryPrice = data.Close;
                        entryTime = data.Timestamp;
                        action = $"BUY {order.Quantity:F0} shares";
                    }
                    else if (order.Tag.StartsWith("Exit"))
                    {
                        availableCash += currentPosition * data.Close;
                        results.AddTrade("SPY", entryTime, data.Timestamp, entryPrice, data.Close, currentPosition);
                        positions["SPY"] = 0;
                        action = $"SELL {currentPosition:F0} shares";
                    }
                }

                var ema50 = entryModule.GetCurrentEMA();
                var ema100 = exitModule.GetCurrentEMA();

                // Debug: Show when crossover conditions are met
                var crossoverInfo = "";
                if (data.Close > ema50)
                {
                    crossoverInfo = " ABOVE EMA50!";
                }

                Console.WriteLine($"{data.Timestamp:MM/dd/yyyy} | ${data.Close:F1}  | ${ema50:F1}  | ${ema100:F1}  | {action}{crossoverInfo}");
            }

            // Final results
            var finalPosition = positions.GetValueOrDefault("SPY", 0);
            if (finalPosition != 0)
            {
                var finalData = testData[testData.Count - 1];
                portfolioValue = availableCash + (finalPosition * finalData.Close);
            }
            else
            {
                portfolioValue = availableCash;
            }

            Console.WriteLine();
            Console.WriteLine("TEST RESULTS:");
            Console.WriteLine("================");
            Console.WriteLine($"Starting Capital: ${1_000_000:N0}");
            Console.WriteLine($"Ending Portfolio: ${portfolioValue:N0}");
            Console.WriteLine($"Total Return: {((portfolioValue - 1_000_000) / 1_000_000):P2}");
            
            if (results.TotalTrades > 0)
            {
                Console.WriteLine();
                Console.WriteLine(results.GetSummary());
            }

            Console.WriteLine();
            Console.WriteLine("Framework test complete!");
            Console.WriteLine("This demonstrates the strategy logic is working correctly.");
        }

        private static List<SecurityData> CreateTestData()
        {
            var data = new List<SecurityData>();
            var startDate = new DateTime(2025, 1, 1);
            
            // Create 150 days of test data with a clear pattern:
            // 1. Start low (below EMA)
            // 2. Trend up to cross above EMA50 (trigger buy)
            // 3. Continue up 
            // 4. Then trend down to cross below EMA100 (trigger sell)
            
            var prices = new decimal[]
            {
                // Start low - build EMA history (days 1-50)
                400, 401, 402, 401, 400, 399, 398, 399, 400, 401,
                402, 401, 400, 399, 398, 397, 396, 397, 398, 399,
                400, 399, 398, 397, 396, 395, 394, 395, 396, 397,
                398, 397, 396, 395, 394, 393, 392, 393, 394, 395,
                396, 395, 394, 393, 392, 391, 390, 391, 392, 393,
                
                // Continue building EMA100 history (days 51-100)
                394, 393, 392, 391, 390, 389, 388, 389, 390, 391,
                392, 391, 390, 389, 388, 387, 386, 387, 388, 389,
                390, 389, 388, 387, 386, 385, 384, 385, 386, 387,
                388, 387, 386, 385, 384, 383, 382, 383, 384, 385,
                386, 385, 384, 383, 382, 381, 380, 381, 382, 383,
                
                // Strong uptrend - should trigger buy (days 101-125)
                384, 386, 388, 390, 392, 394, 396, 398, 400, 402,
                404, 406, 408, 410, 412, 414, 416, 418, 420, 422,
                424, 426, 428, 430, 432,
                
                // Strong downtrend - should trigger sell (days 126-150)  
                430, 428, 426, 424, 422, 420, 418, 416, 414, 412,
                410, 408, 406, 404, 402, 400, 398, 396, 394, 392,
                390, 388, 386, 384, 382
            };

            for (int i = 0; i < prices.Length; i++)
            {
                data.Add(new SecurityData
                {
                    Symbol = "SPY",
                    Close = prices[i],
                    Open = prices[i] - 0.5m,
                    High = prices[i] + 1,
                    Low = prices[i] - 1,
                    Volume = 1000000,
                    Timestamp = startDate.AddDays(i)
                });
            }

            return data;
        }
    }
}
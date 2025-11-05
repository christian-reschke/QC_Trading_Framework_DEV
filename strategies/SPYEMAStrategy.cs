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
    /// SPY EMA Crossover Strategy Test
    /// Entry: Price > EMA50
    /// Exit: Price < EMA100
    /// Allocation: 100% of portfolio
    /// Timeframe: Daily
    /// Period: Q3 2025
    /// Starting Capital: $1M
    /// </summary>
    public static class SPYEMAStrategy
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("SPY EMA CROSSOVER STRATEGY - Q3 2025 BACKTEST");
            Console.WriteLine("================================================");
            Console.WriteLine("Strategy Rules:");
            Console.WriteLine("   * BUY SPY when close > EMA50");
            Console.WriteLine("   * SELL SPY when close < EMA100");
            Console.WriteLine("   * Allocation: 100% of portfolio");
            Console.WriteLine("   * Timeframe: Daily");
            Console.WriteLine("   * Period: Q3 2025 (Jul-Sep)");
            Console.WriteLine("   * Starting Capital: $1,000,000");
            Console.WriteLine();

            // Build the strategy
            var entryModule = new EMA50Entry();
            var exitModule = new EMA100Exit();
            
            var strategy = new SimpleStrategyBuilder()
                .WithName("SPY EMA50/100 Crossover")
                .WithEntry(entryModule)
                .WithExit(exitModule)
                .WithPositionSizing(new FullAllocationSizing())
                .WithRiskManagement(new BasicRiskManagement())
                .Build();

            Console.WriteLine($"Strategy Built: {strategy.Name}");
            Console.WriteLine($"   Entry: {strategy.EntryModule.Name}");
            Console.WriteLine($"   Exit: {strategy.ExitModule.Name}");
            Console.WriteLine($"   Sizing: {strategy.PositionSizingModule.Name}");
            Console.WriteLine($"   Risk: {strategy.RiskModule.Name}");
            Console.WriteLine();

            // Setup simulation
            var startingCapital = 1_000_000m;
            var results = new QuickResults(startingCapital);
            var positions = new Dictionary<string, decimal>();
            var portfolioValue = startingCapital;
            var availableCash = startingCapital;
            
            // Track entry details for exit calculation
            var entryPrice = 0m;
            var entryTime = DateTime.MinValue;

            // Simulate Q3 2025 daily data (realistic SPY price action)
            var q3Data = GenerateQ3_2025_SPYData();

            Console.WriteLine("Running Backtest...");
            Console.WriteLine("Date        | Close   | EMA50   | EMA100  | Action");
            Console.WriteLine("------------|---------|---------|---------|------------------");

            var q3Start = new DateTime(2025, 7, 1);
            
            foreach (var data in q3Data)
            {
                var currentPosition = positions.GetValueOrDefault("SPY", 0);
                
                // Update portfolio value
                if (currentPosition != 0)
                {
                    portfolioValue = availableCash + (currentPosition * data.Close);
                }

                // Process strategy
                var orders = strategy.ProcessData(data, positions, portfolioValue, availableCash);

                var action = "HOLD";
                foreach (var order in orders)
                {
                    if (order.Tag.StartsWith("Entry"))
                    {
                        // Entry trade
                        positions["SPY"] = order.Quantity;
                        availableCash -= order.Quantity * data.Close;
                        entryPrice = data.Close;
                        entryTime = data.Timestamp;
                        action = $"BUY {order.Quantity:F0} shares";
                    }
                    else if (order.Tag.StartsWith("Exit"))
                    {
                        // Exit trade
                        availableCash += currentPosition * data.Close;
                        
                        // Record completed trade
                        results.AddTrade("SPY", entryTime, data.Timestamp, entryPrice, data.Close, currentPosition);
                        
                        positions["SPY"] = 0;
                        action = $"SELL {currentPosition:F0} shares";
                    }
                }

                // Only show Q3 data in output (but process all data for EMA calculation)
                if (data.Timestamp >= q3Start)
                {
                    // Get EMA values for display
                    var ema50 = entryModule.GetCurrentEMA();
                    var ema100 = exitModule.GetCurrentEMA();

                    Console.WriteLine($"{data.Timestamp:MM/dd/yyyy} | ${data.Close:F2}  | ${ema50:F2}  | ${ema100:F2}  | {action}");
                }
            }

            // Final portfolio value
            var finalPosition = positions.GetValueOrDefault("SPY", 0);
            if (finalPosition != 0)
            {
                var finalData = q3Data[q3Data.Count - 1];
                portfolioValue = availableCash + (finalPosition * finalData.Close);
            }
            else
            {
                portfolioValue = availableCash;
            }

            Console.WriteLine();
            Console.WriteLine("BACKTEST RESULTS:");
            Console.WriteLine("===================");
            Console.WriteLine($"Starting Capital: ${startingCapital:N0}");
            Console.WriteLine($"Ending Portfolio: ${portfolioValue:N0}");
            Console.WriteLine($"Total Return: {((portfolioValue - startingCapital) / startingCapital):P2}");
            Console.WriteLine();

            // Show detailed metrics if we had trades
            if (results.TotalTrades > 0)
            {
                Console.WriteLine(results.GetSummary());
            }
            else
            {
                Console.WriteLine("No completed trades during the period.");
                Console.WriteLine("(This could mean the strategy stayed in a position through Q3)");
            }

            Console.WriteLine();
            Console.WriteLine("STRATEGY TEST COMPLETE!");
            Console.WriteLine("Ready to implement in QuantConnect for real backtesting!");
        }

        private static List<SecurityData> GenerateQ3_2025_SPYData()
        {
            var data = new List<SecurityData>();
            
            // Start earlier to warm up the EMAs (need 100+ days for EMA100)
            var startDate = new DateTime(2025, 3, 1); // Start in March for warm-up
            var endDate = new DateTime(2025, 9, 30);  // Q3 end
            
            var basePrice = 450m; // Realistic SPY price for 2025
            var currentDate = startDate;
            var price = basePrice;
            var random = new Random(42); // Fixed seed for reproducible results

            // Create a trending market with some volatility to generate crossovers
            var trendPhase = 0; // 0 = down, 1 = up, 2 = sideways
            var daysSincePhaseChange = 0;

            while (currentDate <= endDate)
            {
                // Skip weekends
                if (currentDate.DayOfWeek != DayOfWeek.Saturday && currentDate.DayOfWeek != DayOfWeek.Sunday)
                {
                    daysSincePhaseChange++;
                    
                    // Change trend phases to create crossovers
                    if (daysSincePhaseChange > 30)
                    {
                        trendPhase = (trendPhase + 1) % 3;
                        daysSincePhaseChange = 0;
                    }
                    
                    // Generate price movement based on trend phase
                    double trendComponent = 0;
                    switch (trendPhase)
                    {
                        case 0: // Down trend
                            trendComponent = -0.5; // Stronger downtrend
                            break;
                        case 1: // Up trend  
                            trendComponent = 0.6; // Stronger uptrend
                            break;
                        case 2: // Sideways
                            trendComponent = 0.0;
                            break;
                    }
                    
                    // Add random daily movement
                    var randomComponent = (random.NextDouble() * 0.04 - 0.02); // +/- 2% random
                    var dailyReturn = (decimal)(trendComponent / 100 + randomComponent);
                    
                    price = price * (1 + dailyReturn);
                    
                    // Keep price in reasonable range
                    price = Math.Max(350m, Math.Min(550m, price));

                    data.Add(new SecurityData
                    {
                        Symbol = "SPY",
                        Close = Math.Round(price, 2),
                        Open = Math.Round(price * 0.999m, 2),
                        High = Math.Round(price * 1.005m, 2),
                        Low = Math.Round(price * 0.995m, 2),
                        Volume = 50_000_000 + random.Next(0, 20_000_000),
                        Timestamp = currentDate
                    });
                }
                currentDate = currentDate.AddDays(1);
            }

            return data;
        }

        private static decimal GetSimpleEMA(decimal currentPrice, int period)
        {
            // Simplified EMA calculation for display purposes
            // In real implementation, this would use the actual EMA calculation from modules
            return currentPrice * 0.98m; // Approximate for demo
        }
    }
}
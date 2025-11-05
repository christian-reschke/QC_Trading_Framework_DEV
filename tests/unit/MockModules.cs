using System;
using System.Collections.Generic;
using StrategyFramework.Interfaces;

namespace StrategyFramework.Tests.Mocks
{
    /// <summary>
    /// Mock entry module for testing - always signals entry on even timestamps
    /// </summary>
    public class MockEntryModule : IEntryModule
    {
        public string Name => "MockEntry";
        public Dictionary<string, object> Parameters { get; set; } = new Dictionary<string, object>();

        public bool ShouldEnter(SecurityData data)
        {
            // Simple test logic: enter on even seconds
            return data.Timestamp.Second % 2 == 0;
        }

        public decimal GetEntrySignal(SecurityData data)
        {
            // Return +1 for long, 0 for no signal
            return ShouldEnter(data) ? 1 : 0;
        }
    }

    /// <summary>
    /// Mock exit module for testing - exits after 2 minutes or 5% profit/loss
    /// </summary>
    public class MockExitModule : IExitModule
    {
        public string Name => "MockExit";
        public Dictionary<string, object> Parameters { get; set; } = new Dictionary<string, object>();

        public bool ShouldExit(SecurityData data, decimal currentPosition, decimal entryPrice, DateTime entryTime)
        {
            // Exit after 2 minutes
            if ((data.Timestamp - entryTime).TotalMinutes >= 2)
                return true;
            
            // Exit on 5% profit or loss
            var pnlPercent = Math.Abs((data.Close - entryPrice) / entryPrice);
            return pnlPercent >= 0.05m;
        }
    }

    /// <summary>
    /// Mock position sizing module for testing - always uses $10,000 per trade
    /// </summary>
    public class MockPositionSizingModule : IPositionSizingModule
    {
        public string Name => "MockSizing";
        public Dictionary<string, object> Parameters { get; set; } = new Dictionary<string, object>();

        public decimal CalculatePositionSize(SecurityData data, decimal portfolioValue, decimal availableCash, bool isLong)
        {
            // Fixed $10,000 position size
            var dollarAmount = 10000m;
            var shares = dollarAmount / data.Close;
            return isLong ? shares : -shares;
        }
    }

    /// <summary>
    /// Mock risk module for testing - blocks trades if less than $5,000 available
    /// </summary>
    public class MockRiskModule : IRiskModule
    {
        public string Name => "MockRisk";
        public Dictionary<string, object> Parameters { get; set; } = new Dictionary<string, object>();

        public bool ValidateTrade(SecurityData data, decimal proposedQuantity, decimal currentPosition, 
                                decimal portfolioValue, decimal availableCash)
        {
            // Block trades if less than $5,000 available
            if (availableCash < 5000m)
                return false;
            
            // Block if proposed trade would use more than 50% of portfolio
            var tradeValue = Math.Abs(proposedQuantity * data.Close);
            return tradeValue <= portfolioValue * 0.5m;
        }
    }
}
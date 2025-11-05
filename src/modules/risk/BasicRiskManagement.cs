using System;
using System.Collections.Generic;
using StrategyFramework.Interfaces;

namespace StrategyFramework.Modules.Risk
{
    /// <summary>
    /// Basic risk management - prevents over-leverage and validates basic trade constraints
    /// </summary>
    public class BasicRiskManagement : IRiskModule
    {
        public string Name => "BasicRisk";
        public Dictionary<string, object> Parameters { get; set; }

        public BasicRiskManagement()
        {
            Parameters = new Dictionary<string, object>
            {
                { "MaxLeverage", 1.0m }, // No leverage
                { "MinCashBuffer", 1000m } // Keep $1000 buffer
            };
        }

        public bool ValidateTrade(SecurityData data, decimal proposedQuantity, decimal currentPosition, 
                                decimal portfolioValue, decimal availableCash)
        {
            // Always allow exit trades
            if (currentPosition != 0 && Math.Sign(proposedQuantity) != Math.Sign(currentPosition))
                return true;
            
            // For entry trades, check basic constraints
            var tradeValue = Math.Abs(proposedQuantity * data.Close);
            
            // Don't allow trades that exceed portfolio value (no leverage)
            if (tradeValue > portfolioValue)
                return false;
            
            // Allow trades up to 99% of available cash (more realistic for 100% allocation strategy)
            if (tradeValue > availableCash * 0.99m)
                return false;
            
            return true;
        }
    }
}
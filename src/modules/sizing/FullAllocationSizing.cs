using System;
using System.Collections.Generic;
using StrategyFramework.Interfaces;

namespace StrategyFramework.Modules.Sizing
{
    /// <summary>
    /// Full allocation position sizing - uses 100% of net liquidation value
    /// </summary>
    public class FullAllocationSizing : IPositionSizingModule
    {
        public string Name => "FullAllocation_100%";
        public Dictionary<string, object> Parameters { get; set; }

        public FullAllocationSizing()
        {
            Parameters = new Dictionary<string, object>
            {
                { "AllocationPercent", 1.0m } // 100%
            };
        }

        public decimal CalculatePositionSize(SecurityData data, decimal portfolioValue, decimal availableCash, bool isLong)
        {
            // Use 99% of available cash to allow for rounding and fees
            var dollarAmount = availableCash * 0.99m;
            var shares = Math.Floor(dollarAmount / data.Close);
            
            return isLong ? shares : -shares;
        }
    }
}
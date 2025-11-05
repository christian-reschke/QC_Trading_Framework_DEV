using System;
using System.Collections.Generic;

namespace StrategyFramework.Interfaces
{
    /// <summary>
    /// Interface for risk management modules that can override or block trades
    /// </summary>
    public interface IRiskModule
    {
        /// <summary>
        /// Name of the risk management module for identification
        /// </summary>
        string Name { get; }

        /// <summary>
        /// Validates if a proposed trade should be allowed
        /// </summary>
        /// <param name="data">Current security price data</param>
        /// <param name="proposedQuantity">Proposed trade quantity</param>
        /// <param name="currentPosition">Current position in the security</param>
        /// <param name="portfolioValue">Current total portfolio value</param>
        /// <param name="availableCash">Available cash for trading</param>
        /// <returns>True if trade is allowed, false if blocked by risk management</returns>
        bool ValidateTrade(SecurityData data, decimal proposedQuantity, decimal currentPosition, 
                          decimal portfolioValue, decimal availableCash);

        /// <summary>
        /// Configuration parameters for this risk management module
        /// </summary>
        Dictionary<string, object> Parameters { get; set; }
    }
}
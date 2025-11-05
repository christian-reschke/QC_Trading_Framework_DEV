using System;
using System.Collections.Generic;

namespace StrategyFramework.Interfaces
{
    /// <summary>
    /// Interface for position sizing modules that determine how much to buy/sell
    /// </summary>
    public interface IPositionSizingModule
    {
        /// <summary>
        /// Name of the position sizing module for identification
        /// </summary>
        string Name { get; }

        /// <summary>
        /// Calculates the position size for a new trade
        /// </summary>
        /// <param name="data">Current security price data</param>
        /// <param name="portfolioValue">Current total portfolio value</param>
        /// <param name="availableCash">Available cash for trading</param>
        /// <param name="isLong">True for long position, false for short</param>
        /// <returns>Number of shares/units to trade (positive for long, negative for short)</returns>
        decimal CalculatePositionSize(SecurityData data, decimal portfolioValue, decimal availableCash, bool isLong);

        /// <summary>
        /// Configuration parameters for this position sizing module
        /// </summary>
        Dictionary<string, object> Parameters { get; set; }
    }
}
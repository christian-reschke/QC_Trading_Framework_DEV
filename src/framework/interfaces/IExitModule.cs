using System;
using System.Collections.Generic;

namespace StrategyFramework.Interfaces
{
    /// <summary>
    /// Interface for exit signal modules that determine when to close positions
    /// </summary>
    public interface IExitModule
    {
        /// <summary>
        /// Name of the exit module for identification
        /// </summary>
        string Name { get; }

        /// <summary>
        /// Determines if a position should be exited
        /// </summary>
        /// <param name="data">Current security price data</param>
        /// <param name="currentPosition">Current position quantity (positive for long, negative for short)</param>
        /// <param name="entryPrice">Price at which the position was entered</param>
        /// <param name="entryTime">Time when the position was entered</param>
        /// <returns>True if position should be exited, false otherwise</returns>
        bool ShouldExit(SecurityData data, decimal currentPosition, decimal entryPrice, DateTime entryTime);

        /// <summary>
        /// Configuration parameters for this exit module
        /// </summary>
        Dictionary<string, object> Parameters { get; set; }
    }
}
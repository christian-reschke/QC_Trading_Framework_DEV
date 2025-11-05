using System;
using System.Collections.Generic;

namespace StrategyFramework.Interfaces
{
    /// <summary>
    /// Interface for entry signal modules
    /// </summary>
    public interface IEntryModule
    {
        /// <summary>
        /// Name of the entry module
        /// </summary>
        string Name { get; }
        
        /// <summary>
        /// Determines if we should enter a position
        /// </summary>
        /// <param name="data">Security data for analysis</param>
        /// <returns>True if should enter, false otherwise</returns>
        bool ShouldEnter(SecurityData data);
        
        /// <summary>
        /// Gets the entry signal strength and direction
        /// </summary>
        /// <param name="data">Security data for analysis</param>
        /// <returns>Signal strength (positive for long, negative for short, 0 for no signal)</returns>
        decimal GetEntrySignal(SecurityData data);
        
        /// <summary>
        /// Parameters used by this module
        /// </summary>
        Dictionary<string, object> Parameters { get; }
    }
    
    /// <summary>
    /// Simple data structure for security information
    /// </summary>
    public class SecurityData
    {
        public string Symbol { get; set; }
        public decimal Price { get; set; }
        public decimal Close { get; set; }
        public decimal Open { get; set; }
        public decimal High { get; set; }
        public decimal Low { get; set; }
        public decimal Volume { get; set; }
        public DateTime Timestamp { get; set; }
        
        // For backwards compatibility
        public decimal ClosePrice => Close;
        
        // Additional technical indicators would be added here
        // For now, keep it simple
    }
}
using System;
using System.Collections.Generic;
using StrategyFramework.Interfaces;

namespace StrategyFramework.Modules.Entries
{
    /// <summary>
    /// Simple Moving Average entry module - enters when price crosses above SMA
    /// This demonstrates how easy it is to create new modules!
    /// </summary>
    public class SimpleMovingAverageEntry : IEntryModule
    {
        public string Name => "SMA_Entry";
        public Dictionary<string, object> Parameters { get; set; }

        private readonly int _period;
        private readonly List<decimal> _priceHistory = new List<decimal>();

        public SimpleMovingAverageEntry(int period = 20)
        {
            _period = period;
            Parameters = new Dictionary<string, object>
            {
                { "Period", period }
            };
        }

        public bool ShouldEnter(SecurityData data)
        {
            return GetEntrySignal(data) > 0;
        }

        public decimal GetEntrySignal(SecurityData data)
        {
            // Track price history
            _priceHistory.Add(data.Close);
            if (_priceHistory.Count > _period + 1)
                _priceHistory.RemoveAt(0);

            // Need enough data for calculation
            if (_priceHistory.Count < _period + 1)
                return 0;

            // Calculate moving average
            var sma = 0m;
            for (int i = _priceHistory.Count - _period - 1; i < _priceHistory.Count - 1; i++)
            {
                sma += _priceHistory[i];
            }
            sma /= _period;

            // Entry signal: current price > SMA and previous price <= SMA (crossover)
            var currentPrice = data.Close;
            var previousPrice = _priceHistory[_priceHistory.Count - 2];

            if (currentPrice > sma && previousPrice <= sma)
                return 1; // Long signal

            return 0; // No signal
        }
    }
}
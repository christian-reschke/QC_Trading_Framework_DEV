using System;
using System.Collections.Generic;
using System.Linq;
using StrategyFramework.Interfaces;

namespace StrategyFramework.Modules.Entries
{
    /// <summary>
    /// EMA50 entry module - enters when price closes above EMA50
    /// </summary>
    public class EMA50Entry : IEntryModule
    {
        public string Name => "EMA50_Entry";
        public Dictionary<string, object> Parameters { get; set; }

        private readonly int _period = 50;
        private readonly List<decimal> _priceHistory = new List<decimal>();
        private decimal _currentEMA = 0;
        private bool _isInitialized = false;
        private DateTime _lastUpdateTime = DateTime.MinValue;

        public EMA50Entry()
        {
            Parameters = new Dictionary<string, object>
            {
                { "Period", _period }
            };
        }

        public bool ShouldEnter(SecurityData data)
        {
            return GetEntrySignal(data) > 0;
        }

        public decimal GetEntrySignal(SecurityData data)
        {
            // Only update EMA once per timestamp to avoid duplicates
            if (_lastUpdateTime != data.Timestamp)
            {
                _priceHistory.Add(data.Close);
                _currentEMA = CalculateEMA(data.Close);
                _lastUpdateTime = data.Timestamp;
            }
            
            // Need enough data
            if (!_isInitialized) return 0;
            
            // Entry signal: current price > EMA50
            if (data.Close > _currentEMA)
                return 1; // Long signal
            
            return 0; // No signal
        }

        private decimal CalculateEMA(decimal currentPrice)
        {
            if (_priceHistory.Count < _period)
            {
                // Use current price as EMA until we have enough data
                if (_priceHistory.Count == 1)
                {
                    _currentEMA = currentPrice;
                    _isInitialized = true;
                }
                return _currentEMA;
            }
            
            if (!_isInitialized)
            {
                // Initialize with SMA of first 50 prices
                _currentEMA = _priceHistory.Take(_period).Average();
                _isInitialized = true;
                return _currentEMA;
            }
            
            // EMA formula: EMA = (Close - EMA_prev) * multiplier + EMA_prev
            decimal multiplier = 2m / (_period + 1);
            _currentEMA = (currentPrice - _currentEMA) * multiplier + _currentEMA;
            
            return _currentEMA;
        }

        public decimal GetCurrentEMA() => _currentEMA;
    }
}
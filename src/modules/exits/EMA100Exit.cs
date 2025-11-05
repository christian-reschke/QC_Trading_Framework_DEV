using System;
using System.Collections.Generic;
using System.Linq;
using StrategyFramework.Interfaces;

namespace StrategyFramework.Modules.Exits
{
    /// <summary>
    /// EMA100 exit module - exits when price drops below EMA100
    /// </summary>
    public class EMA100Exit : IExitModule
    {
        public string Name => "EMA100_Exit";
        public Dictionary<string, object> Parameters { get; set; }

        private readonly int _period = 100;
        private readonly List<decimal> _priceHistory = new List<decimal>();
        private decimal _currentEMA = 0;
        private bool _isInitialized = false;
        private DateTime _lastUpdateTime = DateTime.MinValue;

        public EMA100Exit()
        {
            Parameters = new Dictionary<string, object>
            {
                { "Period", _period }
            };
        }

        public bool ShouldExit(SecurityData data, decimal currentPosition, decimal entryPrice, DateTime entryTime)
        {
            // Only update EMA once per timestamp to avoid duplicates
            if (_lastUpdateTime != data.Timestamp)
            {
                _priceHistory.Add(data.Close);
                _currentEMA = CalculateEMA(data.Close);
                _lastUpdateTime = data.Timestamp;
            }
            
            // Only exit if we have a long position
            if (currentPosition <= 0) return false;
            
            // Always allow exit check once initialized
            if (!_isInitialized) return false;
            
            // Exit signal: current price < EMA100
            return data.Close < _currentEMA;
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
                // Initialize with SMA of first 100 prices
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
using System;
using System.Collections.Generic;
using StrategyFramework.Interfaces;

namespace StrategyFramework.Builder
{
    /// <summary>
    /// Builder class for creating modular trading strategies with fluent API
    /// Usage: new SimpleStrategyBuilder().WithEntry(entryModule).WithExit(exitModule)...Build()
    /// </summary>
    public class SimpleStrategyBuilder
    {
        private IEntryModule _entryModule;
        private IExitModule _exitModule;
        private IPositionSizingModule _positionSizingModule;
        private IRiskModule _riskModule;
        private string _strategyName;

        /// <summary>
        /// Sets the entry module for the strategy
        /// </summary>
        public SimpleStrategyBuilder WithEntry(IEntryModule entryModule)
        {
            _entryModule = entryModule ?? throw new ArgumentNullException(nameof(entryModule));
            return this;
        }

        /// <summary>
        /// Sets the exit module for the strategy
        /// </summary>
        public SimpleStrategyBuilder WithExit(IExitModule exitModule)
        {
            _exitModule = exitModule ?? throw new ArgumentNullException(nameof(exitModule));
            return this;
        }

        /// <summary>
        /// Sets the position sizing module for the strategy
        /// </summary>
        public SimpleStrategyBuilder WithPositionSizing(IPositionSizingModule positionSizingModule)
        {
            _positionSizingModule = positionSizingModule ?? throw new ArgumentNullException(nameof(positionSizingModule));
            return this;
        }

        /// <summary>
        /// Sets the risk management module for the strategy
        /// </summary>
        public SimpleStrategyBuilder WithRiskManagement(IRiskModule riskModule)
        {
            _riskModule = riskModule ?? throw new ArgumentNullException(nameof(riskModule));
            return this;
        }

        /// <summary>
        /// Sets the strategy name for identification
        /// </summary>
        public SimpleStrategyBuilder WithName(string name)
        {
            _strategyName = name ?? throw new ArgumentNullException(nameof(name));
            return this;
        }

        /// <summary>
        /// Builds and validates the complete strategy
        /// </summary>
        /// <returns>A configured ISimpleStrategy instance</returns>
        /// <exception cref="InvalidOperationException">Thrown when required modules are missing</exception>
        public ISimpleStrategy Build()
        {
            ValidateConfiguration();
            
            return new SimpleStrategy(
                _strategyName ?? GenerateDefaultName(),
                _entryModule,
                _exitModule,
                _positionSizingModule,
                _riskModule
            );
        }

        private void ValidateConfiguration()
        {
            if (_entryModule == null)
                throw new InvalidOperationException("Entry module is required. Use WithEntry() to set it.");
            
            if (_exitModule == null)
                throw new InvalidOperationException("Exit module is required. Use WithExit() to set it.");
            
            if (_positionSizingModule == null)
                throw new InvalidOperationException("Position sizing module is required. Use WithPositionSizing() to set it.");
            
            if (_riskModule == null)
                throw new InvalidOperationException("Risk management module is required. Use WithRiskManagement() to set it.");
        }

        private string GenerateDefaultName()
        {
            return $"{_entryModule.Name}_{_exitModule.Name}_{_positionSizingModule.Name}_{_riskModule.Name}";
        }
    }

    /// <summary>
    /// Default implementation of ISimpleStrategy that coordinates all modules
    /// </summary>
    internal class SimpleStrategy : ISimpleStrategy
    {
        public string Name { get; }
        public IEntryModule EntryModule { get; }
        public IExitModule ExitModule { get; }
        public IPositionSizingModule PositionSizingModule { get; }
        public IRiskModule RiskModule { get; }

        // Track entry prices and times for exit decisions
        private readonly Dictionary<string, decimal> _entryPrices = new Dictionary<string, decimal>();
        private readonly Dictionary<string, DateTime> _entryTimes = new Dictionary<string, DateTime>();

        internal SimpleStrategy(string name, IEntryModule entryModule, IExitModule exitModule, 
                              IPositionSizingModule positionSizingModule, IRiskModule riskModule)
        {
            Name = name;
            EntryModule = entryModule;
            ExitModule = exitModule;
            PositionSizingModule = positionSizingModule;
            RiskModule = riskModule;
        }

        public List<TradeOrder> ProcessData(SecurityData data, Dictionary<string, decimal> currentPositions, 
                                          decimal portfolioValue, decimal availableCash)
        {
            var orders = new List<TradeOrder>();
            var symbol = data.Symbol;
            var currentPosition = currentPositions.GetValueOrDefault(symbol, 0);

            try
            {
                // Always check entry signal (this updates EMA50)
                var entrySignal = EntryModule.GetEntrySignal(data);
                var shouldEnter = EntryModule.ShouldEnter(data);
                
                // Always check exit signal (this updates EMA100)
                // Use dummy values if no position to ensure EMA gets updated
                ExitModule.ShouldExit(data, Math.Max(currentPosition, 1), data.Close, DateTime.UtcNow);
                
                // Check for exit signals first (if we have a position)
                if (currentPosition != 0)
                {
                    var entryPrice = _entryPrices.GetValueOrDefault(symbol, data.Close);
                    var entryTime = _entryTimes.GetValueOrDefault(symbol, DateTime.UtcNow);

                    if (ExitModule.ShouldExit(data, currentPosition, entryPrice, entryTime))
                    {
                        // Exit the entire position
                        var exitQuantity = -currentPosition; // Opposite sign to close
                        
                        if (RiskModule.ValidateTrade(data, exitQuantity, currentPosition, portfolioValue, availableCash))
                        {
                            orders.Add(new TradeOrder
                            {
                                Symbol = symbol,
                                Quantity = exitQuantity,
                                OrderType = "Market",
                                Tag = $"Exit-{ExitModule.Name}",
                                Timestamp = DateTime.UtcNow
                            });

                            // Clear tracking data after exit
                            _entryPrices.Remove(symbol);
                            _entryTimes.Remove(symbol);
                        }
                    }
                }
                // Check for entry signals (if we don't have a position or after exit)
                else if (shouldEnter)
                {
                    var isLong = entrySignal > 0;
                    
                    var positionSize = PositionSizingModule.CalculatePositionSize(data, portfolioValue, availableCash, isLong);
                    
                    // Apply entry signal direction to position size
                    var adjustedQuantity = Math.Abs(positionSize) * Math.Sign(entrySignal);
                    
                    if (adjustedQuantity != 0 && RiskModule.ValidateTrade(data, adjustedQuantity, currentPosition, portfolioValue, availableCash))
                    {
                        orders.Add(new TradeOrder
                        {
                            Symbol = symbol,
                            Quantity = adjustedQuantity,
                            OrderType = "Market",
                            Tag = $"Entry-{EntryModule.Name}",
                            Timestamp = DateTime.UtcNow
                        });

                        // Track entry for future exit decisions
                        _entryPrices[symbol] = data.Close;
                        _entryTimes[symbol] = DateTime.UtcNow;
                    }
                }
            }
            catch (Exception ex)
            {
                // Log error but don't crash the strategy
                // In QuantConnect, you'd use this.Error($"Strategy {Name} error: {ex.Message}");
                // For now, we'll just skip this data point
            }

            return orders;
        }
    }
}
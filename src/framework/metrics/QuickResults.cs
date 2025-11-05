using System;
using System.Collections.Generic;
using System.Linq;

namespace StrategyFramework.Metrics
{
    /// <summary>
    /// Lightweight performance metrics calculator for rapid strategy feedback
    /// Focuses on essential metrics only for quick decision making
    /// </summary>
    public class QuickResults
    {
        public decimal TotalReturn { get; private set; }
        public decimal SharpeRatio { get; private set; }
        public decimal MaxDrawdown { get; private set; }
        public decimal WinRate { get; private set; }
        public int TotalTrades { get; private set; }
        public decimal ProfitFactor { get; private set; }
        
        // Additional useful metrics
        public decimal AverageWin { get; private set; }
        public decimal AverageLoss { get; private set; }
        public TimeSpan BacktestPeriod { get; private set; }
        public decimal AnnualizedReturn { get; private set; }

        private readonly List<TradeResult> _trades;
        private readonly List<decimal> _dailyReturns;
        private decimal _startingCapital;

        public QuickResults(decimal startingCapital = 100000m)
        {
            _startingCapital = startingCapital;
            _trades = new List<TradeResult>();
            _dailyReturns = new List<decimal>();
        }

        /// <summary>
        /// Add a completed trade to the performance calculation
        /// </summary>
        public void AddTrade(string symbol, DateTime entryTime, DateTime exitTime, 
                           decimal entryPrice, decimal exitPrice, decimal quantity, string tag = "")
        {
            var pnl = (exitPrice - entryPrice) * quantity;
            var pnlPercent = pnl / (entryPrice * Math.Abs(quantity));
            
            _trades.Add(new TradeResult
            {
                Symbol = symbol,
                EntryTime = entryTime,
                ExitTime = exitTime,
                EntryPrice = entryPrice,
                ExitPrice = exitPrice,
                Quantity = quantity,
                PnL = pnl,
                PnLPercent = pnlPercent,
                IsWin = pnl > 0,
                Tag = tag
            });

            RecalculateMetrics();
        }

        /// <summary>
        /// Add daily portfolio returns for Sharpe ratio calculation
        /// </summary>
        public void AddDailyReturn(decimal dailyReturn)
        {
            _dailyReturns.Add(dailyReturn);
            RecalculateMetrics();
        }

        /// <summary>
        /// Get a formatted summary of key metrics
        /// </summary>
        public string GetSummary()
        {
            return $@"
=== QUICK RESULTS SUMMARY ===
Total Return: {TotalReturn:P2}
Annualized Return: {AnnualizedReturn:P2}
Sharpe Ratio: {SharpeRatio:F2}
Max Drawdown: {MaxDrawdown:P2}
Win Rate: {WinRate:P1}
Total Trades: {TotalTrades}
Profit Factor: {ProfitFactor:F2}
Average Win: {AverageWin:C}
Average Loss: {AverageLoss:C}
Backtest Period: {BacktestPeriod.TotalDays:F0} days
===========================";
        }

        /// <summary>
        /// Get individual trade details for analysis
        /// </summary>
        public List<TradeResult> GetTrades() => _trades.ToList();

        private void RecalculateMetrics()
        {
            if (_trades.Count == 0)
            {
                ResetMetrics();
                return;
            }

            TotalTrades = _trades.Count;
            
            // Calculate total return
            var totalPnL = _trades.Sum(t => t.PnL);
            TotalReturn = totalPnL / _startingCapital;

            // Calculate win rate
            var wins = _trades.Count(t => t.IsWin);
            WinRate = wins / (decimal)TotalTrades;

            // Calculate average win/loss
            var winningTrades = _trades.Where(t => t.IsWin).ToList();
            var losingTrades = _trades.Where(t => !t.IsWin).ToList();
            
            AverageWin = winningTrades.Any() ? winningTrades.Average(t => t.PnL) : 0;
            AverageLoss = losingTrades.Any() ? losingTrades.Average(t => Math.Abs(t.PnL)) : 0;

            // Calculate profit factor
            var grossProfit = winningTrades.Sum(t => t.PnL);
            var grossLoss = Math.Abs(losingTrades.Sum(t => t.PnL));
            ProfitFactor = grossLoss > 0 ? grossProfit / grossLoss : 0;

            // Calculate backtest period
            if (_trades.Count > 1)
            {
                BacktestPeriod = _trades.Max(t => t.ExitTime) - _trades.Min(t => t.EntryTime);
                
                // Calculate annualized return
                if (BacktestPeriod.TotalDays > 0)
                {
                    var annualMultiplier = 365.25 / BacktestPeriod.TotalDays;
                    AnnualizedReturn = (decimal)Math.Pow((double)(1 + TotalReturn), annualMultiplier) - 1;
                }
            }

            // Calculate Sharpe ratio
            if (_dailyReturns.Count > 1)
            {
                var avgDailyReturn = _dailyReturns.Average();
                var dailyStdDev = CalculateStandardDeviation(_dailyReturns);
                SharpeRatio = dailyStdDev > 0 ? (avgDailyReturn * (decimal)Math.Sqrt(252)) / (dailyStdDev * (decimal)Math.Sqrt(252)) : 0;
            }

            // Calculate max drawdown (simplified version using trade PnL)
            MaxDrawdown = CalculateMaxDrawdown();
        }

        private decimal CalculateMaxDrawdown()
        {
            if (_trades.Count == 0) return 0;

            var runningCapital = _startingCapital;
            var peak = _startingCapital;
            var maxDrawdown = 0m;

            foreach (var trade in _trades.OrderBy(t => t.ExitTime))
            {
                runningCapital += trade.PnL;
                
                if (runningCapital > peak)
                    peak = runningCapital;
                
                var drawdown = (peak - runningCapital) / peak;
                if (drawdown > maxDrawdown)
                    maxDrawdown = drawdown;
            }

            return maxDrawdown;
        }

        private decimal CalculateStandardDeviation(List<decimal> values)
        {
            if (values.Count < 2) return 0;
            
            var avg = values.Average();
            var sumSquaredDiffs = values.Sum(v => (v - avg) * (v - avg));
            return (decimal)Math.Sqrt((double)(sumSquaredDiffs / (values.Count - 1)));
        }

        private void ResetMetrics()
        {
            TotalReturn = 0;
            SharpeRatio = 0;
            MaxDrawdown = 0;
            WinRate = 0;
            TotalTrades = 0;
            ProfitFactor = 0;
            AverageWin = 0;
            AverageLoss = 0;
            BacktestPeriod = TimeSpan.Zero;
            AnnualizedReturn = 0;
        }
    }

    /// <summary>
    /// Represents a single completed trade with all relevant metrics
    /// </summary>
    public class TradeResult
    {
        public string Symbol { get; set; }
        public DateTime EntryTime { get; set; }
        public DateTime ExitTime { get; set; }
        public decimal EntryPrice { get; set; }
        public decimal ExitPrice { get; set; }
        public decimal Quantity { get; set; }
        public decimal PnL { get; set; }
        public decimal PnLPercent { get; set; }
        public bool IsWin { get; set; }
        public string Tag { get; set; }
        public TimeSpan Duration => ExitTime - EntryTime;
    }
}
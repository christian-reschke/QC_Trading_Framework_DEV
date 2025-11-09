"""
Backtest Logging Service for QuantConnect Object Store

Simple, robust logging that captures comprehensive backtest data
and saves it to QC's object store for external analysis.
"""

import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

class BacktestLogger:
    """
    Handles logging of backtest data to QuantConnect's object store.
    
    Features:
    - Trade logging (entries/exits with full details)
    - Daily performance tracking
    - Indicator values over time
    - Final portfolio state
    - Robust JSON serialization
    - Error handling that won't break backtests
    """
    
    def __init__(self, algorithm, run_id: str = "", enabled: bool = True):
        """
        Initialize the logger.
        
        Args:
            algorithm: QCAlgorithm instance
            run_id: Unique identifier for this backtest run (auto-generated if empty)
            enabled: Whether logging is enabled
        """
        self.algorithm = algorithm
        self.enabled = enabled
        self.run_id = run_id if run_id else str(uuid.uuid4())
        
        # Data storage
        self.trades: List[Dict[str, Any]] = []
        self.daily_performance: List[Dict[str, Any]] = []
        self.indicator_data: List[Dict[str, Any]] = []
        self.entry_conditions: List[Dict[str, Any]] = []
        
        # Metadata
        self.start_time = algorithm.time
        self.strategy_name = ""
        self.symbol = ""
        self.timeframe_minutes = 0
        
        # Trade tracking
        self.current_trade_id = 0
        
        if self.enabled:
            algorithm.Log(f"BacktestLogger initialized - Run ID: {self.run_id}")
    
    def set_metadata(self, strategy_name: str, symbol: str, timeframe_minutes: int):
        """Set strategy metadata"""
        self.strategy_name = strategy_name
        self.symbol = symbol
        self.timeframe_minutes = timeframe_minutes
    
    def log_trade_entry(self, symbol: str, quantity: int, price: float, 
                       entry_conditions: Dict[str, Any] = None):
        """
        Log a trade entry.
        
        Args:
            symbol: Trading symbol
            quantity: Number of shares
            price: Entry price
            entry_conditions: Dict of entry condition values
        """
        if not self.enabled:
            return
        
        try:
            self.current_trade_id += 1
            
            trade_entry = {
                "trade_id": self.current_trade_id,
                "type": "entry",
                "timestamp": self.algorithm.time.isoformat(),
                "symbol": str(symbol),
                "quantity": int(quantity),
                "price": float(price),
                "value": float(quantity * price),
                "portfolio_value": float(self.algorithm.portfolio.total_portfolio_value),
                "cash": float(self.algorithm.portfolio.cash),
                "entry_conditions": self._sanitize(entry_conditions) if entry_conditions else {}
            }
            
            self.trades.append(trade_entry)
            
        except Exception as e:
            self.algorithm.Log(f"BacktestLogger.log_trade_entry error: {e}")
    
    def log_trade_exit(self, symbol: str, quantity: int, price: float, 
                      entry_price: float = None, hold_days: int = None,
                      exit_reason: str = ""):
        """
        Log a trade exit.
        
        Args:
            symbol: Trading symbol
            quantity: Number of shares sold
            price: Exit price
            entry_price: Original entry price for P&L calculation
            hold_days: Number of days held
            exit_reason: Reason for exit (stop loss, signal, etc.)
        """
        if not self.enabled:
            return
        
        try:
            # Calculate P&L if entry price provided
            pnl = None
            return_pct = None
            if entry_price is not None:
                pnl = float(quantity * (price - entry_price))
                return_pct = float((price - entry_price) / entry_price)
            
            trade_exit = {
                "trade_id": self.current_trade_id,
                "type": "exit",
                "timestamp": self.algorithm.time.isoformat(),
                "symbol": str(symbol),
                "quantity": int(quantity),
                "price": float(price),
                "value": float(quantity * price),
                "portfolio_value": float(self.algorithm.portfolio.total_portfolio_value),
                "cash": float(self.algorithm.portfolio.cash),
                "entry_price": float(entry_price) if entry_price else None,
                "pnl": pnl,
                "return_pct": return_pct,
                "hold_days": int(hold_days) if hold_days else None,
                "exit_reason": str(exit_reason)
            }
            
            self.trades.append(trade_exit)
            
        except Exception as e:
            self.algorithm.Log(f"BacktestLogger.log_trade_exit error: {e}")
    
    def log_daily_performance(self):
        """Log daily portfolio performance"""
        if not self.enabled:
            return
        
        try:
            daily_data = {
                "date": self.algorithm.time.date().isoformat(),
                "timestamp": self.algorithm.time.isoformat(),
                "portfolio_value": float(self.algorithm.portfolio.total_portfolio_value),
                "cash": float(self.algorithm.portfolio.cash),
                "holdings_value": float(self.algorithm.portfolio.total_holdings_value)
            }
            
            # Add symbol-specific holdings if symbol is set
            if self.symbol:
                try:
                    holding = self.algorithm.portfolio[self.symbol]
                    daily_data.update({
                        "symbol_quantity": float(holding.quantity),
                        "symbol_avg_price": float(holding.average_price),
                        "symbol_market_price": float(holding.price),
                        "symbol_value": float(holding.holdings_value)
                    })
                except:
                    pass
            
            self.daily_performance.append(daily_data)
            
        except Exception as e:
            self.algorithm.Log(f"BacktestLogger.log_daily_performance error: {e}")
    
    def log_indicators(self, indicator_values: Dict[str, Any]):
        """
        Log indicator values.
        
        Args:
            indicator_values: Dict of indicator names and values
        """
        if not self.enabled:
            return
        
        try:
            indicator_data = {
                "timestamp": self.algorithm.time.isoformat(),
                "indicators": self._sanitize(indicator_values)
            }
            
            self.indicator_data.append(indicator_data)
            
        except Exception as e:
            self.algorithm.Log(f"BacktestLogger.log_indicators error: {e}")
    
    def log_entry_conditions(self, conditions: Dict[str, Any], signal: bool = False):
        """
        Log entry condition states.
        
        Args:
            conditions: Dict of condition names and boolean/numeric values
            signal: Whether entry signal was triggered
        """
        if not self.enabled:
            return
        
        try:
            condition_data = {
                "timestamp": self.algorithm.time.isoformat(),
                "entry_signal": bool(signal),
                "conditions": self._sanitize(conditions)
            }
            
            self.entry_conditions.append(condition_data)
            
        except Exception as e:
            self.algorithm.Log(f"BacktestLogger.log_entry_conditions error: {e}")
    
    def save_to_object_store(self):
        """Save all logged data to QuantConnect's object store"""
        if not self.enabled:
            self.algorithm.Log("BacktestLogger: Logging disabled, skipping save")
            return False
        
        try:
            # Compile final payload
            payload = {
                "metadata": {
                    "run_id": self.run_id,
                    "strategy_name": self.strategy_name,
                    "symbol": self.symbol,
                    "timeframe_minutes": self.timeframe_minutes,
                    "start_time": self.start_time.isoformat(),
                    "end_time": self.algorithm.time.isoformat(),
                    "total_runtime_days": (self.algorithm.time - self.start_time).days
                },
                "final_state": {
                    "portfolio_value": float(self.algorithm.portfolio.total_portfolio_value),
                    "cash": float(self.algorithm.portfolio.cash),
                    "holdings_value": float(self.algorithm.portfolio.total_holdings_value),
                    "total_trades": len([t for t in self.trades if t["type"] == "entry"])
                },
                "trades": self.trades,
                "daily_performance": self.daily_performance,
                "indicator_data": self.indicator_data,
                "entry_conditions": self.entry_conditions
            }
            
            # Add symbol-specific final holdings
            if self.symbol:
                try:
                    holding = self.algorithm.portfolio[self.symbol]
                    payload["final_state"]["symbol_holdings"] = {
                        "quantity": float(holding.quantity),
                        "avg_price": float(holding.average_price),
                        "market_price": float(holding.price),
                        "value": float(holding.holdings_value)
                    }
                except:
                    pass
            
            # Sanitize the entire payload
            sanitized_payload = self._sanitize(payload)
            
            # Convert to JSON
            json_data = json.dumps(sanitized_payload, separators=(",", ":"))
            
            # Calculate size for logging
            size_bytes = len(json_data.encode('utf-8'))
            size_kb = size_bytes / 1024
            
            self.algorithm.Log(f"BacktestLogger: Saving {len(self.trades)} trades, "
                             f"{len(self.daily_performance)} daily records, "
                             f"{len(self.indicator_data)} indicator records")
            self.algorithm.Log(f"BacktestLogger: Data size: {size_kb:.1f} KB")
            
            # Save to object store
            file_path = f"backtests/{self.run_id}.json"
            saved = self.algorithm.object_store.save(file_path, json_data)
            
            if saved:
                self.algorithm.Log(f"BacktestLogger: Successfully saved to {file_path}")
            else:
                self.algorithm.Log(f"BacktestLogger: Failed to save to {file_path}")
            
            return saved
            
        except Exception as e:
            self.algorithm.Log(f"BacktestLogger.save_to_object_store error: {e}")
            return False
    
    def _sanitize(self, obj: Any, depth: int = 0, max_depth: int = 5) -> Any:
        """
        Sanitize objects for JSON serialization.
        Based on the reference implementation but simplified.
        """
        if depth > max_depth:
            try:
                return str(obj)
            except:
                return "<max-depth-exceeded>"
        
        # Handle None and basic types
        if obj is None or isinstance(obj, (bool, int, float, str)):
            return obj
        
        # Handle datetime objects
        if hasattr(obj, 'isoformat'):
            try:
                return obj.isoformat()
            except:
                return str(obj)
        
        # Handle numpy types (try import to avoid errors if not available)
        try:
            import numpy as np
            if isinstance(obj, np.generic):
                return obj.item()
            if isinstance(obj, np.ndarray):
                return obj.tolist()
        except ImportError:
            # Numpy not available, skip numpy handling
            pass
        except:
            pass
        
        # Handle QuantConnect Symbol
        try:
            if hasattr(obj, 'value') and hasattr(obj, 'id'):  # Likely a QC Symbol
                return str(obj)
        except:
            pass
        
        # Handle dictionaries
        if isinstance(obj, dict):
            result = {}
            for k, v in obj.items():
                try:
                    key = str(k)
                    result[key] = self._sanitize(v, depth + 1, max_depth)
                except:
                    result["<error-key>"] = "<error-value>"
            return result
        
        # Handle lists and tuples
        if isinstance(obj, (list, tuple)):
            return [self._sanitize(item, depth + 1, max_depth) for item in obj]
        
        # Handle sets
        if isinstance(obj, set):
            return [self._sanitize(item, depth + 1, max_depth) for item in list(obj)]
        
        # Fallback to string conversion
        try:
            return str(obj)
        except:
            return "<unserializable>"
from AlgorithmImports import * 
from config import StrategyConfig 
import json 
import numpy as np 

from typing import Any, Dict, List, Tuple, Union

from datetime import datetime, timezone
import uuid, math

from services.indicators import IndicatorHub
from services.execution_service import ExecutionService
from services.app_logging import BacktestLogger, ObjectStoreSink
from services.rules import build_default_entry_rules, UptrendRule
from services.risk import AtrStopManager
from services.plotting import Plotter
from services.windows import rolling_percentile

class SimpleCrossOverAlgo(QCAlgorithm):   
    def initialize(self) -> None:        
        try:
            self._cfg: StrategyConfig = StrategyConfig() 
            self._symbol: Symbol = Symbol.EMPTY 
            self._fast: SimpleMovingAverage = SimpleMovingAverage(1) 
            self._slow: SimpleMovingAverage = SimpleMovingAverage(1) 
            self._execution_service: Any = None 
            self._test_entered: bool = False 
            self._results: List[Dict[str, Any]] = [] 
            self._bbw_threshold: float = 0.0

            # Load configuration (preserve existing behavior if external code overwrites self._cfg later)
            cfg = self._cfg

            # Dates
            y_1 = int(cfg.y_1)
            m_1 = int(cfg.m_1)
            d_1 = int(cfg.d_1)
            y_2 = int(cfg.y_2)
            m_2 = int(cfg.m_2)
            d_2 = int(cfg.d_2)

            # Engine configuration
            self.set_start_date(y_1, m_1, d_1)
            self.set_end_date(y_2, m_2, d_2)
            self.set_cash(100000)

            # Universe and indicators
            security = self.add_equity(cfg.symbol, cfg.resolution)
            self._symbol = security.symbol

            if cfg.warmup_bars > 0:
                self.set_warmup(cfg.warmup_bars)

            # Example indicators for crossover logic
            self._fast = self.sma(self._symbol, 10, cfg.resolution)
            self._slow = self.sma(self._symbol, 30, cfg.resolution)

            # Optional: Setup external execution service if one exists in the environment
            try:
                self._execution_service = ExecutionService(self, hub= None, cfg=self._cfg)  # type: ignore[attr-defined]
            except Exception:
                self._execution_service = None

            # Optional debug-time scheduled entry (kept exactly when debugging=True)
            if cfg.debugging:
                self.schedule.on(
                    self.date_rules.every_day(self._symbol),
                    self.time_rules.at(10, 1),
                    self._test_enter_once
                )

            # Emit one-line compact configuration snapshot for diffing runs
            self.debug(
                f"[cfg] run_id={cfg.run_id} debug={cfg.debugging} "
                f"start={y_1:04d}-{m_1:02d}-{d_1:02d} end={y_2:04d}-{m_2:02d}-{d_2:02d} "
                f"symbol={cfg.symbol} res={cfg.resolution} warmup_bars={cfg.warmup_bars} "
                f"plotting={cfg.plotting_enabled} write_results_enabled={cfg.write_results_enabled}"
            )
        except Exception as e:
            try:
                Extensions.set_runtime_error(self, e, "initialize")  # type: ignore[attr-defined]
            except Exception:
                pass
            self.debug(f"[initialize] exception: {e}")
            raise

    def on_data(self, slice: Slice) -> None:
        try:
            if self.is_warming_up:
                return

            if not self._fast.is_ready or not self._slow.is_ready:
                return

            fast = float(self._fast.current.value)
            slow = float(self._slow.current.value)

            invested = self.portfolio[self._symbol].invested

            if not invested and fast > slow:
                self.set_holdings(self._symbol, 1.0)
            elif invested and fast < slow:
                if self._execution_service is not None:
                    try:
                        self._execution_service.liquidate(self._symbol)  # type: ignore[attr-defined]
                    except Exception:
                        self.liquidate(self._symbol)
                else:
                    self.liquidate(self._symbol)
        except Exception as e:
            try:
                bar_time = slice.time if slice is not None else self.time
            except Exception:
                bar_time = self.time
            try:
                Extensions.set_runtime_error(self, e, "on_data")  # type: ignore[attr-defined]
            except Exception:
                pass
            self.debug(f"[on_data] exception at {bar_time}: {e}")
            raise

    def on_end_of_algorithm(self) -> None:
        try:
            cfg = self._cfg
            payload: Dict[str, Any] = {
                "run_id": cfg.run_id if len(cfg.run_id) > 0 else str(uuid.uuid_4()),
                "end_time": self.time.isoformat(),
                "symbol": str(self._symbol) if self._symbol is not None else "",
                "final_cash": float(self.portfolio.cash),
                "final_total_portfolio_value": float(self.portfolio.total_portfolio_value),
                "holdings": {
                    "quantity": float(self.portfolio[self._symbol].quantity) if self._symbol is not None else 0.0,
                    "avg_price": float(self.portfolio[self._symbol].average_price) if self._symbol is not None else 0.0
                }
            }

            # Sanitize to ensure JSON serializability
            payload_sanitized = self._json_sanitize(payload)

            # Pre-save diagnostics
            row_count = 1
            approx_size = -1
            try:
                approx_size = len(json.dumps(payload_sanitized, separators=(",", ":")))
            except Exception:
                approx_size = -1
            self.debug(f"[save] rows={row_count} approx_json_size={approx_size}B")

            if not cfg.write_results_enabled:
                self.debug("[save] Skipped ObjectStore write (write_results_enabled=False).")
                return

            # Determine key; ensure uuid.uuid_4() is used in fallback
            key = cfg.run_id if len(cfg.run_id) > 0 else str(uuid.uuid_4())
            path = f"results/{key}.json"

            saved = False
            try:
                saved = self.object_store.save(path, json.dumps(payload_sanitized))
            except Exception as e:
                self.debug(f"[save] ObjectStore.save error for key={path}: {e}")
                saved = False

            self.debug(f"[save] key={path} saved={saved}")
        except Exception as e:
            try:
                Extensions.set_runtime_error(self, e, "on_end_of_algorithm")  # type: ignore[attr-defined]
            except Exception:
                pass
            self.debug(f"[on_end_of_algorithm] exception: {e}")
            raise

    # Keep only one definition (remove any duplicates in previous versions)
    def _get_bbw_threshold(self) -> float:
        return self._bbw_threshold

    def _test_enter_once(self) -> None:
        if self._test_entered:
            return
        self._test_entered = True
        try:            
            self.set_holdings(self._symbol, 0.1)            
            self.debug("[test] placed initial debug order (once).")
        except Exception as e:
            try:
                Extensions.set_runtime_error(self, e, "test_enter_once")  # type: ignore[attr-defined]
            except Exception:
                pass
            self.debug(f"[test] exception during scheduled entry: {e}")
            raise

    def _json_sanitize(
        self,
        obj: Any,
        depth: int = 0,
        max_depth: int = 4
    ) -> Any:
        if depth > max_depth:
            try:
                return str(obj)
            except Exception:
                return "<depth-exceeded>"

        # Primitives that are JSON-serializable
        if obj is None or isinstance(obj, (bool, int, float, str)):
            return obj

        # datetime-like
        if isinstance(obj, (datetime, date, time)):
            try:
                return obj.isoformat()
            except Exception:
                return str(obj)

        # numpy scalars
        try:
            if isinstance(obj, np.generic):
                return obj.item()
        except Exception:
            pass

        # numpy arrays
        try:
            if isinstance(obj, np.ndarray):
                return [self._json_sanitize(x, depth + 1, max_depth) for x in obj.tolist()]
        except Exception:
            pass

        # QuantConnect Symbol or other domain objects
        try:
            if isinstance(obj, Symbol):
                return str(obj)
        except Exception:
            pass

        # dict-like
        if isinstance(obj, dict):
            out: Dict[str, Any] = {}
            for k, v in obj.items():
                try:
                    key = str(k)
                except Exception:
                    key = "<unserializable-key>"
                out[key] = self._json_sanitize(v, depth + 1, max_depth)
            return out

        # list-like
        if isinstance(obj, list):
            return [self._json_sanitize(x, depth + 1, max_depth) for x in obj]

        # tuple/set -> list
        if isinstance(obj, (tuple, set)):
            return [self._json_sanitize(x, depth + 1, max_depth) for x in list(obj)]

        # Fallback to string
        try:
            return str(obj)
        except Exception:
            return "<unserializable>"

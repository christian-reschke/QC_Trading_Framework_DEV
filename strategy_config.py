# region imports
from AlgorithmImports import *
# endregion

"""
Strategy configuration constants
"""

# Symbol configuration - single source of truth
SYMBOL = "MDB"

# Timeframe configuration - single source of truth
TIMEFRAME_MINUTES = 30

# Backtest period configuration - single source of truth
START_DATE = "2019-01-01"
END_DATE = "2024-12-31"

# Starting capital configuration - single source of truth
STARTING_CAPITAL = 100000

# Version configuration - single source of truth
STRATEGY_VERSION = "v2.1.75"

# Logging configuration - single source of truth
LOGGING_ENABLED = True
RUN_ID = ""  # Auto-generate unique ID if empty
LOG_TRADES = True
LOG_DAILY_PERFORMANCE = True
LOG_INDICATORS = True
LOG_ENTRY_CONDITIONS = True
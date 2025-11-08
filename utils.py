"""
Shared utility functions for the trading framework
"""
import re
import json

def print_red(message):
    """Print message in red color"""
    print(f"\033[91m{message}\033[0m")

def print_green(message):
    """Print message in green color"""
    print(f"\033[92m{message}\033[0m")

def print_yellow(message):
    """Print message in yellow color"""
    print(f"\033[93m{message}\033[0m")

def print_error(message):
    """Print error message in red"""
    print_red(f"ERROR: {message}")

def print_success(message):
    """Print success message in green"""
    print_green(f"SUCCESS: {message}")

def print_warning(message):
    """Print warning message in yellow"""
    print_yellow(f"WARNING: {message}")


class QCOutputParser:
    """
    Parser for QuantConnect backtest output with convenient getter methods.
    
    Usage:
        parser = QCOutputParser(qc_output_string)
        return_pct = parser.get_return_percent()
        sharpe = parser.get_sharpe_ratio()
        name = parser.get_backtest_name()
    """
    
    def __init__(self, qc_output):
        """
        Initialize parser with QuantConnect output.
        
        Args:
            qc_output (str): Raw QuantConnect backtest output string
            
        Raises:
            ValueError: If required fields cannot be parsed from output
        """
        self.raw_output = qc_output
        self.data = self._parse_output(qc_output)
    
    def _parse_output(self, qc_output):
        """
        Parse QuantConnect backtest output into structured format.
        
        Args:
            qc_output (str): Raw QuantConnect backtest output string
            
        Returns:
            dict: Parsed backtest results
            
        Raises:
            ValueError: If required fields cannot be parsed from output
        """
        result = {
            "backtest_info": {},
            "performance_metrics": {},
            "risk_metrics": {},
            "trade_metrics": {},
            "raw_output": qc_output
        }
        
        try:
            # Extract backtest name
            backtest_name_match = re.search(r"Started backtest named '([^']+)'", qc_output)
            if backtest_name_match:
                result["backtest_info"]["name"] = backtest_name_match.group(1)
            
            # Extract backtest ID
            backtest_id_match = re.search(r"Backtest id: ([a-f0-9]+)", qc_output)
            if backtest_id_match:
                result["backtest_info"]["id"] = backtest_id_match.group(1)
            
            # Extract backtest URL
            backtest_url_match = re.search(r"Backtest url:\s*\n(https://[^\s]+)", qc_output)
            if backtest_url_match:
                result["backtest_info"]["url"] = backtest_url_match.group(1)
            
            # Extract strategy version
            version_match = re.search(r"Strategy Version\s*\|\s*([^\s]+)", qc_output)
            if version_match:
                result["backtest_info"]["strategy_version"] = version_match.group(1)
            
            # Parse the statistics table
            # Define metrics and their categories
            metrics_map = {
                # Performance metrics
                "Equity": ("performance_metrics", "final_equity"),
                "Return": ("performance_metrics", "return_percent"),
                "Compounding Annual Return": ("performance_metrics", "annual_return_percent"),
                "End Equity": ("performance_metrics", "end_equity"),
                "Start Equity": ("performance_metrics", "start_equity"),
                "Net Profit": ("performance_metrics", "net_profit_percent"),
                
                # Risk metrics
                "Drawdown": ("risk_metrics", "max_drawdown_percent"),
                "Sharpe Ratio": ("risk_metrics", "sharpe_ratio"),
                "Sortino Ratio": ("risk_metrics", "sortino_ratio"),
                "Probabilistic Sharpe Ratio": ("risk_metrics", "probabilistic_sharpe_ratio"),
                "Annual Standard Deviation": ("risk_metrics", "annual_std_dev"),
                "Annual Variance": ("risk_metrics", "annual_variance"),
                "Alpha": ("risk_metrics", "alpha"),
                "Beta": ("risk_metrics", "beta"),
                "Information Ratio": ("risk_metrics", "information_ratio"),
                "Tracking Error": ("risk_metrics", "tracking_error"),
                "Treynor Ratio": ("risk_metrics", "treynor_ratio"),
                
                # Trade metrics
                "Total Orders": ("trade_metrics", "total_orders"),
                "Average Win": ("trade_metrics", "average_win_percent"),
                "Average Loss": ("trade_metrics", "average_loss_percent"),
                "Expectancy": ("trade_metrics", "expectancy"),
                "Loss Rate": ("trade_metrics", "loss_rate_percent"),
                "Win Rate": ("trade_metrics", "win_rate_percent"),
                "Profit-Loss Ratio": ("trade_metrics", "profit_loss_ratio"),
                "Fees": ("trade_metrics", "total_fees"),
                "Volume": ("trade_metrics", "volume"),
                "Holdings": ("trade_metrics", "holdings"),
                "Unrealized": ("trade_metrics", "unrealized"),
                "Portfolio Turnover": ("trade_metrics", "portfolio_turnover"),
                "Estimated Strategy Capacity": ("trade_metrics", "strategy_capacity"),
                "Lowest Capacity Asset": ("trade_metrics", "lowest_capacity_asset"),
                "Drawdown Recovery": ("trade_metrics", "drawdown_recovery")
            }
            
            # Parse each metric from the table
            for metric_name, (category, json_key) in metrics_map.items():
                # Look for the metric in the table format
                pattern = rf"{re.escape(metric_name)}\s*\|\s*([^\|]+?)(?:\s*\||\s*$)"
                match = re.search(pattern, qc_output, re.MULTILINE)
                
                if match:
                    raw_value = match.group(1).strip()
                    parsed_value = self._parse_metric_value(raw_value)
                    result[category][json_key] = parsed_value
            
            # Validate that we got essential metrics
            essential_metrics = ["return_percent", "sharpe_ratio", "max_drawdown_percent"]
            missing_metrics = []
            
            for metric in essential_metrics:
                found = False
                for category in ["performance_metrics", "risk_metrics"]:
                    if metric in result[category]:
                        found = True
                        break
                if not found:
                    missing_metrics.append(metric)
            
            if missing_metrics:
                raise ValueError(f"Failed to parse essential metrics: {missing_metrics}")
            
            return result
            
        except Exception as e:
            raise ValueError(f"Failed to parse QuantConnect output: {str(e)}")
    
    def _parse_metric_value(self, raw_value):
        """
        Parse a metric value from string to appropriate type.
        
        Args:
            raw_value (str): Raw value from QuantConnect output
            
        Returns:
            Union[float, int, str]: Parsed value
        """
        # Remove common formatting
        clean_value = raw_value.strip()
        
        # Handle empty or dash values
        if not clean_value or clean_value == "-" or clean_value == "":
            return None
        
        # Handle percentage values
        if clean_value.endswith("%"):
            try:
                return float(clean_value[:-1].strip())
            except ValueError:
                return clean_value
        
        # Handle dollar values
        if clean_value.startswith("$") or clean_value.startswith("-$"):
            try:
                # Remove $ and commas, handle negative
                numeric_part = clean_value.replace("$", "").replace(",", "")
                return float(numeric_part)
            except ValueError:
                return clean_value
        
        # Try to parse as float
        try:
            return float(clean_value.replace(",", ""))
        except ValueError:
            pass
        
        # Try to parse as int
        try:
            return int(clean_value.replace(",", ""))
        except ValueError:
            pass
        
        # Return as string if all else fails
        return clean_value
    
    # Getter methods for important metrics
    def get_backtest_name(self):
        """Get the backtest name"""
        return self.data["backtest_info"].get("name")
    
    def get_backtest_id(self):
        """Get the backtest ID"""
        return self.data["backtest_info"].get("id")
    
    def get_backtest_url(self):
        """Get the backtest URL"""
        return self.data["backtest_info"].get("url")
    
    def get_strategy_version(self):
        """Get the strategy version"""
        return self.data["backtest_info"].get("strategy_version")
    
    def get_return_percent(self):
        """Get the return percentage"""
        return self.data["performance_metrics"].get("return_percent")
    
    def get_annual_return_percent(self):
        """Get the annual return percentage"""
        return self.data["performance_metrics"].get("annual_return_percent")
    
    def get_net_profit_percent(self):
        """Get the net profit percentage"""
        return self.data["performance_metrics"].get("net_profit_percent")
    
    def get_final_equity(self):
        """Get the final equity value"""
        return self.data["performance_metrics"].get("final_equity")
    
    def get_end_equity(self):
        """Get the end equity value"""
        return self.data["performance_metrics"].get("end_equity")
    
    def get_start_equity(self):
        """Get the start equity value"""
        return self.data["performance_metrics"].get("start_equity")
    
    def get_max_drawdown_percent(self):
        """Get the maximum drawdown percentage"""
        return self.data["risk_metrics"].get("max_drawdown_percent")
    
    def get_sharpe_ratio(self):
        """Get the Sharpe ratio"""
        return self.data["risk_metrics"].get("sharpe_ratio")
    
    def get_sortino_ratio(self):
        """Get the Sortino ratio"""
        return self.data["risk_metrics"].get("sortino_ratio")
    
    def get_alpha(self):
        """Get the Alpha"""
        return self.data["risk_metrics"].get("alpha")
    
    def get_beta(self):
        """Get the Beta"""
        return self.data["risk_metrics"].get("beta")
    
    def get_total_orders(self):
        """Get the total number of orders"""
        return self.data["trade_metrics"].get("total_orders")
    
    def get_win_rate_percent(self):
        """Get the win rate percentage"""
        return self.data["trade_metrics"].get("win_rate_percent")
    
    def get_loss_rate_percent(self):
        """Get the loss rate percentage"""
        return self.data["trade_metrics"].get("loss_rate_percent")
    
    def get_profit_loss_ratio(self):
        """Get the profit-loss ratio"""
        return self.data["trade_metrics"].get("profit_loss_ratio")
    
    def get_total_fees(self):
        """Get the total fees"""
        return self.data["trade_metrics"].get("total_fees")
    
    def get_expectancy(self):
        """Get the expectancy"""
        return self.data["trade_metrics"].get("expectancy")
    
    def get_raw_output(self):
        """Get the raw QuantConnect output"""
        return self.raw_output
    
    def to_dict(self):
        """Get the full parsed data as dictionary"""
        return self.data
    
    def to_json(self, indent=None):
        """Get the parsed data as JSON string"""
        return json.dumps(self.data, indent=indent)


# Backward compatibility function
def parse_qc_output_to_json(qc_output):
    """
    Parse QuantConnect backtest output into structured JSON format.
    
    Args:
        qc_output (str): Raw QuantConnect backtest output string
        
    Returns:
        dict: Parsed backtest results in JSON format
        
    Raises:
        ValueError: If required fields cannot be parsed from output
    """
    parser = QCOutputParser(qc_output)
    return parser.to_dict()
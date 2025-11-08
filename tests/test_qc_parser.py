"""
Unit tests for QuantConnect output parser
"""
import unittest
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import QCOutputParser, parse_qc_output_to_json
from examples.backtest_outputs_from_qc import get_backtest_output, get_negative_backtest_output


class TestQCOutputParser(unittest.TestCase):
    """Test cases for QuantConnect output parser"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.positive_output = get_backtest_output()
        self.negative_output = get_negative_backtest_output()
        self.positive_parser = QCOutputParser(self.positive_output)
        self.negative_parser = QCOutputParser(self.negative_output)
    
    def test_parse_positive_return(self):
        """Test parsing positive return values"""
        return_pct = self.positive_parser.get_return_percent()
        self.assertIsInstance(return_pct, float)
        self.assertAlmostEqual(return_pct, 10.48, places=2)
        self.assertGreater(return_pct, 0)
    
    def test_parse_negative_return(self):
        """Test parsing negative return values"""
        return_pct = self.negative_parser.get_return_percent()
        self.assertIsInstance(return_pct, float)
        self.assertAlmostEqual(return_pct, -37.31, places=2)
        self.assertLess(return_pct, 0)
    
    def test_parse_positive_drawdown(self):
        """Test parsing drawdown for positive performance case"""
        drawdown = self.positive_parser.get_max_drawdown_percent()
        self.assertIsInstance(drawdown, float)
        self.assertAlmostEqual(drawdown, 38.2, places=1)
        self.assertGreater(drawdown, 0)
    
    def test_parse_negative_drawdown(self):
        """Test parsing drawdown for negative performance case"""
        drawdown = self.negative_parser.get_max_drawdown_percent()
        self.assertIsInstance(drawdown, float)
        self.assertAlmostEqual(drawdown, 60.1, places=1)
        self.assertGreater(drawdown, 0)
    
    def test_parse_positive_sharpe(self):
        """Test parsing positive Sharpe ratio"""
        sharpe = self.positive_parser.get_sharpe_ratio()
        self.assertIsInstance(sharpe, float)
        self.assertAlmostEqual(sharpe, 0.235, places=3)
        self.assertGreater(sharpe, 0)
    
    def test_parse_negative_sharpe(self):
        """Test parsing negative Sharpe ratio"""
        sharpe = self.negative_parser.get_sharpe_ratio()
        self.assertIsInstance(sharpe, float)
        self.assertAlmostEqual(sharpe, -0.683, places=3)
        self.assertLess(sharpe, 0)
    
    def test_backtest_name_getter(self):
        """Test backtest name getter"""
        name_pos = self.positive_parser.get_backtest_name()
        name_neg = self.negative_parser.get_backtest_name()
        
        self.assertEqual(name_pos, "Crawling Yellow-Green Giraffe")
        self.assertEqual(name_neg, "Determined Blue Antelope")
    
    def test_backtest_id_getter(self):
        """Test backtest ID getter"""
        id_pos = self.positive_parser.get_backtest_id()
        id_neg = self.negative_parser.get_backtest_id()
        
        self.assertEqual(id_pos, "3d044e792641d892dcae6312dc0d3bfd")
        self.assertEqual(id_neg, "afb54e1a186b17a68f23f38bbf3f1416")
    
    def test_strategy_version_getter(self):
        """Test strategy version getter"""
        version_pos = self.positive_parser.get_strategy_version()
        version_neg = self.negative_parser.get_strategy_version()
        
        self.assertEqual(version_pos, "v2.1.56")
        self.assertEqual(version_neg, "v2.1.53")
    
    def test_equity_getters(self):
        """Test equity-related getters"""
        final_equity = self.positive_parser.get_final_equity()
        end_equity = self.positive_parser.get_end_equity()
        start_equity = self.positive_parser.get_start_equity()
        
        self.assertAlmostEqual(final_equity, 110477.43, places=2)
        self.assertAlmostEqual(end_equity, 110477.43, places=2)
        self.assertEqual(start_equity, 100000)
    
    def test_trade_metrics_getters(self):
        """Test trade metrics getters"""
        total_orders = self.positive_parser.get_total_orders()
        win_rate = self.positive_parser.get_win_rate_percent()
        loss_rate = self.positive_parser.get_loss_rate_percent()
        profit_loss_ratio = self.positive_parser.get_profit_loss_ratio()
        
        self.assertEqual(total_orders, 77)
        self.assertEqual(win_rate, 32)
        self.assertEqual(loss_rate, 68)
        self.assertAlmostEqual(profit_loss_ratio, 2.64, places=2)
    
    def test_fees_getter(self):
        """Test fees getter (negative value)"""
        fees_pos = self.positive_parser.get_total_fees()
        fees_neg = self.negative_parser.get_total_fees()
        
        self.assertAlmostEqual(fees_pos, -124.88, places=2)
        self.assertAlmostEqual(fees_neg, -134.72, places=2)
        self.assertLess(fees_pos, 0)
        self.assertLess(fees_neg, 0)
    
    def test_risk_metrics_getters(self):
        """Test risk metrics getters"""
        alpha = self.positive_parser.get_alpha()
        beta = self.positive_parser.get_beta()
        sortino = self.positive_parser.get_sortino_ratio()
        
        self.assertAlmostEqual(alpha, -0.059, places=3)
        self.assertAlmostEqual(beta, 1.205, places=3)
        self.assertAlmostEqual(sortino, 0.378, places=3)
    
    def test_expectancy_getter(self):
        """Test expectancy getter"""
        expectancy_pos = self.positive_parser.get_expectancy()
        expectancy_neg = self.negative_parser.get_expectancy()
        
        self.assertAlmostEqual(expectancy_pos, 0.149, places=3)
        self.assertAlmostEqual(expectancy_neg, -0.164, places=3)
    
    def test_raw_output_getter(self):
        """Test raw output getter"""
        raw_pos = self.positive_parser.get_raw_output()
        raw_neg = self.negative_parser.get_raw_output()
        
        self.assertEqual(raw_pos, self.positive_output)
        self.assertEqual(raw_neg, self.negative_output)
    
    def test_to_dict_method(self):
        """Test to_dict method"""
        data = self.positive_parser.to_dict()
        
        self.assertIn("backtest_info", data)
        self.assertIn("performance_metrics", data)
        self.assertIn("risk_metrics", data)
        self.assertIn("trade_metrics", data)
        self.assertIn("raw_output", data)
    
    def test_to_json_method(self):
        """Test to_json method"""
        json_str = self.positive_parser.to_json()
        self.assertIsInstance(json_str, str)
        
        # Test with indentation
        json_indented = self.positive_parser.to_json(indent=2)
        self.assertIn('\n', json_indented)  # Should have newlines when indented
    
    def test_backward_compatibility(self):
        """Test that old function still works"""
        result = parse_qc_output_to_json(self.positive_output)
        
        # Should have same structure as class method
        self.assertIn("performance_metrics", result)
        self.assertIn("return_percent", result["performance_metrics"])
        self.assertAlmostEqual(result["performance_metrics"]["return_percent"], 10.48, places=2)
    
    def test_invalid_output_handling(self):
        """Test handling of invalid/incomplete output"""
        invalid_output = "This is not a valid QuantConnect output"
        
        with self.assertRaises(ValueError) as context:
            QCOutputParser(invalid_output)
        
        self.assertIn("Failed to parse essential metrics", str(context.exception))


if __name__ == "__main__":
    unittest.main()
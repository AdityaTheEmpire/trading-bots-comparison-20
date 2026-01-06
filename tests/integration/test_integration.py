"""
Integration tests for the complete framework.
"""
import pytest
import json
from src.core.backtest_engine import BacktestEngine
from src.core.metrics import PerformanceMetrics
from src.analysis.visualizer import PerformanceVisualizer
from src.analysis.report_generator import ReportGenerator
from src.utils.exporters import ResultExporter
from src.bots.freqtrade_bot import FreqtradeBot
from src.bots.jesse_bot import JesseBot


class TestBacktestEngine:
    """Tests for BacktestEngine."""
    
    def test_initialization(self):
        config = {
            'delta_exchange': {'testnet': True},
            'backtest_settings': {
                'start_date': '2023-01-01',
                'end_date': '2023-12-31',
                'initial_capital': 10000,
                'symbols': ['BTCUSDT']
            }
        }
        engine = BacktestEngine(config)
        assert engine.config == config
    
    def test_run_backtest(self, bot_config):
        config = {
            'delta_exchange': {'testnet': True},
            'backtest_settings': {
                'start_date': '2023-01-01',
                'end_date': '2023-01-31',
                'initial_capital': 10000,
                'symbols': ['BTCUSDT']
            },
            'performance_metrics': {'risk_free_rate': 0.02}
        }
        engine = BacktestEngine(config)
        bot = FreqtradeBot(bot_config)
        result = engine.run_backtest(bot, 'BTCUSDT')
        
        assert 'bot_name' in result
        assert 'sharpe_ratio' in result
        assert 'max_drawdown_pct' in result


class TestPerformanceMetrics:
    """Tests for PerformanceMetrics."""
    
    def test_calculate_returns(self):
        portfolio_values = [10000, 10100, 10200, 10150, 10300]
        returns = PerformanceMetrics.calculate_returns(portfolio_values)
        assert len(returns) == len(portfolio_values) - 1
    
    def test_sharpe_ratio(self):
        portfolio_values = [10000, 10100, 10200, 10300, 10400]
        sharpe = PerformanceMetrics.sharpe_ratio(portfolio_values)
        assert isinstance(sharpe, float)
    
    def test_max_drawdown(self):
        portfolio_values = [10000, 11000, 9000, 9500, 12000]
        dd = PerformanceMetrics.max_drawdown(portfolio_values)
        assert 'max_drawdown' in dd
        assert 'max_drawdown_pct' in dd
        assert dd['max_drawdown_pct'] > 0
    
    def test_win_rate(self):
        trades = [
            {'type': 'buy', 'price': 100, 'cost': 1000},
            {'type': 'sell', 'price': 110, 'proceeds': 1100},
            {'type': 'buy', 'price': 110, 'cost': 1100},
            {'type': 'sell', 'price': 105, 'proceeds': 1050},
        ]
        win_rate = PerformanceMetrics.win_rate(trades)
        assert win_rate == 50.0
    
    def test_profit_factor(self):
        trades = [
            {'type': 'buy', 'price': 100, 'cost': 1000},
            {'type': 'sell', 'price': 110, 'proceeds': 1100},
        ]
        pf = PerformanceMetrics.profit_factor(trades)
        assert pf >= 0


class TestResultExporter:
    """Tests for ResultExporter."""
    
    def test_export_to_json(self, tmp_path):
        exporter = ResultExporter(output_dir=str(tmp_path))
        results = [
            {'bot_name': 'TestBot', 'total_return_pct': 10.5}
        ]
        filepath = exporter.export_to_json(results, 'test_results.json')
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        assert len(data) == 1
        assert data[0]['bot_name'] == 'TestBot'
    
    def test_export_to_csv(self, tmp_path):
        import pandas as pd
        exporter = ResultExporter(output_dir=str(tmp_path))
        df = pd.DataFrame([
            {'bot_name': 'TestBot', 'total_return_pct': 10.5}
        ])
        filepath = exporter.export_to_csv(df, 'test_results.csv')
        
        df_loaded = pd.read_csv(filepath)
        assert len(df_loaded) == 1
        assert df_loaded.iloc[0]['bot_name'] == 'TestBot'


class TestIntegrationWorkflow:
    """Integration tests for complete workflow."""
    
    def test_complete_workflow(self, bot_config, tmp_path):
        """Test the complete workflow from backtest to report generation."""
        # Setup
        config = {
            'delta_exchange': {'testnet': True},
            'backtest_settings': {
                'start_date': '2023-01-01',
                'end_date': '2023-01-31',
                'initial_capital': 10000,
                'symbols': ['BTCUSDT']
            },
            'performance_metrics': {'risk_free_rate': 0.02}
        }
        
        # Initialize bots
        bots = [FreqtradeBot(bot_config), JesseBot(bot_config)]
        
        # Run backtests
        engine = BacktestEngine(config)
        results = engine.run_all_backtests(bots)
        
        assert len(results) >= 2  # At least 2 bots * 1 symbol
        
        # Aggregate results
        aggregated_df = engine.get_aggregated_results()
        assert len(aggregated_df) == 2  # 2 bots
        
        # Export results
        exporter = ResultExporter(output_dir=str(tmp_path / "results"))
        exporter.export_aggregated_results(aggregated_df)
        
        # Verify exports
        assert (tmp_path / "results" / "aggregated_results.csv").exists()
        assert (tmp_path / "results" / "aggregated_results.json").exists()

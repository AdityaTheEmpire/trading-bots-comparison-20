"""
Test cases for all 20 trading bots.
"""
import pytest
from src.bots.freqtrade_bot import FreqtradeBot
from src.bots.jesse_bot import JesseBot
from src.bots.ccxt_bot import CCXTBot
from src.bots.backtrader_bot import BacktraderBot
from src.bots.additional_bots import (
    QuantConnectBot, ZiplineBot, VectorBTBot, TALibBot,
    PyAlgoTradeBot, CatalystBot
)
from src.bots.strategy_bots import (
    RSIBot, MACDBot, BollingerBot, MACrossoverBot,
    MeanReversionBot, MomentumBot, BreakoutBot,
    GridTradingBot, ArbitrageBot, MarketMakingBot
)


class TestFreqtradeBot:
    """Tests for FreqtradeBot."""
    
    def test_initialization(self, bot_config):
        bot = FreqtradeBot(bot_config)
        assert bot.name == "Freqtrade"
        assert bot.short_window == 20
        assert bot.long_window == 50
    
    def test_generate_signals(self, bot_config, sample_ohlcv_data):
        bot = FreqtradeBot(bot_config)
        signals = bot.generate_signals(sample_ohlcv_data)
        assert 'signal' in signals.columns
        assert len(signals) == len(sample_ohlcv_data)
    
    def test_backtest(self, bot_config, sample_ohlcv_data):
        bot = FreqtradeBot(bot_config)
        result = bot.backtest(sample_ohlcv_data, initial_capital=10000)
        assert 'bot_name' in result
        assert 'final_capital' in result
        assert result['initial_capital'] == 10000


class TestJesseBot:
    """Tests for JesseBot."""
    
    def test_initialization(self, bot_config):
        bot = JesseBot(bot_config)
        assert bot.name == "Jesse"
        assert bot.rsi_period == 14
    
    def test_generate_signals(self, bot_config, sample_ohlcv_data):
        bot = JesseBot(bot_config)
        signals = bot.generate_signals(sample_ohlcv_data)
        assert 'signal' in signals.columns
        assert 'rsi' in signals.columns
    
    def test_backtest(self, bot_config, sample_ohlcv_data):
        bot = JesseBot(bot_config)
        result = bot.backtest(sample_ohlcv_data, initial_capital=10000)
        assert result['bot_name'] == "Jesse"


class TestCCXTBot:
    """Tests for CCXTBot."""
    
    def test_initialization(self, bot_config):
        bot = CCXTBot(bot_config)
        assert bot.name == "CCXT"
        assert bot.bb_period == 20
    
    def test_generate_signals(self, bot_config, sample_ohlcv_data):
        bot = CCXTBot(bot_config)
        signals = bot.generate_signals(sample_ohlcv_data)
        assert 'signal' in signals.columns
        assert 'bb_upper' in signals.columns
        assert 'bb_lower' in signals.columns


class TestBacktraderBot:
    """Tests for BacktraderBot."""
    
    def test_initialization(self, bot_config):
        bot = BacktraderBot(bot_config)
        assert bot.name == "Backtrader"
    
    def test_calculate_macd(self, bot_config, sample_ohlcv_data):
        bot = BacktraderBot(bot_config)
        macd_data = bot.calculate_macd(sample_ohlcv_data['close'])
        assert 'macd' in macd_data.columns
        assert 'signal' in macd_data.columns


class TestQuantConnectBot:
    """Tests for QuantConnectBot."""
    
    def test_initialization(self, bot_config):
        bot = QuantConnectBot(bot_config)
        assert bot.name == "QuantConnect"
    
    def test_backtest(self, bot_config, sample_ohlcv_data):
        bot = QuantConnectBot(bot_config)
        result = bot.backtest(sample_ohlcv_data, initial_capital=10000)
        assert result['bot_name'] == "QuantConnect"


class TestZiplineBot:
    """Tests for ZiplineBot."""
    
    def test_initialization(self, bot_config):
        bot = ZiplineBot(bot_config)
        assert bot.name == "Zipline"
    
    def test_generate_signals(self, bot_config, sample_ohlcv_data):
        bot = ZiplineBot(bot_config)
        signals = bot.generate_signals(sample_ohlcv_data)
        assert 'z_score' in signals.columns


class TestVectorBTBot:
    """Tests for VectorBTBot."""
    
    def test_initialization(self, bot_config):
        bot = VectorBTBot(bot_config)
        assert bot.name == "VectorBT"


class TestTALibBot:
    """Tests for TALibBot."""
    
    def test_initialization(self, bot_config):
        bot = TALibBot(bot_config)
        assert bot.name == "TALib"
    
    def test_calculate_stochastic(self, bot_config, sample_ohlcv_data):
        bot = TALibBot(bot_config)
        stoch = bot.calculate_stochastic(sample_ohlcv_data)
        assert 'k' in stoch.columns
        assert 'd' in stoch.columns


class TestPyAlgoTradeBot:
    """Tests for PyAlgoTradeBot."""
    
    def test_initialization(self, bot_config):
        bot = PyAlgoTradeBot(bot_config)
        assert bot.name == "PyAlgoTrade"


class TestCatalystBot:
    """Tests for CatalystBot."""
    
    def test_initialization(self, bot_config):
        bot = CatalystBot(bot_config)
        assert bot.name == "Catalyst"


class TestRSIBot:
    """Tests for RSIBot."""
    
    def test_initialization(self, bot_config):
        bot = RSIBot(bot_config)
        assert bot.name == "RSI_Strategy"
    
    def test_calculate_rsi(self, bot_config, sample_ohlcv_data):
        bot = RSIBot(bot_config)
        rsi = bot.calculate_rsi(sample_ohlcv_data['close'])
        assert len(rsi) == len(sample_ohlcv_data)


class TestMACDBot:
    """Tests for MACDBot."""
    
    def test_initialization(self, bot_config):
        bot = MACDBot(bot_config)
        assert bot.name == "MACD_Strategy"


class TestBollingerBot:
    """Tests for BollingerBot."""
    
    def test_initialization(self, bot_config):
        bot = BollingerBot(bot_config)
        assert bot.name == "Bollinger_Strategy"


class TestMACrossoverBot:
    """Tests for MACrossoverBot."""
    
    def test_initialization(self, bot_config):
        bot = MACrossoverBot(bot_config)
        assert bot.name == "MA_Crossover_Strategy"


class TestMeanReversionBot:
    """Tests for MeanReversionBot."""
    
    def test_initialization(self, bot_config):
        bot = MeanReversionBot(bot_config)
        assert bot.name == "Mean_Reversion_Strategy"


class TestMomentumBot:
    """Tests for MomentumBot."""
    
    def test_initialization(self, bot_config):
        bot = MomentumBot(bot_config)
        assert bot.name == "Momentum_Strategy"


class TestBreakoutBot:
    """Tests for BreakoutBot."""
    
    def test_initialization(self, bot_config):
        bot = BreakoutBot(bot_config)
        assert bot.name == "Breakout_Strategy"


class TestGridTradingBot:
    """Tests for GridTradingBot."""
    
    def test_initialization(self, bot_config):
        bot = GridTradingBot(bot_config)
        assert bot.name == "Grid_Trading_Strategy"


class TestArbitrageBot:
    """Tests for ArbitrageBot."""
    
    def test_initialization(self, bot_config):
        bot = ArbitrageBot(bot_config)
        assert bot.name == "Arbitrage_Strategy"


class TestMarketMakingBot:
    """Tests for MarketMakingBot."""
    
    def test_initialization(self, bot_config):
        bot = MarketMakingBot(bot_config)
        assert bot.name == "Market_Making_Strategy"

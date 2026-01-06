# Framework Architecture

## Overview

The Trading Bots Comparison Framework is designed with a modular, extensible architecture that separates concerns and allows for easy addition of new trading bots and strategies.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Main Script                          │
│                      (main.py)                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ├── Initialize Configuration
                       ├── Create Bot Instances
                       ├── Run Backtests
                       ├── Export Results
                       ├── Generate Visualizations
                       └── Create Reports
                       │
    ┌──────────────────┴──────────────────┐
    │                                     │
    ▼                                     ▼
┌─────────────────────┐        ┌─────────────────────┐
│   Core Module       │        │   Bots Module       │
│  (src/core/)        │        │  (src/bots/)        │
├─────────────────────┤        ├─────────────────────┤
│ - base_bot.py       │        │ - freqtrade_bot.py  │
│ - metrics.py        │◄───────┤ - jesse_bot.py      │
│ - delta_api.py      │        │ - ccxt_bot.py       │
│ - backtest_engine.py│        │ - backtrader_bot.py │
└─────────────────────┘        │ - additional_bots.py│
                               │ - strategy_bots.py  │
                               └─────────────────────┘
           │                            │
           │                            │
           ▼                            ▼
┌─────────────────────┐        ┌─────────────────────┐
│  Analysis Module    │        │   Utils Module      │
│ (src/analysis/)     │        │  (src/utils/)       │
├─────────────────────┤        ├─────────────────────┤
│ - visualizer.py     │        │ - exporters.py      │
│ - report_generator.py│       └─────────────────────┘
└─────────────────────┘
```

## Module Descriptions

### Core Module (`src/core/`)

**Purpose**: Contains fundamental framework components

1. **base_bot.py** - Abstract base class for all trading bots
   - Defines the interface that all bots must implement
   - Provides common backtesting functionality
   - Manages trade execution and portfolio tracking

2. **metrics.py** - Performance metrics calculator
   - Sharpe ratio calculation
   - Maximum drawdown analysis
   - Win rate computation
   - Profit factor calculation
   - Aggregated metrics generation

3. **delta_api.py** - Delta Exchange API client
   - Fetches OHLCV market data
   - Handles API authentication
   - Provides synthetic data for testing

4. **backtest_engine.py** - Backtesting orchestrator
   - Runs backtests across multiple bots
   - Manages data fetching and bot execution
   - Aggregates results from all bots

### Bots Module (`src/bots/`)

**Purpose**: Trading bot implementations

1. **freqtrade_bot.py** - Freqtrade-style MA crossover
2. **jesse_bot.py** - RSI mean reversion
3. **ccxt_bot.py** - Bollinger Bands strategy
4. **backtrader_bot.py** - MACD strategy
5. **additional_bots.py** - 6 framework-based bots
   - QuantConnect (Momentum)
   - Zipline (Mean Reversion)
   - VectorBT (Dual MA)
   - TALib (Stochastic)
   - PyAlgoTrade (ATR Breakout)
   - Catalyst (Volume-weighted)
6. **strategy_bots.py** - 10 strategy-specific bots
   - RSI Strategy
   - MACD Strategy
   - Bollinger Strategy
   - MA Crossover
   - Mean Reversion
   - Momentum
   - Breakout
   - Grid Trading
   - Arbitrage
   - Market Making

### Analysis Module (`src/analysis/`)

**Purpose**: Result visualization and reporting

1. **visualizer.py** - Chart generation
   - Returns comparison chart
   - Sharpe ratio comparison
   - Max drawdown analysis
   - Win rate comparison
   - Profit factor comparison
   - Performance heatmap

2. **report_generator.py** - Markdown report creation
   - Executive summary
   - Top performers identification
   - Complete rankings table
   - Detailed metrics for each bot
   - Summary statistics
   - Methodology explanation

### Utils Module (`src/utils/`)

**Purpose**: Utility functions

1. **exporters.py** - Result export utilities
   - JSON export
   - CSV export
   - Trade details export

## Data Flow

```
1. Configuration Loading
   config.json → Main Script

2. Bot Initialization
   Main Script → Bot Instances (x20)

3. Data Fetching
   Delta API → Historical OHLCV Data

4. Backtesting
   Bot Instances + OHLCV Data → Raw Results

5. Metrics Calculation
   Raw Results → Performance Metrics

6. Aggregation
   Individual Results → Aggregated DataFrame

7. Export
   Aggregated Data → JSON/CSV Files

8. Visualization
   Aggregated Data → PNG Charts

9. Reporting
   Aggregated Data → Markdown Report
```

## Class Hierarchy

```
BaseTradingBot (Abstract)
├── FreqtradeBot
├── JesseBot
├── CCXTBot
├── BacktraderBot
├── QuantConnectBot
├── ZiplineBot
├── VectorBTBot
├── TALibBot
├── PyAlgoTradeBot
├── CatalystBot
├── RSIBot
├── MACDBot
├── BollingerBot
├── MACrossoverBot
├── MeanReversionBot
├── MomentumBot
├── BreakoutBot
├── GridTradingBot
├── ArbitrageBot
└── MarketMakingBot
```

## Key Design Patterns

### 1. Template Method Pattern

The `BaseTradingBot` class uses the template method pattern:
- `backtest()` defines the algorithm structure
- Subclasses implement specific methods:
  - `initialize()`
  - `generate_signals()`
  - `execute_trade()`

### 2. Strategy Pattern

Each bot implements a different trading strategy while conforming to the same interface.

### 3. Dependency Injection

Configuration is injected into bots rather than hardcoded, allowing flexibility.

### 4. Single Responsibility Principle

Each module has a single, well-defined purpose:
- Core: Framework fundamentals
- Bots: Trading strategies
- Analysis: Reporting and visualization
- Utils: Helper functions

## Extension Points

### Adding a New Bot

1. Create a new class extending `BaseTradingBot`
2. Implement required abstract methods
3. Add to `main.py` initialization
4. Create corresponding tests

### Adding New Metrics

1. Add calculation method to `PerformanceMetrics` class
2. Update `calculate_all_metrics()` to include new metric
3. Update visualizations and reports as needed

### Adding New Visualizations

1. Add method to `PerformanceVisualizer` class
2. Call from `create_all_charts()`
3. Update report to reference new chart

### Adding New Export Formats

1. Add export method to `ResultExporter` class
2. Call from main script

## Testing Strategy

```
tests/
├── bots/
│   └── test_all_bots.py       # Unit tests for each bot
├── integration/
│   └── test_integration.py    # Integration tests
└── conftest.py                # Test fixtures
```

### Test Coverage

- **Unit Tests**: Each bot initialization and signal generation
- **Integration Tests**: Complete workflow from backtest to export
- **Fixtures**: Reusable test data (OHLCV, configuration)

## Performance Considerations

1. **Vectorized Operations**: Uses pandas for efficient data manipulation
2. **Lazy Evaluation**: Generates visualizations only when needed
3. **Memory Management**: Streams large results to disk
4. **Parallel Potential**: Architecture supports parallelizing bot backtests

## Security Considerations

1. **API Keys**: Stored in config.json (gitignored)
2. **Input Validation**: Configuration validated before use
3. **Safe Defaults**: Uses testnet by default
4. **No Credentials in Code**: All secrets externalized

## Configuration Management

```json
{
  "delta_exchange": {
    "api_key": "...",
    "api_secret": "...",
    "testnet": true
  },
  "backtest_settings": {
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "initial_capital": 10000,
    "symbols": ["BTCUSDT", "ETHUSDT"],
    "timeframe": "1h"
  },
  "performance_metrics": {
    "risk_free_rate": 0.02
  }
}
```

## Error Handling

- Configuration errors: Fallback to example config
- API errors: Synthetic data generation
- Calculation errors: Graceful degradation with warnings
- File I/O errors: Clear error messages

## Future Enhancements

Potential areas for expansion:

1. **Live Trading**: Add paper trading and live execution
2. **Optimization**: Hyperparameter tuning for strategies
3. **Walk-Forward Analysis**: More robust backtesting
4. **Machine Learning**: ML-based strategy bots
5. **Web Interface**: Dashboard for real-time monitoring
6. **Database Integration**: Store results in database
7. **Parallel Processing**: Distribute backtests across cores
8. **Custom Indicators**: Library of technical indicators
9. **Risk Management**: Position sizing and stop-loss
10. **Portfolio Analysis**: Multi-asset portfolio optimization

---

This architecture provides a solid foundation for comparing trading strategies while remaining flexible and extensible for future enhancements.

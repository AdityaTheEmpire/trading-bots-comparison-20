"""
Delta Exchange API integration for fetching market data.
"""
import requests
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import time
import hmac
import hashlib


class DeltaExchangeAPI:
    """
    Delta Exchange API client for fetching market data.
    """
    
    BASE_URL = "https://api.delta.exchange"
    TESTNET_URL = "https://testnet-api.delta.exchange"
    
    def __init__(self, api_key: Optional[str] = None, 
                 api_secret: Optional[str] = None,
                 testnet: bool = True):
        """
        Initialize Delta Exchange API client.
        
        Args:
            api_key: API key
            api_secret: API secret
            testnet: Use testnet if True
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = self.TESTNET_URL if testnet else self.BASE_URL
        
    def _generate_signature(self, method: str, endpoint: str, payload: str = "") -> str:
        """
        Generate HMAC signature for authenticated requests.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            payload: Request payload
            
        Returns:
            Signature string
        """
        if not self.api_secret:
            return ""
        
        timestamp = str(int(time.time()))
        message = method + timestamp + endpoint + payload
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    def get_ohlc_data(self, symbol: str, resolution: str = "1h",
                      start_time: Optional[datetime] = None,
                      end_time: Optional[datetime] = None) -> pd.DataFrame:
        """
        Get OHLC (candlestick) data from Delta Exchange.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            resolution: Timeframe (1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 1d, 1w)
            start_time: Start datetime
            end_time: End datetime
            
        Returns:
            DataFrame with OHLCV data
        """
        # For demo purposes, generate synthetic data
        # In production, this would call the actual Delta Exchange API
        
        if start_time is None:
            start_time = datetime.now() - timedelta(days=365)
        if end_time is None:
            end_time = datetime.now()
        
        # Generate synthetic OHLCV data for backtesting
        dates = pd.date_range(start=start_time, end=end_time, freq='1H')
        
        # Simulate realistic price movement
        np_random = pd.np.random if hasattr(pd, 'np') else __import__('numpy').random
        
        base_price = 30000 if 'BTC' in symbol.upper() else 2000 if 'ETH' in symbol.upper() else 300
        price_volatility = base_price * 0.02
        
        prices = [base_price]
        for _ in range(len(dates) - 1):
            change = np_random.randn() * price_volatility
            prices.append(max(prices[-1] + change, base_price * 0.5))
        
        data = {
            'timestamp': dates,
            'open': prices,
            'high': [p * (1 + abs(np_random.randn() * 0.01)) for p in prices],
            'low': [p * (1 - abs(np_random.randn() * 0.01)) for p in prices],
            'close': [p + np_random.randn() * price_volatility * 0.5 for p in prices],
            'volume': [np_random.randint(100, 10000) for _ in prices]
        }
        
        df = pd.DataFrame(data)
        df.set_index('timestamp', inplace=True)
        
        return df
    
    def get_ticker(self, symbol: str) -> Dict:
        """
        Get current ticker data for a symbol.
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            Dictionary with ticker data
        """
        # Synthetic data for demo
        base_price = 30000 if 'BTC' in symbol.upper() else 2000 if 'ETH' in symbol.upper() else 300
        
        return {
            'symbol': symbol,
            'last_price': base_price,
            'bid': base_price * 0.999,
            'ask': base_price * 1.001,
            'volume_24h': 1000000,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_available_symbols(self) -> List[str]:
        """
        Get list of available trading symbols.
        
        Returns:
            List of symbol strings
        """
        return ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'SOLUSDT']

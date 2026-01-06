"""
Export utilities for saving results in various formats.
"""
import json
import csv
import pandas as pd
from typing import Dict, List
import os


class ResultExporter:
    """
    Export backtest results to various formats.
    """
    
    def __init__(self, output_dir: str = "results"):
        """
        Initialize exporter.
        
        Args:
            output_dir: Directory to save results
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def export_to_json(self, results: List[Dict], filename: str = "results.json") -> str:
        """
        Export results to JSON format.
        
        Args:
            results: List of result dictionaries
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        filepath = os.path.join(self.output_dir, filename)
        
        # Convert to serializable format
        serializable_results = []
        for result in results:
            result_copy = result.copy()
            # Remove non-serializable items
            if 'trades_detail' in result_copy:
                trades = result_copy['trades_detail']
                serializable_trades = []
                for trade in trades:
                    trade_copy = trade.copy()
                    if 'timestamp' in trade_copy:
                        trade_copy['timestamp'] = str(trade_copy['timestamp'])
                    serializable_trades.append(trade_copy)
                result_copy['trades_detail'] = serializable_trades
            
            serializable_results.append(result_copy)
        
        with open(filepath, 'w') as f:
            json.dump(serializable_results, f, indent=2, default=str)
        
        print(f"Results exported to JSON: {filepath}")
        return filepath
    
    def export_to_csv(self, df: pd.DataFrame, filename: str = "results.csv") -> str:
        """
        Export results to CSV format.
        
        Args:
            df: DataFrame with results
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        filepath = os.path.join(self.output_dir, filename)
        df.to_csv(filepath, index=False)
        
        print(f"Results exported to CSV: {filepath}")
        return filepath
    
    def export_aggregated_results(self, df: pd.DataFrame, 
                                  json_filename: str = "aggregated_results.json",
                                  csv_filename: str = "aggregated_results.csv"):
        """
        Export aggregated results in both JSON and CSV.
        
        Args:
            df: DataFrame with aggregated results
            json_filename: JSON output filename
            csv_filename: CSV output filename
        """
        # Export to CSV
        self.export_to_csv(df, csv_filename)
        
        # Export to JSON
        results_dict = df.to_dict(orient='records')
        self.export_to_json(results_dict, json_filename)
    
    def export_detailed_trades(self, results: List[Dict], 
                              filename: str = "detailed_trades.json") -> str:
        """
        Export detailed trade information.
        
        Args:
            results: List of result dictionaries
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        filepath = os.path.join(self.output_dir, filename)
        
        trades_by_bot = {}
        for result in results:
            bot_name = result.get('bot_name', 'Unknown')
            symbol = result.get('symbol', 'Unknown')
            trades = result.get('trades_detail', [])
            
            key = f"{bot_name}_{symbol}"
            trades_by_bot[key] = [
                {k: str(v) if k == 'timestamp' else v for k, v in trade.items()}
                for trade in trades
            ]
        
        with open(filepath, 'w') as f:
            json.dump(trades_by_bot, f, indent=2, default=str)
        
        print(f"Detailed trades exported: {filepath}")
        return filepath

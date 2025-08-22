"""
Data loading utilities for jailbreak research datasets
"""

import os
import pandas as pd
from datasets import load_dataset
from typing import Dict, List, Optional
import logging

class JailbreakDataLoader:
    """Load and manage jailbreak research datasets"""
    
    def __init__(self, cache_dir: str = "./data/cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
    def load_jailbreak_bench(self, split: str = "behaviors") -> Dict:
        """Load JailbreakBench dataset
        
        Args:
            split: 'behaviors' for harmful or 'benign' for benign
            
        Returns:
            Dictionary with dataset contents
        """
        try:
            dataset = load_dataset(
                "JailbreakBench/JBB-Behaviors", 
                split, 
                cache_dir=self.cache_dir
            )
            return {
                'data': dataset['train'],
                'size': len(dataset['train']),
                'source': 'JailbreakBench'
            }
        except Exception as e:
            logging.error(f"Failed to load JailbreakBench: {e}")
            return None
    
    def load_advbench(self) -> Dict:
        """Load AdvBench dataset"""
        try:
            dataset = load_dataset(
                "walledai/AdvBench",
                cache_dir=self.cache_dir
            )
            return {
                'data': dataset['train'],
                'size': len(dataset['train']),
                'source': 'AdvBench'
            }
        except Exception as e:
            logging.error(f"Failed to load AdvBench: {e}")
            return None
    
    def load_strongreject(self) -> Dict:
        """Load StrongREJECT dataset"""
        try:
            dataset = load_dataset(
                "alexandreteles/strongreject",
                cache_dir=self.cache_dir
            )
            return {
                'data': dataset['train'],
                'size': len(dataset['train']),
                'source': 'StrongREJECT'
            }
        except Exception as e:
            logging.error(f"Failed to load StrongREJECT: {e}")
            return None
    
    def get_combined_dataset(self, sources: List[str] = None) -> pd.DataFrame:
        """Combine multiple datasets for evaluation
        
        Args:
            sources: List of dataset names to combine
            
        Returns:
            Combined pandas DataFrame
        """
        if sources is None:
            sources = ['jailbreak_bench', 'advbench']
        
        combined_data = []
        
        for source in sources:
            if source == 'jailbreak_bench':
                data = self.load_jailbreak_bench()
                if data:
                    df = pd.DataFrame(data['data'])
                    df['source'] = 'JailbreakBench'
                    combined_data.append(df)
            
            elif source == 'advbench':
                data = self.load_advbench()
                if data:
                    df = pd.DataFrame(data['data'])
                    df['source'] = 'AdvBench'
                    combined_data.append(df)
            
            elif source == 'strongreject':
                data = self.load_strongreject()
                if data:
                    df = pd.DataFrame(data['data'])
                    df['source'] = 'StrongREJECT'
                    combined_data.append(df)
        
        if combined_data:
            return pd.concat(combined_data, ignore_index=True)
        else:
            return pd.DataFrame()
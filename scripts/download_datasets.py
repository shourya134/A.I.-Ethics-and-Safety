#!/usr/bin/env python3
"""
Download and cache all supported datasets for jailbreak research
"""

import argparse
import logging
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.datasets.data_loader import JailbreakDataLoader
from src.utils.logging_utils import setup_logging

def main():
    parser = argparse.ArgumentParser(description="Download jailbreak research datasets")
    parser.add_argument("--cache-dir", default="./data/cache", 
                       help="Directory to cache datasets")
    parser.add_argument("--datasets", nargs="+", 
                       default=["jailbreak_bench", "advbench", "strongreject"],
                       help="Datasets to download")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose logging")
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(verbose=args.verbose)
    
    # Initialize data loader
    loader = JailbreakDataLoader(cache_dir=args.cache_dir)
    
    # Download datasets
    for dataset_name in args.datasets:
        logging.info(f"Downloading {dataset_name}...")
        
        try:
            if dataset_name == "jailbreak_bench":
                # Download both harmful and benign
                harmful = loader.load_jailbreak_bench("behaviors")
                benign = loader.load_jailbreak_bench("benign")
                if harmful and benign:
                    logging.info(f"✓ JailbreakBench: {harmful['size']} harmful + {benign['size']} benign")
                
            elif dataset_name == "advbench":
                data = loader.load_advbench()
                if data:
                    logging.info(f"✓ AdvBench: {data['size']} examples")
                
            elif dataset_name == "strongreject":
                data = loader.load_strongreject()
                if data:
                    logging.info(f"✓ StrongREJECT: {data['size']} examples")
                    
        except Exception as e:
            logging.error(f"✗ Failed to download {dataset_name}: {e}")
    
    logging.info("Dataset download complete!")

if __name__ == "__main__":
    main()
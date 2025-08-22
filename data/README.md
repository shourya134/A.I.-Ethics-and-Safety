# Data Directory

This directory contains datasets and examples for jailbreak research.

## Structure

- `raw/`: Original, unprocessed datasets
- `processed/`: Cleaned and preprocessed data
- `examples/`: Example jailbreak attempts and demonstrations
- `cache/`: Cached datasets from Hugging Face and other sources

## Datasets

Supported datasets include:
- JailbreakBench: Harmful and benign behavior examples
- AdvBench: Adversarial behavior collection
- StrongREJECT: Refusal evaluation prompts
- HarmBench: Comprehensive test cases

## Usage

Use the data loader to access datasets:

```python
from src.datasets import JailbreakDataLoader

loader = JailbreakDataLoader()
data = loader.load_jailbreak_bench()
```

## Security Note

All data in this directory should be handled according to our Ethics Guidelines. Harmful examples are for research purposes only.
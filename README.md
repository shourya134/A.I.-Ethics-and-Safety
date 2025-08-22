#  AI Safety Jailbreak Research Project

A comprehensive framework for researching and defending against jailbreak attacks on large language models.

##  Project Overview

This repository provides tools and methodologies for:
- **Detection**: Identifying various jailbreak attack patterns
- **Analysis**: Understanding attack mechanisms and success factors  
- **Defense**: Developing and evaluating countermeasures
- **Evaluation**: Benchmarking defense effectiveness

##  Quick Start

### Installation

```bash
git clone https://github.com/yourusername/ai-safety-jailbreak-research.git
cd ai-safety-jailbreak-research
pip install -e .
```

### Download Datasets

```bash
python scripts/download_datasets.py
```

### Run Basic Detection

```python
from src.detectors import PromptLevelDetector
from src.datasets import JailbreakDataLoader

# Load data
loader = JailbreakDataLoader()
data = loader.load_jailbreak_bench()

# Initialize detector
detector = PromptLevelDetector()

# Detect jailbreak attempts
for prompt in data['data']:
    result = detector.detect(prompt['goal'])
    print(f"Risk Level: {result['risk_level']}")
```

## Supported Datasets

- **JailbreakBench**: 100 harmful + 100 benign behaviors
- **AdvBench**: 520 harmful behaviors  
- **HarmBench**: 400 comprehensive test cases
- **StrongREJECT**: 313 refusal evaluation prompts

##  Detection Methods

### Prompt-Level Attacks
- Roleplay scenario detection
- Obfuscation pattern recognition
- DAN-style prompt identification

### Multi-Turn Attacks  
- Crescendo attack detection
- Conversation flow analysis
- Many-shot pattern recognition

### Token-Level Attacks
- GCG suffix detection
- Perplexity-based filtering
- JailMine pattern analysis

### Indirect Attacks
- Prompt injection scanning
- Content sanitization
- Source validation

##  Evaluation Metrics

- **Attack Success Rate (ASR)**: Percentage of successful jailbreaks
- **False Positive Rate**: Benign prompts incorrectly flagged
- **Detection Latency**: Time to identify threats
- **Robustness Score**: Performance across attack variations

##  Ethics & Safety

This research is conducted for defensive purposes only. Please review our [Ethics Guidelines](ETHICS.md) before contributing.

## =� License

MIT License - see [LICENSE](LICENSE) file for details.

##  Contributing

Please read [CONTRIBUTING.md](docs/contributing.md) for guidelines.

##  Citation

If you use this framework in your research, please cite:

```bibtex
@misc{ai-safety-jailbreak-research,
  title={AI Safety Jailbreak Research Framework},
  author={Your Name},
  year={2025},
  url={https://github.com/yourusername/ai-safety-jailbreak-research}
}
```
🧠 LLM Evaluation Toolkit

A modular, configurable Python toolkit for evaluating Large Language Model (LLM) outputs across multiple dimensions. Designed for researchers, developers, and product teams who need systematic, reproducible LLM evaluation.






✨ Features

Multi-metric Evaluation: Exact match, fuzzy match, keyword match, semantic similarity

Customisable: Configure metrics, weights, and thresholds via YAML/JSON

Batch Processing: Evaluate multiple LLM outputs at once

Report Generation: Automatically generate markdown reports with summaries and examples

Extensible: Easy to add custom evaluation metrics

Synthetic Data: Built-in dataset generation for testing

📋 Quick Start
Installation
# Clone the repository
git clone https://github.com/SamAde1203/llm-evaluation-toolkit.git
cd llm-evaluation-toolkit

# Install dependencies
pip install -r requirements.txt

Basic Usage
from llm_eval.evaluator import LLMEvaluator

# Sample data
predictions = [
    "The capital of France is Paris.",
    "Water boils at 100°C."
]

references = [
    "Paris is the capital of France.",
    "Water boils at 100 degrees Celsius."
]

# Initialize and run evaluation
evaluator = LLMEvaluator()
results = evaluator.evaluate_batch(predictions, references)

# Print summary
evaluator.print_summary()

# Save results
evaluator.save_results(results, "results/evaluation.json")

Run Examples
# Quick demo
python examples/demo.py

# Comprehensive demo with report generation
python examples/comprehensive_demo.py

📊 Evaluation Metrics
Metric	Description	Use Case
Exact Match	Strict string equality (with normalisation)	Fact-checking, exact answers
Fuzzy Match	Levenshtein-based similarity	Typos, minor variations
Keyword Match	Presence/coverage of key factual words	Factual completeness
Semantic Similarity	Cosine similarity of sentence embeddings	Paraphrasing, semantic equivalence

🏗️ Project Structure
llm-evaluation-toolkit/
│
├── README.md                 # Main documentation  
├── CONTRIBUTING.md           # How to contribute  
├── CODE_OF_CONDUCT.md        # Community guidelines  
├── LICENSE                   # MIT License  
├── requirements.txt          # Python dependencies  
├── setup.py / pyproject.toml # Package configuration  
│
├── .github/                  # GitHub workflows & templates  
│   ├── workflows/            # CI/CD (unit tests)  
│   └── ISSUE_TEMPLATE/       # Bug/feature templates  
│
├── configs/                  # YAML configs  
│   ├── default.yaml  
│   └── advanced_config.yaml  
│
├── src/                      # Source code  
│   ├── metrics/              # Metric modules  
│   ├── evaluator.py          # Evaluation engine  
│   ├── datasets.py           # Dataset loader  
│   ├── config.py             # Config manager  
│   ├── utils.py              # Helpers  
│   └── __main__.py           # CLI entrypoint  
│
├── examples/                 # Example scripts and notebooks  
├── tests/                    # Unit & integration tests  
├── data/                     # Sample datasets and results  
├── reports/                  # Generated reports & charts  
├── docs/                     # API docs & images  
├── notebooks/                # Jupyter notebooks  
└── scripts/                  # Automation tools  


🔧 Advanced Configuration
Create a config.yaml file:
metrics:
  exact_match:
    enabled: true
    normalize: true

  fuzzy_match:
    enabled: true
    threshold: 0.7

  keyword_match:
    enabled: true

  semantic_similarity:
    enabled: true
    model_name: "all-MiniLM-L6-v2"

weights:
  exact_match: 0.3
  fuzzy_match: 0.2
  keyword_match: 0.2
  semantic_similarity: 0.3

output:
  save_results: true
  output_dir: "data/results/"
  generate_report: true

Load configuration in Python
from llm_eval.config import EvaluationConfig
from llm_eval.evaluator import LLMEvaluator

config = EvaluationConfig("config.yaml")
evaluator = LLMEvaluator(config.get_metrics_config())

📈 Sample Output
Console Summary
LLM EVALUATION SUMMARY
========================================
Total Samples: 8
Metrics Used: exact_match, fuzzy_match, keyword_match, semantic_similarity

AGGREGATE SCORES:
----------------------------------------
semantic_similarity : 0.810 (±0.209)
keyword_match       : 0.473 (±0.248)
exact_match         : 0.000 (±0.000)
fuzzy_match         : 0.125 (±0.331)
overall             : 0.363 (±0.147)

Generated Report Includes:

Aggregate statistics

Sample-level breakdowns

Top/bottom-performing samples

Configuration snapshot

Metrics used

Reports are saved in the reports/ folder.

🧪 Testing
# Run all unit tests
python -m pytest tests/

# Run a specific test file
python tests/test_metrics.py

🔮 Roadmap

LLM-as-judge evaluation (GPT-4, Claude, etc.)

BLEU, ROUGE, METEOR metrics

Toxicity / safety detection

Web dashboard interface

API endpoints for remote evaluation

Integration with LLM frameworks (LangChain, LlamaIndex)

🤝 Contributing

Contributions are welcome!

Fork the repository

Create a feature branch:

git checkout -b feature/amazing-feature


Commit your changes:

git commit -m "Add amazing feature"


Push to the branch:

git push origin feature/amazing-feature


Open a Pull Request

📄 License

This project is licensed under the MIT License — see the LICENSE file.

🙏 Acknowledgements

SentenceTransformers

scikit-learn

Matplotlib / Seaborn (if visualisation enabled)

📚 Citation
@software{llm_evaluation_toolkit,
  title  = {LLM Evaluation Toolkit},
  author = {Adeyemi, Sam},
  year   = {2025},
  url    = {https://github.com/SamAde1203/llm-evaluation-toolkit}
}


Built with ❤️ for the LLM research and engineering community.

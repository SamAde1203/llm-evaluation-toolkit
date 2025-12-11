# 🧠 LLM Evaluation Toolkit

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)











A modular, extensible, and reproducible framework for evaluating Large Language Models (LLMs) using multiple metrics, configurable pipelines, and automated reporting — built for AI researchers, ML engineers, AI safety teams, and product teams who require reliable evaluation at scale.

🚀 Why This Toolkit?

Evaluating LLM outputs is one of the hardest problems in AI:

Different LLMs hallucinate, paraphrase, compress, or omit details

Classic metrics like BLEU/ROUGE fail to capture meaning

Different evaluators produce inconsistent results

Teams often rely on ad-hoc scripts that cannot be reproduced

The LLM Evaluation Toolkit provides:

✔ A standardised evaluation pipeline
✔ Multiple metrics for semantic + factual evaluation
✔ Full YAML-based configuration
✔ Detailed Markdown reports + visualisations
✔ Reproducible scoring logic suitable for research and production
✔ Lightweight integration with any LLM (GPT-4/Claude/Gemini/Llama/etc.)

This is the kind of framework used internally by OpenAI, Anthropic, DeepMind, Scale AI, and research labs — now available in an open-source form.

✨ Features
🔍 Multi-Metric Evaluation

Exact Match

Fuzzy Matching (Levenshtein-based)

Keyword Coverage

Semantic Similarity (SentenceTransformers embeddings)

⚙️ Configurable Pipeline

YAML/JSON configs

Adjustable metric weights

Threshold controls

Model selection for semantic similarity

📊 Automated Report Generation

Markdown reports

Score breakdowns

Metric summaries

Visualisations (heatmaps, score histograms, etc.)

🧱 Extensible Architecture

Add your own evaluation metric in minutes.

🧪 Dataset Tools

JSON/CSV dataset loaders

Synthetic dataset generation for experiments

🛠️ Installation
# Clone the repository
git clone https://github.com/SamAde1203/llm-evaluation-toolkit.git
cd llm-evaluation-toolkit

# Install dependencies
pip install -r requirements.txt

⚡ Quick Start
from llm_eval.evaluator import LLMEvaluator

predictions = [
    "The capital of France is Paris.",
    "Water boils at 100°C."
]

references = [
    "Paris is the capital of France.",
    "Water boils at 100 degrees Celsius."
]

# Initialize evaluator
evaluator = LLMEvaluator()

# Evaluate batch
results = evaluator.evaluate_batch(predictions, references)

# Print summary
evaluator.print_summary()

# Save results
evaluator.save_results(results, "data/results/evaluation.json")

📊 Evaluation Metrics
Metric	Description	Best For
Exact Match	Normalised string comparison	Factual Q&A
Fuzzy Match	Levenshtein similarity score	Typos / near-matches
Keyword Match	Factual token coverage	Content completeness
Semantic Similarity	Embedding-based cosine similarity	Paraphrasing, meaning
🏗️ Project Structure
llm-evaluation-toolkit/
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE
│
├── configs/
│   ├── default.yaml
│   └── advanced_config.yaml
│
├── src/
│   ├── evaluator.py
│   ├── datasets.py
│   ├── config.py
│   ├── utils.py
│   └── metrics/
│       ├── correctness.py
│       ├── relevance.py
│       └── safety.py
│
├── examples/
│   ├── demo.py
│   ├── comprehensive_demo.py
│   ├── quickstart.ipynb
│   └── custom_metrics.py
│
├── tests/
│   ├── test_metrics.py
│   ├── test_evaluator.py
│   └── test_datasets.py
│
├── docs/images/
│   └── project_structure.png
│
├── reports/
└── data/

🧩 Advanced Configuration (YAML)
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

🧠 System Architecture

<<<<<<< HEAD
![Project Structure](docs/images/project_structure.png)
=======
(Replace with a full architecture diagram if desired — I can generate one.)
>>>>>>> 4cacce4 (docs: rewrite README into world-class documentation)

📈 Sample Output
Console Summary
Total Samples: 8
Metrics Used: exact_match, fuzzy_match, keyword_match, semantic_similarity

AGGREGATE SCORES:
semantic_similarity : 0.810 (±0.209)
keyword_match       : 0.473 (±0.248)
exact_match         : 0.000
fuzzy_match         : 0.125
overall             : 0.363

Example Visualisation

🧪 Running Tests
python -m pytest tests/

🔮 Roadmap
Planned Enhancements:

LLM-as-Judge evaluation (GPT-4 / Claude / Gemini)

BLEU / ROUGE / METEOR support

Toxicity & safety signal detection

Web dashboard UI

API endpoints for cloud-based evaluation

HuggingFace integration

Model benchmarking suite

Want to contribute? PRs are welcome!

🤝 Contributing

We welcome contributions of all kinds.
See CONTRIBUTING.md for guidelines.

📄 License

This project is licensed under the MIT License.
You are free to use, modify, and distribute it.

📚 Citation
@software{llm_evaluation_toolkit,
  title  = {LLM Evaluation Toolkit},
  author = {Adeyemi, Sam},
  year   = {2025},
  url    = {https://github.com/SamAde1203/llm-evaluation-toolkit}
}

❤️ Built for the AI Research & Engineering Community

This toolkit exists to make LLM evaluation transparent, reproducible, and scientifically rigorous — empowering anyone to build safer, more reliable AI systems.

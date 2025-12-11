import sys
sys.path.append('.')

from src.evaluator import LLMEvaluator
from src.metrics.correctness import CorrectnessMetrics
from src.metrics.relevance import RelevanceMetrics

# Test the exact match function directly
print("=== Testing Exact Match ===")
test_cases = [
    ("Paris", "Paris"),
    ("Paris", "paris"),
    (" Paris ", "Paris"),
    ("The capital is Paris", "Paris is the capital"),
]

for pred, ref in test_cases:
    score = CorrectnessMetrics.exact_match(pred, ref)
    print(f"'{pred}' vs '{ref}': {score}")

print("\n=== Testing Fuzzy Match ===")
for pred, ref in test_cases:
    score = CorrectnessMetrics.fuzzy_match(pred, ref, threshold=0.7)
    print(f"'{pred}' vs '{ref}': {score}")

print("\n=== Testing Semantic Similarity ===")
relevance = RelevanceMetrics()
for pred, ref in test_cases:
    score = relevance.semantic_similarity(pred, ref)
    print(f"'{pred}' vs '{ref}': {score:.3f}")
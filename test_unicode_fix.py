import sys
sys.path.append('.')

from src.evaluator import LLMEvaluator

# Test with Unicode characters
predictions = [
    "The chemical formula for water is H₂O.",
    "The speed of light is 3×10⁸ m/s.",
    "Temperature can reach -40°C in winter."
]

references = [
    "Water is H₂O.",
    "Light speed is 3 x 10^8 meters per second.",
    "Winter temperatures can drop to -40 degrees Celsius."
]

print("Testing Unicode handling...")
evaluator = LLMEvaluator()
results = evaluator.evaluate_batch(predictions, references)

print("\nSaving results with Unicode...")
evaluator.save_results(results, "data/results/unicode_test.json")

print("\nReading back to verify...")
import json
with open("data/results/unicode_test.json", 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(f"Successfully read {len(data['per_sample'])} samples with Unicode")

print("\nUnicode test passed!")
# run_eval.py in project root
from src.evaluator import LLMEvaluator

def main():
    # Sample data
    predictions = [
        "The capital of France is Paris.",
        "Water boils at 100 degrees Celsius at sea level.",
        "The moon is made of green cheese."
    ]
    
    references = [
        "Paris is the capital of France.",
        "Water boils at 100°C at standard atmospheric pressure.",
        "The moon is composed primarily of silicate minerals."
    ]
    
    # Initialize evaluator
    evaluator = LLMEvaluator()
    
    # Run evaluation
    results = evaluator.evaluator_batch(predictions, references)
    
    print("Aggregate Results:")
    for key, value in results['aggregate'].items():
        print(f"  {key}: {value:.3f}")
    
    # Save results
    evaluator.save_results(results, "data/results/eval_results.json")

if __name__ == "__main__":
    main()
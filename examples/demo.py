import sys
sys.path.append('.')

from src.evaluator import LLMEvaluator

def main():
    # Better sample data - mix of exact matches and paraphrases
    predictions = [
        "The capital of France is Paris.",
        "Water boils at 100 degrees Celsius at sea level.",
        "The moon is made of green cheese.",  # Wrong answer
        "The Earth orbits the Sun.",  # Correct
        "Python is a compiled language."  # Partially correct (it's interpreted)
    ]
    
    references = [
        "Paris is the capital of France.",  # Paraphrase
        "Water boils at 100°C at sea level.",  # Nearly exact
        "The Moon is composed of rock and dust.",  # Correct answer
        "Earth revolves around the Sun.",  # Paraphrase
        "Python is an interpreted, high-level programming language."  # More detailed
    ]
    
    sample_ids = ["france_capital", "water_boiling", "moon_composition", 
                  "earth_orbit", "python_language"]
    
    print("Initializing LLM Evaluator...")
    evaluator = LLMEvaluator()
    
    print("\nRunning evaluation on 5 samples...")
    results = evaluator.evaluate_batch(predictions, references, sample_ids)
    
    # Print nice summary
    evaluator.print_summary()
    
    # Save results
    evaluator.save_results(results, "data/results/eval_results.json")
    
    # Show per-sample scores
    print("\nDETAILED PER-SAMPLE SCORES:")
    print("-" * 60)
    for sample in results['per_sample']:
        print(f"\nID: {sample['sample_id']}")
        print(f"Prediction: {sample['prediction']}")
        print(f"Reference:  {sample['reference']}")
        for metric, score in sample['scores'].items():
            print(f"  {metric:20s}: {score:.3f}")

if __name__ == "__main__":
    main()
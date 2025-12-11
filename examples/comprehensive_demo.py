import sys
sys.path.append('.')

from src.evaluator import LLMEvaluator
from src.datasets import DatasetLoader
from src.config import EvaluationConfig
from reports.report_generator import ReportGenerator
import traceback

def main():
    print("=" * 70)
    print("LLM EVALUATION TOOLKIT - COMPREHENSIVE DEMO")
    print("=" * 70)
    
    try:
        # 1. Load or create dataset
        print("\n1. Loading dataset...")
        dataset = DatasetLoader.create_qa_dataset(num_samples=8)
        
        # Extract questions and reference answers
        questions = [item['question'] for item in dataset]
        references = [item['reference_answer'] for item in dataset]
        categories = [item['category'] for item in dataset]
        sample_ids = [f"q{i+1}_{cat}" for i, cat in enumerate(categories)]
        
        # 2. Generate synthetic LLM predictions
        print("2. Generating synthetic LLM predictions...")
        predictions = DatasetLoader.generate_llm_predictions(dataset, correctness_level=0.75)
        
        # 3. Initialize evaluator with configuration
        print("3. Initializing evaluator...")
        config = EvaluationConfig()
        evaluator = LLMEvaluator(config.get_metrics_config())
        
        # 4. Run evaluation
        print("4. Running evaluation...")
        results = evaluator.evaluate_batch(predictions, references, sample_ids)
        
        # 5. Print summary
        print("\n" + "=" * 70)
        evaluator.print_summary()
        
        # 6. Save results
        evaluator.save_results(results, "data/results/comprehensive_eval.json")
        
        # 7. Generate report
        print("\n5. Generating comprehensive report...")
        try:
            report_gen = ReportGenerator(results)
            report_content = report_gen.generate_markdown_report()
            print("   Report generated successfully!")
        except Exception as e:
            print(f"   Warning: Could not generate full report: {e}")
            print("   Continuing with basic results...")
        
        # 8. Show sample of predictions vs references
        print("\n6. Sample Comparisons:")
        print("-" * 70)
        for i in range(min(3, len(dataset))):
            print(f"\nQuestion: {questions[i]}")
            print(f"Reference: {references[i]}")
            print(f"LLM Prediction: {predictions[i]}")
            print(f"Overall Score: {results['per_sample'][i]['scores']['overall_score']:.3f}")
        
        print("\n" + "=" * 70)
        print("DEMO COMPLETE!")
        print("✓ Results saved to 'data/results/comprehensive_eval.json'")
        if 'report_gen' in locals():
            print("✓ Report generated in 'reports/' folder")
        print("=" * 70)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nTraceback:")
        traceback.print_exc()
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check if data/results directory exists")
        print("3. Try running with: python -c \"import sys; print(sys.getdefaultencoding())\"")
        print("=" * 70)

if __name__ == "__main__":
    main()
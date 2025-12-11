import json
from typing import Dict, List, Any, Optional
from pathlib import Path
import numpy as np
from datetime import datetime

# Import our metrics
from .metrics.correctness import CorrectnessMetrics
from .metrics.relevance import RelevanceMetrics

class LLMEvaluator:
    """
    Main class to orchestrate evaluation of LLM outputs.
    """
    
    def __init__(self, metrics_config: Optional[Dict[str, Any]] = None):
        """
        Initialize evaluator with desired metrics.
        
        Args:
            metrics_config: Dict specifying which metrics to use and their params.
                Example: {
                    'exact_match': {'threshold': 0.8},
                    'semantic_similarity': {'model_name': 'all-MiniLM-L6-v2'}
                }
        """
        self.metrics_config = metrics_config or {
            'exact_match': {'normalize': True},
            'fuzzy_match': {'threshold': 0.7},
            'keyword_match': {},
            'semantic_similarity': {'model_name': 'all-MiniLM-L6-v2'}
        }
        
        # Initialize metric classes
        self.correctness = CorrectnessMetrics()
        self.relevance = RelevanceMetrics(
            model_name=self.metrics_config.get('semantic_similarity', {}).get('model_name', 'all-MiniLM-L6-v2')
        )
        
        self.results = None
    
    def evaluate_single(self, prediction: str, reference: str, sample_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Evaluate a single prediction against a reference.
        """
        results = {
            'sample_id': sample_id,
            'prediction': prediction,
            'reference': reference
        }
        scores = {}
        
        # Exact match
        if 'exact_match' in self.metrics_config:
            config = self.metrics_config['exact_match']
            scores['exact_match'] = self.correctness.exact_match(
                prediction, reference, 
                normalize=config.get('normalize', True)
            )
        
        # Fuzzy match
        if 'fuzzy_match' in self.metrics_config:
            config = self.metrics_config['fuzzy_match']
            scores['fuzzy_match'] = self.correctness.fuzzy_match(
                prediction, reference,
                threshold=config.get('threshold', 0.7)
            )
        
        # Keyword match
        if 'keyword_match' in self.metrics_config:
            scores['keyword_match'] = self.correctness.keyword_match(prediction, reference)
        
        # Semantic similarity
        if 'semantic_similarity' in self.metrics_config:
            scores['semantic_similarity'] = self.relevance.semantic_similarity(prediction, reference)
        
        # Overall score (weighted average)
        weights = {
            'exact_match': 0.3,
            'fuzzy_match': 0.2,
            'keyword_match': 0.2,
            'semantic_similarity': 0.3
        }
        
        valid_scores = {k: v for k, v in scores.items() if k in weights}
        if valid_scores:
            total_weight = sum(weights[k] for k in valid_scores.keys())
            scores['overall_score'] = sum(
                scores[k] * weights[k] for k in valid_scores.keys()
            ) / total_weight
        else:
            scores['overall_score'] = 0.0
        
        results['scores'] = scores
        return results
    
    def evaluate_batch(self, predictions: List[str], references: List[str], 
                      sample_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Evaluate a batch of predictions.
        """
        if len(predictions) != len(references):
            raise ValueError("Predictions and references must have the same length")
        
        if sample_ids is None:
            sample_ids = [f"sample_{i}" for i in range(len(predictions))]
        
        results = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_samples': len(predictions),
                'metrics_used': list(self.metrics_config.keys())
            },
            'per_sample': [],
            'aggregate': {}
        }
        
        # Evaluate each sample
        for i, (pred, ref, sid) in enumerate(zip(predictions, references, sample_ids)):
            sample_result = self.evaluate_single(pred, ref, sid)
            results['per_sample'].append(sample_result)
        
        # Calculate aggregate statistics
        all_metrics = set()
        for sample in results['per_sample']:
            all_metrics.update(sample['scores'].keys())
        
        for metric in all_metrics:
            if metric != 'overall_score':
                metric_scores = [sample['scores'][metric] for sample in results['per_sample']]
                results['aggregate'][f'{metric}_mean'] = float(np.mean(metric_scores))
                results['aggregate'][f'{metric}_std'] = float(np.std(metric_scores))
                results['aggregate'][f'{metric}_min'] = float(np.min(metric_scores))
                results['aggregate'][f'{metric}_max'] = float(np.max(metric_scores))
        
        # Overall scores
        overall_scores = [sample['scores']['overall_score'] for sample in results['per_sample']]
        results['aggregate']['overall_mean'] = float(np.mean(overall_scores))
        results['aggregate']['overall_std'] = float(np.std(overall_scores))
        results['aggregate']['overall_min'] = float(np.min(overall_scores))
        results['aggregate']['overall_max'] = float(np.max(overall_scores))
        
        self.results = results
        return results
    
    def save_results(self, results: Dict[str, Any], output_path: str):
        """
        Save evaluation results to JSON file.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Use UTF-8 encoding
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=lambda x: float(x) if isinstance(x, np.floating) else x)
        
        print(f"Results saved to {output_path}")
    
    def print_summary(self):
        """Print a clean summary of results."""
        if not self.results:
            print("No results available. Run evaluate_batch() first.")
            return
        
        print("=" * 60)
        print("LLM EVALUATION SUMMARY")
        print("=" * 60)
        print(f"Total Samples: {self.results['metadata']['total_samples']}")
        print(f"Metrics Used: {', '.join(self.results['metadata']['metrics_used'])}")
        print("\nAGGREGATE SCORES:")
        print("-" * 40)
        
        for key, value in self.results['aggregate'].items():
            if 'mean' in key:
                metric_name = key.replace('_mean', '')
                print(f"{metric_name:20s}: {value:.3f} "
                      f"(±{self.results['aggregate'].get(f'{metric_name}_std', 0):.3f})")
        
        print("\nTOP PERFORMING SAMPLES:")
        print("-" * 40)
        sorted_samples = sorted(self.results['per_sample'], 
                               key=lambda x: x['scores']['overall_score'], 
                               reverse=True)
        
        for i, sample in enumerate(sorted_samples[:3]):  # Top 3
            print(f"{i+1}. ID: {sample['sample_id']}")
            print(f"   Score: {sample['scores']['overall_score']:.3f}")
            if len(sample['prediction']) > 50:
                print(f"   Prediction: {sample['prediction'][:50]}...")
            else:
                print(f"   Prediction: {sample['prediction']}")
            print()
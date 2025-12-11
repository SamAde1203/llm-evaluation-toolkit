import yaml
import json
from pathlib import Path
from typing import Dict, Any

class EvaluationConfig:
    """Load and manage evaluation configurations."""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_default_config()
        
        if config_path:
            self.load_config(config_path)
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Default configuration."""
        return {
            'metrics': {
                'exact_match': {'enabled': True, 'normalize': True},
                'fuzzy_match': {'enabled': True, 'threshold': 0.7},
                'keyword_match': {'enabled': True},
                'semantic_similarity': {
                    'enabled': True, 
                    'model_name': 'all-MiniLM-L6-v2'
                }
            },
            'weights': {
                'exact_match': 0.3,
                'fuzzy_match': 0.2,
                'keyword_match': 0.2,
                'semantic_similarity': 0.3
            },
            'output': {
                'save_results': True,
                'output_dir': 'data/results',
                'generate_report': True
            }
        }
    
    def load_config(self, config_path: str):
        """Load configuration from YAML or JSON file."""
        path = Path(config_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(path, 'r') as f:
            if path.suffix.lower() == '.yaml' or path.suffix.lower() == '.yml':
                user_config = yaml.safe_load(f)
            else:
                user_config = json.load(f)
        
        # Deep merge with defaults
        self._merge_configs(self.config, user_config)
    
    def _merge_configs(self, default: Dict, user: Dict):
        """Recursively merge user config into default."""
        for key, value in user.items():
            if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                self._merge_configs(default[key], value)
            else:
                default[key] = value
    
    def get_metrics_config(self) -> Dict[str, Any]:
        """Get metrics configuration for evaluator."""
        metrics_config = {}
        for metric_name, metric_config in self.config['metrics'].items():
            if metric_config.get('enabled', True):
                # Remove 'enabled' flag for evaluator
                metric_config_copy = metric_config.copy()
                metric_config_copy.pop('enabled', None)
                metrics_config[metric_name] = metric_config_copy
        
        return metrics_config
    
    def get_weights(self) -> Dict[str, float]:
        """Get weights for score aggregation."""
        return self.config['weights']
    
    def save(self, output_path: str):
        """Save current configuration to file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
        
        print(f"Configuration saved to {output_path}")
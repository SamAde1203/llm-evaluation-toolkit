import Levenshtein
import re
from typing import List, Dict, Any

class CorrectnessMetrics:
    """Metrics for factual correctness against a reference."""
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text for comparison: lowercase, remove extra spaces/punctuation."""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        return text
    
    @staticmethod
    def exact_match(prediction: str, reference: str, normalize: bool = True) -> float:
        """
        Returns 1.0 if prediction exactly matches reference.
        
        Args:
            normalize: If True, normalize text before comparison
        """
        if normalize:
            pred_norm = CorrectnessMetrics.normalize_text(prediction)
            ref_norm = CorrectnessMetrics.normalize_text(reference)
            return 1.0 if pred_norm == ref_norm else 0.0
        else:
            return 1.0 if prediction.strip() == reference.strip() else 0.0
    
    @staticmethod
    def fuzzy_match(prediction: str, reference: str, threshold: float = 0.8) -> float:
        """
        Returns 1.0 if normalized Levenshtein similarity >= threshold.
        """
        pred_norm = CorrectnessMetrics.normalize_text(prediction)
        ref_norm = CorrectnessMetrics.normalize_text(reference)
        
        if len(ref_norm) == 0:
            return 1.0 if len(pred_norm) == 0 else 0.0
        
        distance = Levenshtein.distance(pred_norm, ref_norm)
        similarity = 1 - (distance / max(len(pred_norm), len(ref_norm)))
        
        return 1.0 if similarity >= threshold else 0.0
    
    @staticmethod
    def keyword_match(prediction: str, reference: str, required_keywords: List[str] = None) -> float:
        """
        Check if prediction contains key factual words from reference.
        Returns proportion of required keywords found.
        """
        if required_keywords is None:
            # Auto-extract keywords (simple version: nouns/important words)
            words = set(reference.lower().split())
            # Filter out common words
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
            required_keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        if not required_keywords:
            return 1.0  # No specific keywords to check
        
        pred_lower = prediction.lower()
        matches = sum(1 for keyword in required_keywords if keyword in pred_lower)
        
        return matches / len(required_keywords)
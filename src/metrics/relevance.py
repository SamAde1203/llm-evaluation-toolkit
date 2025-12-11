from sentence_transformers import SentenceTransformer, util
import numpy as np

class RelevanceMetrics:
    """Metrics for semantic relevance, not just lexical overlap."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the sentence transformer model.
        'all-MiniLM-L6-v2' is small but effective for English.
        """
        self.model = SentenceTransformer(model_name)
    
    def semantic_similarity(self, prediction: str, reference: str) -> float:
        """
        Returns cosine similarity between embedding vectors (0 to 1).
        """
        embeddings = self.model.encode([prediction, reference], convert_to_tensor=True)
        similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
        return max(0.0, min(1.0, similarity))  # Clamp to [0, 1]
    
    def batch_semantic_similarity(self, predictions: list, references: list) -> dict:
        """
        Calculate semantic similarity for a batch.
        Returns: {"semantic_similarity": float, "scores": list}
        """
        # Encode all at once for efficiency
        all_texts = predictions + references
        embeddings = self.model.encode(all_texts, convert_to_tensor=True)
        
        pred_embeddings = embeddings[:len(predictions)]
        ref_embeddings = embeddings[len(predictions):]
        
        similarities = util.cos_sim(pred_embeddings, ref_embeddings)
        scores = [similarities[i, i].item() for i in range(len(predictions))]
        
        return {
            "semantic_similarity": np.mean(scores) if scores else 0.0,
            "scores": scores
        }
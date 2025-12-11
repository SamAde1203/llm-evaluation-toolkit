import os

# The corrected datasets.py content
CORRECTED_CONTENT = '''import json
import csv
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Tuple
import random

class DatasetLoader:
    """Load and manage evaluation datasets."""
    
    @staticmethod
    def load_json(file_path: str) -> List[Dict[str, Any]]:
        """Load dataset from JSON file."""
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        if isinstance(data, dict):
            return [data]  # Single sample
        return data
    
    @staticmethod
    def load_csv(file_path: str) -> List[Dict[str, Any]]:
        """Load dataset from CSV file."""
        df = pd.read_csv(file_path)
        return df.to_dict('records')
    
    @staticmethod
    def create_qa_dataset(num_samples: int = 10) -> List[Dict[str, Any]]:
        """Create a synthetic Q&A dataset for testing."""
        qa_pairs = [
            {
                "question": "What is the capital of France?",
                "reference_answer": "Paris is the capital of France.",
                "category": "geography",
                "difficulty": "easy"
            },
            {
                "question": "What is the boiling point of water?",
                "reference_answer": "Water boils at 100°C at sea level.",
                "category": "science",
                "difficulty": "easy"
            },
            {
                "question": "What is the moon made of?",
                "reference_answer": "The Moon is composed of rock, dust, and various minerals.",
                "category": "astronomy",
                "difficulty": "medium"
            },
            {
                "question": "Who wrote \'Romeo and Juliet\'?",
                "reference_answer": "William Shakespeare wrote Romeo and Juliet.",
                "category": "literature",
                "difficulty": "easy"
            },
            {
                "question": "What is the speed of light?",
                "reference_answer": "The speed of light in vacuum is approximately 299,792,458 meters per second.",
                "category": "physics",
                "difficulty": "hard"
            },
            {
                "question": "What is the largest planet in our solar system?",
                "reference_answer": "Jupiter is the largest planet in our solar system.",
                "category": "astronomy",
                "difficulty": "easy"
            },
            {
                "question": "What is the chemical formula for water?",
                "reference_answer": "The chemical formula for water is H₂O.",
                "category": "chemistry",
                "difficulty": "medium"
            },
            {
                "question": "Who painted the Mona Lisa?",
                "reference_answer": "Leonardo da Vinci painted the Mona Lisa.",
                "category": "art",
                "difficulty": "easy"
            },
            {
                "question": "What is the theory of relativity?",
                "reference_answer": "The theory of relativity, developed by Albert Einstein, describes gravity as a curvature of spacetime.",
                "category": "physics",
                "difficulty": "hard"
            },
            {
                "question": "What is photosynthesis?",
                "reference_answer": "Photosynthesis is the process by which plants convert sunlight into chemical energy.",
                "category": "biology",
                "difficulty": "medium"
            }
        ]
        
        # Return requested number of samples
        return qa_pairs[:num_samples]
    
    @staticmethod
    def generate_llm_predictions(dataset: List[Dict[str, Any]], 
                                correctness_level: float = 0.7) -> List[str]:
        """
        Generate synthetic LLM predictions with varying correctness.
        
        Args:
            correctness_level: Probability of correct answer (0.0 to 1.0)
        """
        predictions = []
        
        for item in dataset:
            reference = item[\'reference_answer\']
            
            if random.random() < correctness_level:
                # Generate correct but possibly paraphrased answer
                prediction = DatasetLoader._paraphrase_text(reference)
            else:
                # Generate incorrect answer
                prediction = DatasetLoader._generate_incorrect_answer(item[\'category\'])
            
            predictions.append(prediction)
        
        return predictions
    
    @staticmethod
    def _paraphrase_text(text: str) -> str:
        """Simple paraphrasing for demo purposes."""
        paraphrases = {
            "Paris is the capital of France.": ["The capital of France is Paris.", "France\'s capital city is Paris."],
            "Water boils at 100°C at sea level.": ["At sea level, water boils at 100 degrees Celsius.", "The boiling point of water is 100°C."],
            "The Moon is composed of rock, dust, and various minerals.": ["The Moon is made up of rocks and dust.", "Lunar composition includes rocks, dust, and minerals."],
            "William Shakespeare wrote Romeo and Juliet.": ["Romeo and Juliet was written by William Shakespeare.", "Shakespeare is the author of Romeo and Juliet."],
            "The speed of light in vacuum is approximately 299,792,458 meters per second.": ["Light travels at about 3 x 10^8 m/s in vacuum.", "The speed of light is roughly 300,000 km/s."],
            "Jupiter is the largest planet in our solar system.": ["The largest planet in our solar system is Jupiter.", "Jupiter holds the title of biggest planet in our solar system."],
            "The chemical formula for water is H₂O.": ["Water\'s chemical formula is H₂O.", "H₂O is the formula for water."],
            "Leonardo da Vinci painted the Mona Lisa.": ["The Mona Lisa was painted by Leonardo da Vinci.", "Da Vinci is the artist behind the Mona Lisa."]
        }
        
        # Check for exact match
        if text in paraphrases:
            return random.choice(paraphrases[text])
        
        # Check for substring match (in case of slight variations)
        for original, options in paraphrases.items():
            if original in text or text in original:
                return random.choice(options)
        
        # Default: simple variation without breaking the sentence
        if len(text) > 20:
            sentences = text.split(\'. \')
            if len(sentences) > 1:
                # Reorder sentences
                return \'. \'.join(sentences[1:] + [sentences[0]]) + \'.\'
        
        return text
    
    @staticmethod
    def _generate_incorrect_answer(category: str) -> str:
        """Generate plausible but incorrect answers."""
        incorrect_answers = {
            "geography": ["The capital is London.", "I believe it\'s Berlin.", "Madrid is the capital."],
            "science": ["Water boils at 90°C.", "The boiling point is 110 degrees.", "It depends on the altitude."],
            "astronomy": ["The moon is made of cheese.", "It\'s primarily gaseous.", "Mostly iron and nickel."],
            "literature": ["Charles Dickens wrote it.", "It was Jane Austen.", "Mark Twain authored that play."],
            "physics": ["About 300,000 km/s.", "186,000 miles per second.", "3 x 10^8 m/s exactly."]
        }
        
        return random.choice(incorrect_answers.get(category, ["I don\'t know the answer."]))
'''

# Write the corrected file
with open('src/datasets.py', 'w', encoding='utf-8') as f:
    f.write(CORRECTED_CONTENT)

print("Fixed src/datasets.py with correct indentation!")
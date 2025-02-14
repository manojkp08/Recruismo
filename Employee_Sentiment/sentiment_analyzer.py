from transformers import pipeline
from .utils import extract_themes
from .model_config import THEME_KEYWORDS

class EmployeeSentimentAnalyzer:
    def __init__(self):
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        
    def analyze_feedback(self, feedback_text):
        """Analyze sentiment and extract key themes from feedback"""
        # Get overall sentiment
        sentiment = self.sentiment_analyzer(feedback_text)[0]
        
        # Extract themes
        detected_themes = extract_themes(feedback_text, THEME_KEYWORDS)
        
        return {
            'sentiment': sentiment,
            'themes': detected_themes,
            'risk_score': 1 - sentiment['score'] if sentiment['label'] == 'NEGATIVE' else 0
        }
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Ensure the lexicon is available inside Docker
nltk.download("vader_lexicon")

_sia = SentimentIntensityAnalyzer()

def analyze_text(text: str):
    return _sia.polarity_scores(text)


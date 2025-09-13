from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
import re
import numpy as np
import nltk

try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")


# Initialize once (VADER)
_sentiment_analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str):
    scores = _sentiment_analyzer.polarity_scores(text)
    compound = scores.get("compound", 0.0)
    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    return label, float(compound)

def extract_keywords_bow(questions, top_n=20, stop_words='english'):
    """
    questions: list[str] - corpus
    returns: list of (term, count) sorted desc
    """
    if not questions:
        return []
    # basic cleanup
    cleaned = [re.sub(r"[^\w\s]", " ", q.lower()) for q in questions]
    vectorizer = CountVectorizer(stop_words=stop_words, min_df=1)
    X = vectorizer.fit_transform(cleaned)
    counts = np.asarray(X.sum(axis=0)).ravel()
    terms = vectorizer.get_feature_names_out()
    term_count = list(zip(terms, counts))
    term_count = sorted(term_count, key=lambda x: x[1], reverse=True)
    return term_count[:top_n]

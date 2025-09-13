from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from sklearn.feature_extraction.text import CountVectorizer

# Ensure the lexicon is available
nltk.download("vader_lexicon")

_sia = SentimentIntensityAnalyzer()

# Initialize a vectorizer (for now, single-sentence analysis)
# _vectorizer = CountVectorizer()
# Initialize CountVectorizer with English stop words
_vectorizer = CountVectorizer(stop_words='english')

def analyze_text(text: str):
    """
    Analyzes the input text for sentiment and Bag-of-Words features.
    Returns a dictionary with sentiment scores and BoW vector.
    """
    
    # Sentiment
    sentiment = _sia.polarity_scores(text)

    # BoW
    bow = _vectorizer.fit_transform([text])
    bow_features = _vectorizer.get_feature_names_out()
    bow_counts = bow.toarray()[0]

    bow_dict = {word: int(count) for word, count in zip(bow_features, bow_counts)}

    return {"sentiment": sentiment, "bow": bow_dict}

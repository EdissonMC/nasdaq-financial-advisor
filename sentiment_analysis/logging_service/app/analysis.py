from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob


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
    Subjectivity: Measures the subjectivity of the text. A value close to 1 
    means the text is highly subjective (opinion), while 0 means the text 
    is more objective (factual).
    Returns a dictionary with sentiment scores, BoW vector and Textblob polarities.
    """
    
    # Sentiment
    sentiment = _sia.polarity_scores(text)

    # BoW
    bow = _vectorizer.fit_transform([text])
    bow_features = _vectorizer.get_feature_names_out()
    bow_counts = bow.toarray()[0]

    bow_dict = {word: int(count) for word, count in zip(bow_features, bow_counts)}

    # Subjectivity
    blob = TextBlob(text)
    blob_sentiment = blob.sentiment
    polarity = blob_sentiment.polarity
    subjectivity = blob_sentiment.subjectivity


    return {"sentiment": sentiment, "bow": bow_dict, "blob_polarity": {"polarity": polarity, "subjectivity": subjectivity}}

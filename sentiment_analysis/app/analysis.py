from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob
import os
from openai import OpenAI


# Ensure the lexicon is available
nltk.download("vader_lexicon")

_sia = SentimentIntensityAnalyzer()

# Initialize a vectorizer (for now, single-sentence analysis)
# _vectorizer = CountVectorizer()
# Initialize CountVectorizer with English stop words
_vectorizer = CountVectorizer(stop_words='english')

# Init OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def explain_sentiment_with_llm(text: str, analysis: dict) -> str:
    prompt = f"""
    The following text was analyzed:
    Text: "{text}"
    Sentiment scores: {analysis['sentiment']}
    Bag of Words: {analysis['bow']}
    Polarity & Subjectivity: {analysis['blob_polarity']}
    
    Please provide a short, clear explanation of the sentiment.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content


def analyze_text(text: str, explain_with_llm: bool = False):
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

    result = {
        "text": text,
        "sentiment": sentiment, 
        "bow": bow_dict, 
        "blob_polarity": {"polarity": polarity, "subjectivity": subjectivity}

        }

    # Optional LLM enrichment
    if explain_with_llm:
        analysis_dict = {
            "sentiment": sentiment,
            "bow": bow_dict,
            "blob_polarity": {"polarity": polarity, "subjectivity": subjectivity}
        }
        explanation = explain_sentiment_with_llm(text, analysis_dict)
        result["llm_explanation"] = explanation

    return result

def get_admin_dashboard_data(db: Session):
    analyses = db.query(models.SentimentAnalysis).all()
    
    if not analyses:
        return None

    df = pd.DataFrame([analysis.__dict__ for analysis in analyses])
    
    metrics = schemas.DashboardMetrics(
        avg_positive=df['sentiment_pos'].mean(),
        avg_negative=df['sentiment_neg'].mean(),
        avg_neutral=df['sentiment_neu'].mean(),
        avg_compound=df['sentiment_compound'].mean()
    )
    
    charts = schemas.DashboardChartData(
        sentiment_compound=df['sentiment_compound'].tolist(),
        polarity=df['polarity'].tolist(),
        subjectivity=df['subjectivity'].tolist(),
        created_at=df['created_at'].tolist()
    )

    records = [schemas.SentimentAnalysis.from_orm(analysis) for analysis in analyses]
    
    return schemas.AdminDashboardData(
        records=records,
        metrics=metrics,
        charts=charts
    )
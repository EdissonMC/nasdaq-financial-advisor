import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# API_URL = "http://localhost:8001"  # FastAPI service URL

# When running inside Docker
API_URL = "http://sentiment_api:8001"

st.set_page_config(page_title="Sentiment Analysis Admin", layout="wide")
st.title("📊 Sentiment Analysis Dashboard")

# Fetch data from FastAPI
@st.cache_data
def load_data():
    response = requests.get(f"{API_URL}/analyses")
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("Failed to fetch data from API")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # Show records
    st.subheader("Database Records")
    st.dataframe(df)

    # Metrics
    st.subheader("📈 Summary Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Positive", f"{df['sentiment_pos'].mean():.2f}")
    col2.metric("Avg Negative", f"{df['sentiment_neg'].mean():.2f}")
    col3.metric("Avg Neutral", f"{df['sentiment_neu'].mean():.2f}")
    col4.metric("Avg Compound", f"{df['sentiment_compound'].mean():.2f}")

    # Charts
    st.subheader("📊 Visualizations")

    # Distribution of compound scores
    fig1 = px.histogram(df, x="sentiment_compound", nbins=20, title="Distribution of Compound Sentiment")
    st.plotly_chart(fig1, use_container_width=True)

    # Scatter: polarity vs subjectivity
    fig2 = px.scatter(
        df, x="polarity", y="subjectivity", color="sentiment_compound",
        title="Polarity vs Subjectivity"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Time series (if created_at column exists)
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"])
        fig3 = px.line(df, x="created_at", y="sentiment_compound", title="Sentiment Compound Over Time")
        st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("No records found in database")

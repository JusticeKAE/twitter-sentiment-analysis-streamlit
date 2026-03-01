import streamlit as st
import pickle
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import nltk

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Twitter Sentiment Analysis",
    page_icon="🐦",
    layout="centered"
)

# -----------------------------
# Custom Styling
# -----------------------------
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #1DA1F2;
        }
        .sub-title {
            text-align: center;
            font-size: 18px;
            color: gray;
            margin-bottom: 30px;
        }
        .stButton>button {
            background-color: #1DA1F2;
            color: white;
            border-radius: 8px;
            height: 3em;
            width: 100%;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #0d8ddb;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Download stopwords
# -----------------------------
@st.cache_resource
def load_stopwords():
    nltk.download('stopwords')
    return stopwords.words('english')

# -----------------------------
# Load Model
# -----------------------------
@st.cache_resource
def load_model():
    with open('ensemble_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    return model

# -----------------------------
# Clean + Predict
# -----------------------------
def predict_sentiment(text, model, stop_words):

    text = re.sub(r'[^a-zA-Z]', ' ', text)
    text = text.lower()
    text = text.split()
    text = [word for word in text if word not in stop_words]
    text = ' '.join(text)

    sentiment = model.predict([text])[0]

    return "Positive 😊" if sentiment == 1 else "Negative 😡"

# -----------------------------
# Nitter Scraper
# -----------------------------
def fetch_tweets_nitter(username, limit=5):

    tweets = []
    url = f"https://nitter.net/{username}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception("Nitter instance not reachable")

    soup = BeautifulSoup(response.text, "html.parser")

    tweet_divs = soup.find_all("div", class_="tweet-content")

    for tweet in tweet_divs[:limit]:
        tweets.append(tweet.get_text(strip=True))

    return tweets

# -----------------------------
# Card UI
# -----------------------------
def create_card(tweet_text, sentiment):

    bg_color = "#28a745" if "Positive" in sentiment else "#dc3545"

    return f"""
    <div style="
        background-color: {bg_color};
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        color: white;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    ">
        <h4>{sentiment}</h4>
        <p>{tweet_text}</p>
    </div>
    """

# -----------------------------
# MAIN APP
# -----------------------------
def main():

    st.markdown('<div class="main-title">Twitter Sentiment Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Ensemble Model (TF-IDF + Voting Classifier)</div>', unsafe_allow_html=True)

    stop_words = load_stopwords()
    model = load_model()

    st.divider()

    option = st.selectbox(
        "Choose Analysis Mode",
        ["Input Text", "Get Tweets From User (Nitter)", "Upload CSV Dataset"]
    )

    # ==========================================
    # 1️⃣ INPUT TEXT
    # ==========================================
    if option == "Input Text":

        text_input = st.text_area("Enter text to analyze sentiment")

        if st.button("Analyze Sentiment"):
            if text_input.strip():
                sentiment = predict_sentiment(text_input, model, stop_words)
                st.success(f"Prediction: {sentiment}")
            else:
                st.warning("Please enter some text.")

    # ==========================================
    # 2️⃣ NITTER SCRAPING
    # ==========================================
    elif option == "Get Tweets From User (Nitter)":

        username = st.text_input("Enter Twitter Username (without @)")

        if st.button("Fetch Tweets"):

            if not username.strip():
                st.warning("Please enter a username.")
                return

            with st.spinner("Fetching tweets from Nitter..."):
                try:
                    tweets = fetch_tweets_nitter(username)

                    if tweets:
                        st.success(f"Showing latest tweets from @{username}")

                        for tweet in tweets:
                            sentiment = predict_sentiment(tweet, model, stop_words)
                            card_html = create_card(tweet, sentiment)
                            st.markdown(card_html, unsafe_allow_html=True)
                    else:
                        st.warning("Error fetching tweets:")

                except Exception as e:
                    st.error(f"Error: {e}")

    # ==========================================
    # 3️⃣ CSV UPLOAD
    # ==========================================
    elif option == "Upload CSV Dataset":

        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

        if uploaded_file:

            df = pd.read_csv(uploaded_file)

            st.write("Preview of Dataset:")
            st.dataframe(df.head())

            if "tweet" not in df.columns:
                st.error("CSV must contain a column named 'tweet'")
                return

            if st.button("Analyze Dataset"):

                sentiments = []

                for text in df["tweet"]:
                    sentiments.append(
                        predict_sentiment(str(text), model, stop_words)
                    )

                df["Predicted Sentiment"] = sentiments

                st.success("Analysis Complete")
                st.dataframe(df)

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Download Results",
                    csv,
                    "sentiment_results.csv",
                    "text/csv"
                )

if __name__ == "__main__":
    main()

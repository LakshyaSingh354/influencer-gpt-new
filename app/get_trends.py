import streamlit as st
import openai
import tweepy
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Authenticate Twitter API
bearer_token = os.getenv('TWITTER_BEARER_TOKEN', 'your-twitter-bearer-token')
twitter_client = tweepy.Client(bearer_token)

# Authenticate OpenAI API
openai.api_key = os.getenv('YOUR_OPENAI_API_KEY', '')

def search_trends(topic, source):
    if source == "Twitter":
        trends = twitter_client.search_recent_tweets(query=topic, max_results=10)
        return [trend.text for trend in trends.data] if trends.data else []
    elif source == "GPT":
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a trend generator. Provide the top trends based on the given topic. Give each trend in a new line. Don't repeat the same trend. Don't write introduction and end, only write the trends."
                },
                {
                    "role": "user",
                    "content": f"What are the top trends about {topic}?"
                }
            ]
        )
        # Assuming the response is in newline-separated trends
        trends = completion.choices[0].message["content"].strip().split('\n')
        return trends

def get_trends(query, session_state):
    # Initialization
    if 'trend_engine' not in session_state:
        session_state['trend_engine'] = 'GPT'  # Default trend engine is GPT

    trend_function_choice = session_state['trend_engine']

    st.write(f"Searching {trend_function_choice} for: {query}")

    # Add clear button to reset session state
    if st.button("Clear"):
        st.session_state.clear()  # Correct way to clear the session state

    # Get trends from the selected engine
    trends = search_trends(query, trend_function_choice)

    # Display the trends
    if trends:
        st.write("Top trends found:")
        for trend in trends:
            st.write(f"- {trend}")
    else:
        st.write("No trends found.")

    return trends

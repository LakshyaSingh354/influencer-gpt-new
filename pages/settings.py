import streamlit as st
import json
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Display header and description
st.header("Settings")
st.write("Here you can adjust the settings for the app.")

# Provide option to select Trend Search Engine
st.subheader("Trend Search Engine")
st.session_state['trend_engine'] = st.selectbox(
    "Select Trend Search Engine",
    ("X", "GPT")
)

# Provide option to select Video Generation Engine
st.subheader("Video Generation Engine")
st.session_state['video_engine'] = st.selectbox(
    "Select Video Generation Engine",
    ("D-ID", "Heygen")
)

# Fetch API keys from environment variables, but hide them in the UI
st.subheader("API Key Configurations")
# These keys are securely fetched from environment variables
twitter_bearer_token = os.getenv("TWITTER_BEARER_TOKEN", "")
openai_api_key = os.getenv("YOUR_OPENAI_API_KEY", "")
heygen_api_key = os.getenv("HEYGEN_API_KEY", "")
did_api_key = os.getenv("D_ID_API_KEY", "")
youtube_api_key = os.getenv("YOUTUBE_API_KEY", "")

# Display a message that API keys are loaded, but hide the keys themselves
st.text("API keys are loaded securely. They will not be displayed for privacy.")

# Provide option to select YouTube video category
st.subheader("YouTube Video Category")
st.session_state['YOUTUBE_VIDEO_CATEGORY'] = st.selectbox(
    "Select YouTube Video Category",
    ("Film & Animation", "Autos & Vehicles", "Music", "Pets & Animals", "Sports", "Travel & Events", "Gaming", "People & Blogs", "Comedy", "Entertainment", "News & Politics", "Howto & Style", "Education", "Science & Technology", "Nonprofits & Activism")
)

# Uploaded image for the talking head
uploaded_image = st.file_uploader("Upload an image for the talking head", type=["png", "jpg", "jpeg"])
if uploaded_image is not None:
    with open("uploaded_image.png", "wb") as f:
        f.write(uploaded_image.getbuffer())
    source_url = "uploaded_image.png"
    # Store the last uploaded image in a session variable
    st.session_state['last_uploaded_image'] = "uploaded_image.png"
else:
    # Option to reuse the last uploaded image
    if 'last_uploaded_image' in st.session_state and st.button("Click on the image to reuse it"):
        st.image(st.session_state['last_uploaded_image'])
        source_url = st.session_state['last_uploaded_image']
    else:
        source_url = "https://cdn.discordapp.com/attachments/1116787243634397345/1146111608129597450/hypercubefx_face_like_terminator_bb7255e5-efca-489d-bf9e-9aeb750a6bef.png"

# Save button to persistently save the settings
if st.button("Save Settings"):
    settings_data = {
        'TWITTER_BEARER_TOKEN': twitter_bearer_token,
        'YOUR_OPENAI_API_KEY': openai_api_key,
        'HEYGEN_API_KEY': heygen_api_key,
        'D_ID_API_KEY': did_api_key,
        'YOUTUBE_API_KEY': youtube_api_key,
        'trend_engine': st.session_state['trend_engine'],
        'video_engine': st.session_state['video_engine'],
        'last_uploaded_image': st.session_state.get('last_uploaded_image', '')
    }

    try:
        # Save settings data to a JSON file
        with open("settings.json", "w") as f:
            json.dump(settings_data, f)
        st.success("Settings saved successfully!")
    except Exception as e:
        st.error(f"Error saving settings: {e}")

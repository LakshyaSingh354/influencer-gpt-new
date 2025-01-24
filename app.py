import streamlit as st
import mysql.connector
from mysql.connector import Error
import os
from urllib.parse import urlparse
from app.create_video_script import create_video_script
from app.generate_video import generate_video
from app.get_trends import get_trends
from app.upload_video import upload_video
from app.influencer import generate_influencer_profile, generate_influencer_content, generate_influencer_image

def create_connection():
    try:
        jawsdb_url = os.getenv("JAWSDB_URL")
        if not jawsdb_url:
            st.error("JawsDB URL not found in environment variables.")
            return None

        parsed_url = urlparse(jawsdb_url)
        username = parsed_url.username
        password = parsed_url.password
        hostname = parsed_url.hostname
        port = parsed_url.port
        database = parsed_url.path.lstrip('/')

        connection = mysql.connector.connect(
            host=hostname,
            port=port,
            user=username,
            password=password,
            database=database
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to JawsDB MySQL: {e}")
        return None


def authenticate_user(username, password):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            return result is not None
        except Error as e:
            st.error(f"Error authenticating user: {e}")
    return False


def navigate():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Home", "Get Trends", "Create Video Script", "Generate Video", "Upload Video", "Virtual Influencer", "Logout"]
    )
    return page


def login_register_page():
    st.title("Influencer GPT - Login / Register")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    st.header("Login")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if authenticate_user(login_username, login_password):
            st.session_state.logged_in = True
            st.session_state.username = login_username
            st.success("Logged in successfully!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")

    st.header("New User?")
    st.write("To register, please click the button below:")
    if st.button("Register"):
        register_url = "https://algotradingwalah.in/stripe.php"
        st.markdown(f"[Click here to register]({register_url})", unsafe_allow_html=True)


def home_page():
    st.header("Welcome to Influencer GPT")
    st.write(f"Hello, {st.session_state.username}!")


def get_trends_page():
    st.header("Discover Trends")
    query = st.text_input("Enter a topic to search trends:")
    source = st.radio("Select trend source:", options=["Twitter", "GPT"], index=1)

    if st.button("Find Trends"):
        if query.strip():
            trends = get_trends(query, st.session_state)
            st.write("Here are the top trends:")
            for trend in trends:
                st.write(f"- {trend}")
        else:
            st.warning("Please enter a topic to search trends.")


def create_video_script_page():
    st.header("Create a Viral Video Script")
    topic = st.text_input("Enter a topic for the video:")
    if st.button("Generate Script"):
        if topic.strip():
            script = create_video_script(topic)
            st.text_area("Generated Script", script, height=200)
        else:
            st.warning("Please enter a topic to generate a script.")


def generate_video_page():
    st.header("Generate Video")
    edited_script = st.text_area("Enter or edit your video script:")
    source_url = st.text_input("Enter a source video URL:")
    if st.button("Generate Video"):
        if edited_script.strip() and source_url.strip():
            video_url = generate_video(edited_script, source_url)
            if video_url:
                st.success("Video generated successfully!")
                st.video(video_url)
            else:
                st.error("Failed to generate the video.")
        else:
            st.warning("Please provide a script and a source URL to generate a video.")


def upload_video_page():
    st.header("Upload Video to YouTube")
    video_url = st.text_input("Enter the video URL to upload:")
    if video_url.strip():
        upload_video(video_url)
    else:
        st.warning("Please enter a video URL to proceed.")


def virtual_influencer_page():
    st.header("Virtual Influencer Generator")
    st.subheader("Step 1: Generate Influencer Profile")
    name = st.text_input("Name", "Lumi Haze")
    personality = st.text_input("Personality", "Adventurous and creative")
    interests = st.text_input("Interests", "Technology, fashion, and mental health awareness")
    if st.button("Generate Profile"):
        profile = generate_influencer_profile(name, personality, interests)
        st.subheader("Generated Profile:")
        st.text_area("Profile", profile, height=150)

    st.subheader("Step 2: Generate Influencer Posts")
    num_posts = st.number_input("Number of Posts", min_value=1, max_value=10, value=1, step=1)
    if st.button("Generate Posts"):
        posts = generate_influencer_content(num_posts)
        st.subheader("Generated Posts:")
        for idx, post in enumerate(posts, 1):
            st.write(f"**Post #{idx}:** {post}")

    st.subheader("Step 3: Generate Influencer Image")
    description = st.text_input("Image Description", "A young, stylish influencer with a bright smile wearing trendy clothes")
    style = st.selectbox("Image Style", ["Realistic", "Cartoon", "Abstract"])
    if st.button("Generate Image"):
        image_url = generate_influencer_image(description, style)
        st.subheader("Generated Image:")
        if "Error" not in image_url:
            st.image(image_url, caption="Generated Influencer Image", use_column_width=True)
        else:
            st.error(image_url)


# Main App Logic
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    login_register_page()
else:
    page = navigate()
    if page == "Home":
        home_page()
    elif page == "Get Trends":
        get_trends_page()
    elif page == "Create Video Script":
        create_video_script_page()
    elif page == "Generate Video":
        generate_video_page()
    elif page == "Upload Video":
        upload_video_page()
    elif page == "Virtual Influencer":
        virtual_influencer_page()
    elif page == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = None
        st.success("Logged out successfully!")
        st.experimental_rerun()

st.sidebar.write("Developed by Epitome with ❤️ using Streamlit")

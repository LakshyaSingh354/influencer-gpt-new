import openai
import streamlit as st
from dotenv import load_dotenv
import os

# Set up your OpenAI API key
openai.api_key = os.getenv('YOUR_OPENAI_API_KEY', '')

# Function to generate influencer profile
def generate_influencer_profile(name, personality, interests):
    prompt = f"Create a virtual influencer profile with the name '{name}', personality '{personality}', and interests '{interests}'."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error generating profile: {str(e)}"

# Function to generate influencer content
def generate_influencer_content(num_posts):
    posts = []
    try:
        for _ in range(num_posts):
            prompt = "Write a fun and engaging Instagram post for a virtual influencer promoting a new tech gadget."
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            posts.append(response['choices'][0]['message']['content'].strip())
        return posts
    except Exception as e:
        return [f"Error generating posts: {str(e)}"]

# Function to generate influencer image
def generate_influencer_image(description, style):
    # Refine the prompt for better realism or other styles
    dalle_prompt = ""
    if style.lower() == "realistic":
        dalle_prompt = (
            f"Create a highly realistic, photorealistic image of a virtual influencer. "
            f"The influencer should have the following features: {description}. "
            "Ensure detailed facial features, realistic lighting, shadows, and skin textures. "
            "The background should be natural and consistent with the description provided."
        )
    elif style.lower() == "cartoon":
        dalle_prompt = (
            f"Create a cartoon-style image of a virtual influencer: {description}. "
            "Use vibrant colors, bold outlines, and a fun, expressive pose."
        )
    elif style.lower() == "abstract":
        dalle_prompt = (
            f"Create an abstract artistic representation of a virtual influencer: {description}. "
            "Incorporate surreal elements, creative textures, and unconventional compositions."
        )
    else:
        dalle_prompt = f"Create an image of a virtual influencer with the following features: {description}, style: {style}."

    try:
        response = openai.Image.create(
            prompt=dalle_prompt,
            n=1,
            size="1024x1024"
        )
        return response['data'][0]['url']
    except Exception as e:
        return f"Error generating image: {str(e)}"

# Streamlit App
def main():
    st.title("Virtual Influencer Generator")
    st.sidebar.header("Settings")
    
    # Step 1: Influencer Profile
    st.header("Step 1: Generate Influencer Profile")
    name = st.text_input("Name", "Lumi Haze")
    personality = st.text_input("Personality", "Adventurous and creative")
    interests = st.text_input("Interests", "Technology, fashion, and mental health awareness")
    if st.button("Generate Profile"):
        profile = generate_influencer_profile(name, personality, interests)
        st.subheader("Generated Profile:")
        st.text_area("Profile", profile, height=150)

    # Step 2: Influencer Posts
    st.header("Step 2: Generate Influencer Posts")
    num_posts = st.number_input("Number of Posts", min_value=1, max_value=10, value=1, step=1)
    if st.button("Generate Posts"):
        posts = generate_influencer_content(num_posts)
        st.subheader("Generated Posts:")
        for idx, post in enumerate(posts, 1):
            st.write(f"**Post #{idx}:** {post}")

    # Step 3: Influencer Image
    st.header("Step 3: Generate Influencer Image")
    description = st.text_input("Image Description", "A young, stylish influencer with a bright smile wearing trendy clothes")
    style = st.selectbox("Image Style", ["Realistic", "Cartoon", "Abstract"])
    if st.button("Generate Image"):
        image_url = generate_influencer_image(description, style)
        st.subheader("Generated Image:")
        if "Error" not in image_url:
            st.image(image_url, caption="Generated Influencer Image", use_column_width=True)
        else:
            st.error(image_url)

if __name__ == "__main__":
    main()

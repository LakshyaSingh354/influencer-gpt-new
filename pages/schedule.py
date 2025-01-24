import threading
import time
from workflow import automatic_workflow
import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx

import json
from datetime import datetime
import os
import logging

logging.basicConfig(level=logging.INFO)

# Ensure the file 'scheduled_posts.json' exists, if not create it
def create_file_if_not_exists():
    if not os.path.isfile('scheduled_posts.json'):
        # If the file doesn't exist, create it with an empty dictionary
        with open('scheduled_posts.json', 'w') as file:
            json.dump({}, file)
        logging.info("Created new 'scheduled_posts.json' file")

# Call the function to ensure the file exists
create_file_if_not_exists()

st.title("Schedule a Post")

# User input for topic, date, and time
topic = st.text_input("Topic")
date = st.date_input("Date", min_value=datetime.today())
time_input = st.time_input("Time")

if st.button("Confirm"):
    # Open and read the existing scheduled posts data
    with open('scheduled_posts.json', 'r+') as file:
        file_data = json.load(file)
        file_data[topic] = {"date": str(date), "time": str(time_input)}
        file.seek(0)  # Move to the start of the file
        json.dump(file_data, file, indent=4)

def check_schedules():
    logging.info("check_schedules function called")
    # Initialize trend_engine if it doesn't exist in st.session_state
    st.session_state['trend_engine'] = st.session_state.get('trend_engine', 'GPT')
    
    while True:
        # Open the scheduled posts file to check scheduled posts
        with open('scheduled_posts.json', 'r') as file:
            scheduled_posts = json.load(file)
            
            # Loop through each scheduled post
            for topic in list(scheduled_posts.keys()):
                details = scheduled_posts[topic]
                scheduled_time = datetime.strptime(details['date'] + ' ' + details['time'], '%Y-%m-%d %H:%M:%S')
                
                # Check if current time is equal to or later than scheduled time
                if datetime.now() >= scheduled_time:
                    # Call the automatic_workflow function
                    automatic_workflow(topic, st.session_state)
                    # Remove the post after executing the workflow
                    del scheduled_posts[topic]
                    
                    # Save the updated scheduled posts back to the file
                    with open('scheduled_posts.json', 'w') as file:
                        json.dump(scheduled_posts, file, indent=4)
        time.sleep(60)  # Check every minute

# Start the check_schedules function in a new thread
def start_thread():
    logging.info("start_thread function called")
    if 'thread' not in st.session_state or not st.session_state['thread'].is_alive():
        logging.info("Starting a new thread")
        t1 = threading.Thread(target=check_schedules, daemon=True)
        add_script_run_ctx(t1)
        st.session_state['thread'] = t1
        st.session_state['thread'].start()

# Start the thread only if it's not already running
if 'thread' not in st.session_state or not st.session_state['thread'].is_alive():
    start_thread()

# Load and display the scheduled posts
with open('scheduled_posts.json', 'r') as file:
    scheduled_posts = json.load(file)

# Display the scheduled posts and provide a delete button
st.subheader("Scheduled Posts")
for topic in list(scheduled_posts.keys()):
    details = scheduled_posts.get(topic)
    cols = st.columns([4, 1])
    cols[0].markdown(f"**Topic:** {topic}  \n**Date:** {details['date']}  \n**Time:** {details['time']}")
    if cols[1].button("Delete", key=topic):
        # Remove the scheduled post from the JSON file
        del scheduled_posts[topic]
        with open('scheduled_posts.json', 'w') as file:
            json.dump(scheduled_posts, file, indent=4)
        st.success(f"Deleted scheduled post: {topic}")

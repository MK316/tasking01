import streamlit as st
import pandas as pd
import gspread
from gtts import gTTS
from oauth2client.service_account import ServiceAccountCredentials
import os

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", 
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# Replace with the path to your downloaded JSON credentials file
creds = ServiceAccountCredentials.from_json_keyfile_name("path/to/credentials.json", scope)
client = gspread.authorize(creds)

# Load data from "Task" sheet
def load_tasks():
    sheet = client.open("Your Google Sheet Name").worksheet("Task")
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# Save responses to the "Response" sheet
def save_response(question_num, user_name, user_answer):
    response_sheet = client.open("Your Google Sheet Name").worksheet("Response")
    response_sheet.append_row([question_num, user_name, user_answer])

# Text-to-Speech function
def play_audio(text, lang="ko"):
    tts = gTTS(text=text, lang=lang)
    tts.save("temp_audio.mp3")
    st.audio("temp_audio.mp3", format="audio/mp3")
    os.remove("temp_audio.mp3")  # Clean up the audio file after playing

# Load tasks from the "Task" sheet
tasks_df = load_tasks()

# Streamlit UI
st.title("Question and Answer App")
st.write("This app provides instructions and questions with audio. Type your answer and submit!")

# User input for name
user_name = st.text_input("Enter your name:")

# Check if user name is provided
if user_name:
    # Start button to display instruction
    if st.button("Start"):
        question_num = 0  # Initialize question index
        instruction = tasks_df.iloc[question_num]["Instruction"]
        play_audio(instruction)
        st.write(instruction)
        
        # Question button to display question
        if st.button("Show Question"):
            question_text = tasks_df.iloc[question_num]["Question"]
            play_audio(question_text)
            st.write(question_text)
            
            # Text box for user to enter their answer
            user_answer = st.text_input("Your answer:")
            
            # Submit button to save response
            if st.button("Submit"):
                save_response(question_num + 1, user_name, user_answer)
                st.success("Your answer has been submitted successfully!")
else:
    st.warning("Please enter your name to start.")

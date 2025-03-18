import pandas as pd
from huggingface_hub import InferenceClient
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Hugging Face Client Setup
HF_TOKEN = "YOUR HF TOKEN"  # Update with your valid token
client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.3", token=HF_TOKEN)

# Load Dataset (optional if needed for other purposes)
dataset = pd.read_csv("C:\\Users\\rapol\\Downloads\\mentalhealth\\dataset.csv")


# Function to handle the query using only the model
def get_model_response(query):
    prompt = f"You are a compassionate mental health assistant. Respond empathetically to the user's query:\n\nUser query: {query}"
    messages = [{"role": "user", "content": prompt}]

    try:
        # Query the Hugging Face model
        response_content = client.chat_completion(
            messages=messages, max_tokens=2000, stream=False
        )
        response = response_content.choices[0].message.content.strip()
        return response
    except Exception as e:
        print(f"[ERROR] Error querying the model: {e}")
        return "I'm here to support you. Could you rephrase your question?"


# Function to check for suicide or death-related thoughts in the response
def check_for_suicide_thoughts(response):
    suicide_keywords = ["suicide", "death", "kill myself", "end my life", "harm myself"]
    for keyword in suicide_keywords:
        if keyword in response.lower():
            return True
    return False


# Function to send an email (to notify parents)
# Main function to handle user queries
def handle_user_query(query):
    # Get response from the model
    response = get_model_response(query)
    return response

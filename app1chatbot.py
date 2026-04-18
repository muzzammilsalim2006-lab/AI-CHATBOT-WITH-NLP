# ✅ FINAL ADVANCED AI CHATBOT (ALL FEATURES)

import streamlit as st
import nltk
import spacy
import random
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from difflib import get_close_matches

# Download (only first time)
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# Load model
nlp = spacy.load("en_core_web_sm")

# Stopwords
stop_words = set(stopwords.words('english'))

# Knowledge base (multiple responses)
data = {
    "hello": ["Hi!", "Hello!", "Hey there!", "Hi, how can I help you?"],
    "how are you": ["I'm doing great!", "All good here!", "Feeling awesome!"],
    "what do you do": ["I'm a helpful chatbot!", "I assist with various queries!"],
    "what is python": ["Python is a powerful programming language."],
    "what is ai": ["AI stands for Artificial Intelligence."],
    "who created you": ["I was created as part of an internship project by Muzzammil Sheikh. I'm here to assist you!"],
    "what is your purpose": ["My purpose is to assist you with information and answer your questions."],
    "what is your name": ["My name is Simchi!"],
    "help": ["You can ask me about Python, AI, or general questions."],
    "bye": ["Goodbye!", "See you soon!", "Take care!"]
}

default_responses = [
    "I'm not sure I understand. Can you rephrase?",
    "Interesting question! Try asking differently.",
    "I didn't get that. Ask something else."
]

# ---------------- NLP ---------------- #

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    filtered = [word for word in tokens if word not in stop_words]
    return " ".join(filtered)

# Spell correction (basic)
def correct_spelling(user_input):
    words = user_input.split()
    corrected = []
    for word in words:
        matches = get_close_matches(word, data.keys(), n=1, cutoff=0.7)
        if matches:
            corrected.append(matches[0])
        else:
            corrected.append(word)
    return " ".join(corrected)

# ---------------- Chatbot Logic ---------------- #

def chatbot_response(user_input):
    processed_input = preprocess(user_input)

    # Greeting detection
    if any(word in user_input.lower() for word in ["hello", "hi", "hey"]):
        return random.choice(data["hello"])

    # Spell correction (optional)
    processed_input = correct_spelling(processed_input)

    best_match = None
    highest_similarity = 0

    for key in data:
        sim = nlp(processed_input).similarity(nlp(key))
        
        if sim > highest_similarity:
            highest_similarity = sim
            best_match = key

    if highest_similarity > 0.7:
        return random.choice(data[best_match])
    else:
        return random.choice(default_responses)

# ---------------- Context Handling ---------------- #

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- UI ---------------- #

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

st.title("🤖 AI Chatbot")
st.write("Ask me anything about Python, AI, or general queries!")

# Input box
user_input = st.text_input("You:")

# When user sends message
if user_input:
    response = chatbot_response(user_input)

    # Save conversation
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Display chat history
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")

st.markdown("---")
st.caption("Built using NLP (NLTK + spaCy) with Streamlit UI 🚀")
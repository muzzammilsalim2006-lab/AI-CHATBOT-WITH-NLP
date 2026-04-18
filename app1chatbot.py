import streamlit as st
import nltk
import spacy
import random
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Downloads
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# Load model
nlp = spacy.load("en_core_web_sm")

stop_words = set(stopwords.words('english'))

# 🔥 Expanded dataset (IMPORTANT FIX)
data = {
    "hello": ["Hi!", "Hello!", "Hey there!", "Hi, how can I help you?"],
    "hi": ["Hello!", "Hi there!"],
    "how are you": ["I'm doing great!", "All good here!", "Feeling awesome!"],
    "what do you do": ["I am an AI chatbot. I answer your questions."],
    "who are you": ["I am an AI chatbot created using NLP."],
    "what is python": ["Python is a programming language."],
    "python": ["Python is a powerful programming language."],
    "what is ai": ["AI stands for Artificial Intelligence."],
    "ai": ["Artificial Intelligence is the simulation of human intelligence."],
    "help": ["You can ask me about Python, AI, or general questions."],
    "bye": ["Goodbye!", "See you later!", "Take care!"]
}

default_responses = [
    "I'm not sure I understand. Can you rephrase?",
    "Try asking in a different way.",
    "I didn't get that. Ask something else."
]

# 🔹 Preprocess
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    filtered = [word for word in tokens if word not in stop_words]
    return " ".join(filtered)

# 🔥 Improved Response Logic
def chatbot_response(user_input):
    user_input_lower = user_input.lower()
    processed_input = preprocess(user_input)

    # ✅ 1. Direct match (BEST)
    for key in data:
        if key in user_input_lower:
            return random.choice(data[key])

    # ✅ 2. Token match (NEW FIX)
    for key in data:
        if any(word in key for word in processed_input.split()):
            return random.choice(data[key])

    # ✅ 3. NLP similarity
    best_match = None
    highest_similarity = 0

    for key in data:
        sim = nlp(processed_input).similarity(nlp(key))
        if sim > highest_similarity:
            highest_similarity = sim
            best_match = key

    if highest_similarity > 0.5:
        return random.choice(data[best_match])

    # ✅ 4. Fallback
    return random.choice(default_responses)

# ---------------- UI ---------------- #

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

st.title("🤖 AI Chatbot")
st.write("Ask me anything about Python, AI, or general queries!")

user_input = st.text_input("You:")

if user_input:
    response = chatbot_response(user_input)

    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Display chat
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"🧑 **You:** {message}")
    else:
        st.markdown(f"🤖 **Bot:** {message}")

st.markdown("---")
st.caption("Improved NLP Chatbot with better matching 🚀")
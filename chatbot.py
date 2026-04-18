# ✅ FINAL VERSION: Smart NLP Chatbot (Step 2–5)

import nltk
import spacy
import random
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# ✅ Download required data (runs only first time)
nltk.download('punkt')
nltk.download('stopwords')

# ✅ Load spaCy model
nlp = spacy.load("en_core_web_sm")

# ✅ Preload stopwords (optimized)
stop_words = set(stopwords.words('english'))

# ✅ Knowledge Base (multiple responses)
data = {
    "hello": ["Hi!", "Hello!", "Hey there!"],
    "how are you": ["I'm good!", "Doing great!", "All fine here!"],
    "what is python": ["Python is a powerful programming language."],
    "what is machine learning": ["Machine learning is a subset of AI that focuses on algorithms and statistical models."],
    "what is your name": ["I'm a smart chatbot!"],
    "what is ai": ["AI stands for Artificial Intelligence."],
    "who created you": ["I was created as part of an internship task created by Muzzamil. I'm here to help!"],
    "help": ["You can ask me about Python, AI, or general questions."],
    "bye": ["Goodbye!", "See you later!", "Take care!"]
}

# ✅ Default responses
default_responses = [
    "I'm not sure I understand. Can you rephrase?",
    "Interesting question! Try asking differently.",
    "I didn't get that. Ask something else."
]

# ✅ Preprocessing function
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    tokens = word_tokenize(text)
    filtered = [word for word in tokens if word not in stop_words]
    
    return " ".join(filtered)

# ✅ Chatbot response using NLP similarity
def chatbot_response(user_input):
    processed_input = preprocess(user_input)

    # ✅ Greeting shortcut (faster response)
    if any(word in user_input.lower() for word in ["hello", "hi", "hey"]):
        return random.choice(data["hello"])

    best_match = None
    highest_similarity = 0

    for key in data:
        sim = nlp(processed_input).similarity(nlp(key))
        
        if sim > highest_similarity:
            highest_similarity = sim
            best_match = key

    # ✅ Improved threshold
    if highest_similarity > 0.7:
        return random.choice(data[best_match])
    else:
        return random.choice(default_responses)

# ✅ Chat loop (FIXED - waits for input properly)
print("🤖 Smart Chatbot Started! Type 'bye' to exit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "bye":
        print("Bot:", random.choice(data["bye"]))
        break

    response = chatbot_response(user_input)
    print("Bot:", response)
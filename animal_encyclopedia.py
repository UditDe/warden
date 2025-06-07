import streamlit as st
import requests
from sentence_transformers import SentenceTransformer

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')
# wikipedia.set_lang("en")

# Get animal info from Wikipedia
# def get_animal_info(animal_name):
#     try:
#         summary = wikipedia.summary(animal_name, sentences=5)
#         return summary
#     except Exception:
#         return None  # Return None instead of showing messy error

# Ask LLM via Ollama
def ask_llm(question):
    prompt = f"Tell us somthing about : {question}"
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False},
            timeout=60
        )
        data = response.json()
        return data["response"] if "response" in data else str(data)
    except Exception as e:
        return f"❌ Request failed: {e}"

# Streamlit UI
st.set_page_config(page_title="Animal Encyclopedia", page_icon="🦁")
st.title("🧠🔍 Animal Encyclopedia (Warden's Diary)")

query = st.text_input("Search through his diary about animals:")
if st.button("Search") and query.strip() != "":
    with st.spinner("Fetching info and generating answer..."):
        response = ask_llm(query)
        st.subheader("🤖 Warden Says:")
        st.success(response)


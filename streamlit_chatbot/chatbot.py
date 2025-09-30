import streamlit as st
import pandas as pd


def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def main():
    st.title("My First Chatbot")
    
    initialize_session_state()

    # Display chat messages
    for message in st.session_state.messages:
     if message["role"] == "assistant":
         with st.chat_message("assistant", avatar=robot_img):
            st.write(f"{message['content']}")
    else:
         with st.chat_message("user", avatar=user_emoji):
            st.write(f"{message['content']}")

    # Chat input
    if prompt := st.chat_input("What's on your mind?"):
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Add simple bot response
        response = f"You said: {prompt}"
        with st.chat_message("assistant"):
            st.write(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})


with st.sidebar:
    st.title("Sidebar") 
    ("hi gooners")
    st.radio("Radio-button select", ["Friendly", "Formal", "Funny"], index=0)
    st.multiselect("Multi-select", ["Movies", "Travel", "Food", "Sports"], default=["Food"])
    st.selectbox("Dropdown select", ["Data", "Code", "Travel", "Food", "Sports"], index=0)
    st.slider("Slider", min_value=1, max_value=200, value=60)
    st.select_slider("Option Slider", options=["Very Sad", "Sad", "Okay", "Happy", "Very Happy"], value="Okay")

import streamlit as st
import google.generativeai as genai

import streamlit as st
import google.generativeai as genai

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyBEGMzFNsVxD23D_Nd7SM5TwwEp1QwmzEQ"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def get_gemini_response(prompt):
    response = model.generate_content(prompt)
    return response.text

def main():
    st.title("Gemini AI Chatbot")
    
    initialize_session_state()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Chat with Gemini"):
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
    # Get Gemini response
        response = get_gemini_response(prompt,)
       ##Find the "get_gemini_response" function in your code and replace it with this function below

        # Display assistant response
        with st.chat_message("assistant"):
            st.write(response)
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()

import streamlit as st
import random
import os
import google.generativeai as genai


genai.configure(api_key=os.getenv("AIzaSyBEGMzFNsVxD23D_Nd7SM5TwwEp1QwmzEQ"))
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

def ask_gemini(prompt: str) -> str:
    """Ask Gemini for text. Always returns safe string."""
    try:
        response = gemini_model.generate_content(prompt)
        return response.text if response and response.text else "No response."
    except Exception as e:
        return f"(Gemini unavailable: {e})"


# ================================
# 🎮 Game State Initialization
# ================================
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "stats" not in st.session_state:
    st.session_state.stats = {"Singing": 50, "Dancing": 50, "Popularity": 50, "Teamwork": 50}
if "history" not in st.session_state:
    st.session_state.history = []
if "player_name" not in st.session_state:
    st.session_state.player_name = None
if "show_name" not in st.session_state:
    st.session_state.show_name = None
if "random_event" not in st.session_state:
    st.session_state.random_event = None


# ================================
# 🎲 Helpers
# ================================
def update_stats(updates, choice_desc):
    for k, v in updates.items():
        st.session_state.stats[k] = max(0, min(100, st.session_state.stats[k] + v))
    st.session_state.history.append(choice_desc)

def go_to(page):
    st.session_state.page = page

def get_random_event():
    """Use Gemini to generate a random twist each episode."""
    return ask_gemini(
        f"Generate a short 1–2 sentence random plot twist that could happen "
        f"in a K-pop survival reality show like {st.session_state.show_name}. "
        "Make it realistic (e.g., mentor feedback, sudden challenge, injury, praise)."
    )


# ================================
# 📝 Pages
# ================================
def intro():
    st.title("🎤 K-Pop Survival: The Debut Mission")

    st.write("Welcome to your journey to debut in a K-pop group! "
             "First, let's set up your profile.")

    if st.session_state.player_name is None:
        name = st.text_input("Enter your first name:")
        if name:
            surnames = ["Kim", "Park", "Lee", "Choi", "Jeon", "Jung", "Seo", "Han", "Kang", "Yoon"]
            st.session_state.player_name = random.choice(surnames) + " " + name

    if st.session_state.show_name is None:
        shows = ["I-LAND", "Produce 101", "Sixteen", "Girls Planet 999", "Loud", "Mixnine", "The Unit"]
        st.session_state.show_name = st.selectbox("Choose your survival show:", shows)

    if st.session_state.player_name and st.session_state.show_name:
        st.success(f"Welcome, {st.session_state.player_name}! You’ve entered **{st.session_state.show_name}**.")
        if st.button("Start Journey"):
            go_to("ep1")


def episode(title, description, choices, next_ep):
    """Generic episode page with random Gemini event injection."""
    st.header(title)
    st.write(description)

    # Show Gemini random twist
    if st.session_state.random_event is None:
        st.session_state.random_event = get_random_event()
    st.info(f"📺 Twist: {st.session_state.random_event}")

    for label, effect in choices.items():
        if st.button(label):
            update_stats(effect, f"Chose: {label}")
            st.session_state.random_event = None  # reset for next episode
            go_to(next_ep)
            break


def ep1():
    episode("Episode 1", 
            "Your first audition on stage. What do you show off?",
            {
                "🎶 Show vocals": {"Singing": 10, "Popularity": 5},
                "💃 Focus on dancing": {"Dancing": 10, "Popularity": 5},
                "🤝 Highlight teamwork": {"Teamwork": 10},
            }, "ep2")


def ep2():
    episode("Episode 2", 
            "In the training camp, mentors assign group tasks. How do you contribute?",
            {
                "🧑‍✈️ Take leadership role": {"Teamwork": 10, "Popularity": 5},
                "🎵 Focus on your lines": {"Singing": 10},
                "🩰 Help others with choreography": {"Dancing": 10, "Teamwork": 5},
            }, "ep3")


def ep3():
    episode("Episode 3", 
            "Mid-season twist! A dance battle is announced.",
            {
                "⚡ Go all out with freestyle": {"Dancing": 15, "Popularity": 5},
                "😎 Play safe but polished": {"Dancing": 5, "Teamwork": 5},
                "🎤 Add vocal ad-libs to stand out": {"Singing": 10, "Popularity": 5},
            }, "ep4")


def ep4():
    episode("Episode 4", 
            "Time for a collaboration stage with other contestants.",
            {
                "🌟 Aim for the center position": {"Popularity": 15},
                "🎶 Support with strong vocals": {"Singing": 10, "Teamwork": 5},
                "💃 Carry the dance parts": {"Dancing": 10, "Teamwork": 5},
            }, "ep5")


def ep5():
    episode("Episode 5", 
            "The producers release behind-the-scenes clips. How do you behave?",
            {
                "😂 Be playful and funny": {"Popularity": 15},
                "🤔 Show dedication in practice": {"Singing": 5, "Dancing": 5},
                "🤝 Encourage your teammates": {"Teamwork": 15},
            }, "ep6")


def ep6():
    episode("Episode 6", 
            "The final live stage. Your last chance to impress.",
            {
                "🎤 Pour heart into vocals": {"Singing": 20},
                "🔥 Deliver powerful dance": {"Dancing": 20},
                "✨ Bond with fans through ment": {"Popularity": 20},
            }, "results")


def results():
    st.header("🌟 Final Results")
    stats = st.session_state.stats
    st.write("### Final Stats")
    st.json(stats)

    score = sum(stats.values())
    if score >= 300:
        st.success("🎉 Congratulations! You debuted in the final group!")
    elif score >= 240:
        st.warning("✨ You gave a strong performance and almost debuted, but were just short.")
    else:
        st.error("💔 You were eliminated before the final lineup.")

    finale = ask_gemini(
        f"Summarize the contestant {st.session_state.player_name}'s entire journey on the show "
        f"{st.session_state.show_name}. Stats: {stats}. "
        "Write a dramatic final speech as if the host is speaking."
    )
    st.write(f"🎙️ {finale}")

    st.write("### Choices Made")
    st.write(st.session_state.history)

    if st.button("Play Again"):
        st.session_state.page = "intro"
        st.session_state.stats = {"Singing": 50, "Dancing": 50, "Popularity": 50, "Teamwork": 50}
        st.session_state.history = []
        st.session_state.player_name = None
        st.session_state.show_name = None
        st.session_state.random_event = None


# ================================
# 🚦 Router
# ================================
if st.session_state.page == "intro":
    intro()
elif st.session_state.page == "ep1":
    ep1()
elif st.session_state.page == "ep2":
    ep2()
elif st.session_state.page == "ep3":
    ep3()
elif st.session_state.page == "ep4":
    ep4()
elif st.session_state.page == "ep5":
    ep5()
elif st.session_state.page == "ep6":
    ep6()
elif st.session_state.page == "results":
    results()

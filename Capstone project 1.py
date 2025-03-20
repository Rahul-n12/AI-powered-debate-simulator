import streamlit as st
import openai
import os
import time
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize OpenAI and Groq API clients
openai.api_key = os.getenv("OPENAI_API_KEY")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Initialize chat history in Streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "turn_count" not in st.session_state:
    st.session_state.turn_count = 0
if "debate_ended" not in st.session_state:
    st.session_state.debate_ended = False

# Define AI personas
STEVE_PROMPT = """
You are Steve Jobs, the visionary co-founder of Apple. You embody innovation, creativity, and perfectionism.
Your debating style is passionate and persuasive, emphasizing design, simplicity, and impact on the world.
"""
ELON_PROMPT = """
You are Elon Musk, the entrepreneur behind Tesla, SpaceX, and Neuralink. You focus on engineering, scale, and bold technological advancements.
Your debating style is pragmatic, futuristic, and focused on first-principles thinking.
"""

# Function to generate a response from OpenAI (Steve Jobs)
def query_steve(user_input, context):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": STEVE_PROMPT},
            {"role": "user", "content": user_input}
        ],
        max_tokens=70
    )
    return response.choices[0].message.content

# Function to generate a response from Groq API (Elon Musk)
def query_elon(user_input, context):
    response = groq_client.chat.completions.create(
        model="llama-3.2-1b-preview",
        messages=[
            {"role": "system", "content": ELON_PROMPT},
            {"role": "user", "content": user_input}
        ],
        max_tokens=70
    )
    return response.choices[0].message.content

# Function to simulate the debate
def simulate_debate():
    if st.session_state.debate_ended:
        st.warning("The debate has already concluded. Restart the app to run again.")
        return

    st.subheader("Steve Jobs vs. Elon Musk: The Great Debate")

    if st.session_state.turn_count == 0:
        st.session_state.chat_history.append({"role": "moderator", "content": "Who has contributed more to the advancement of technology?"})
    
    while st.session_state.turn_count < 50:
        last_message = st.session_state.chat_history[-1]["content"]

        if st.session_state.turn_count % 2 == 0:
            # Steve Jobs' turn
            response = query_steve(last_message, st.session_state.chat_history)
            speaker = "Steve Jobs"
        else:
            # Elon Musk's turn
            response = query_elon(last_message, st.session_state.chat_history)
            speaker = "Elon Musk"

        st.session_state.chat_history.append({"role": speaker, "content": response})
        st.session_state.turn_count += 1

        time.sleep(1)

        # Display conversation
        for message in st.session_state.chat_history:
            st.write(f"**{message['role']}**: {message['content']}")

        time.sleep(1)  # Adding slight delay for realism

    st.session_state.debate_ended = True

# Function for judging the debate
def judge():
    if not st.session_state.debate_ended:
        st.warning("Let the debate finish before judging!")
        return
    
    debate_transcript = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.chat_history])

    # Judge's evaluation
    JUDGE_PROMPT = """
    You are an impartial judge evaluating a debate. Analyze the arguments presented, clarity, impact, and engagement.
    Determine which participant—Steve Jobs or Elon Musk—made a stronger case for their contributions to technological advancement.
    Provide a short summary and declare a winner.
    """

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": JUDGE_PROMPT},
            {"role": "user", "content": debate_transcript}
        ],
        max_tokens= 200
    )

    winner = response.choices[0].message.content
    st.subheader("Judge's Verdict")
    st.write(winner)

# Streamlit UI
def main():
    st.title("Steve vs. Elon: The Great Debate")

    # Start the debate
    if st.button("Start Debate"):
        simulate_debate()

    # Display judge's verdict
    if st.button("Judge the Debate"):
        judge()

if __name__ == "__main__":
    main()

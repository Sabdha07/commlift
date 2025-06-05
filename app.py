# Your full Streamlit app.py code goes here, as shared in your last messageimport streamlit as st
import streamlit as st
import requests
import os
from PIL import Image, ImageDraw
from dotenv import load_dotenv
import difflib

from auth import login_user, signup_user, get_user_email
from firebase_utils import save_rewrite, load_recent_rewrites

# --- Setup ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")

# --- Functions ---
def make_rounded(image, radius=None):
    image = image.convert("RGBA")
    width, height = image.size
    if radius is None:
        radius = min(width, height) // 2
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, width, height), fill=255)
    image.putalpha(mask)
    return image

def build_prompt(history, new_message, tone, context, length):
    length_prompt = {
        "Normal": "",
        "Shorter": " Make it more concise and to the point.",
        "Longer": " Elaborate with more details and examples.",
    }
    convo = ""
    for i, entry in enumerate(history[-5:], start=1):
        convo += f"User message #{i}:\n{entry['input']}\n"
        convo += f"Rewritten message #{i}:\n{entry['rewritten']}\n\n"
    style_note = (
        "In your rewrite, imbue a tone of feminine energy that is powerful and inspiring, "
        "using smooth and elegant phrasing. Avoid sharp or aggressive language. "
        "Imagine colors like muted greens, deep reds, blues, and teals with subtle gradients — "
        "bright but not overwhelming, no yellows or oranges. Focus on clarity and warmth while keeping the message motivating and confident."
    )
    return f"""
You are a friendly, expert communication coach who helps users improve their messages.

Rewrite the message clearly and naturally in the user’s voice, adapting to tone/context.

{style_note}

After rewriting, include:
1. A bullet-point list of key improvements.
2. Speaking tips on confidence, tone, pacing.
3. Mini writing tips based on tone.

Include relevant emojis to make the output friendly.

Conversation history:
{convo}

Message:
{new_message}

Context: {context}
Tone: {tone}
Length: {length}.{length_prompt[length]}
""".strip()

def call_gemini_api(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        st.error(f"API Error: {response.status_code} — {response.text}")
        return None

def sentence_diff_table(original, rewritten):
    orig_sentences = [s.strip() for s in original.split(".") if s.strip()]
    new_sentences = [s.strip() for s in rewritten.split(".") if s.strip()]
    matches = difflib.get_close_matches

    st.markdown("### 🔍 Side-by-Side Comparison of Sentences")
    table_data = []
    for orig in orig_sentences:
        best_match = matches(orig, new_sentences, n=1, cutoff=0.3)
        table_data.append((orig, best_match[0] if best_match else ""))

    with st.expander("📋 Compare Sentences"):
        st.write("Each row compares one original sentence with its closest rewritten version.")
        st.table({"Original": [row[0] for row in table_data],
                  "Rewritten": [row[1] for row in table_data]})

# --- UI Setup ---
try:
    logo = Image.open("logo.png")
    logo = make_rounded(logo)
    st.set_page_config(page_title="CommLift ✨", page_icon=logo, layout="wide")
except FileNotFoundError:
    st.set_page_config(page_title="CommLift ✨", page_icon="📢", layout="wide")

st.title("🌊 CommLift — Uplift Your Communication")
st.markdown("Write better, speak clearer, and grow your communication skills — powered by Google Gemini.")

st.sidebar.title("🔐 Login / Signup")

if "user" not in st.session_state:
    st.session_state.user = None
if "email" not in st.session_state:
    st.session_state.email = None

auth_mode = st.sidebar.radio("Select", ["Login", "Sign Up"], horizontal=True)
email_input = st.sidebar.text_input("Email")
password_input = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Submit"):
    if auth_mode == "Login":
        user = login_user(email_input, password_input)
    else:
        user = signup_user(email_input, password_input)
    
    if user:
        st.session_state.user = user
        st.session_state.email = get_user_email(user)
        st.success(f"Welcome, {st.session_state.email}!")
        st.rerun()
    else:
        st.error("Authentication failed. Please try again.")

if st.session_state.user:
    st.sidebar.success(f"Logged in as {st.session_state.email}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.email = None
        st.rerun()

if "history" not in st.session_state:
    st.session_state.history = []

# --- Inputs ---
message_input = st.text_area("✏️ Paste your raw message or idea:", height=200)

context = st.selectbox("📌 What's the context?", [
    "General improvement", "Message to mentor after meeting", "Cold email to researcher",
    "LinkedIn connection intro", "Thank-you message",
    "Professional DM", "Other"
])
if context == "Other":
    context = st.text_input("Enter custom context:")

tone = st.selectbox("🎯 Choose your tone:", [
    "Warm and Reflective", "Casual and Friendly",
    "Professional and Concise", "Bold and Confident", "Humble and Curious"
])
length = st.radio("📝 Message length:", ["Normal", "Shorter", "Longer"])

mini_tips = {
    "Warm and Reflective": "Use heartfelt words and personal touches.",
    "Casual and Friendly": "Keep sentences light and conversational.",
    "Professional and Concise": "Focus on clarity and avoid filler words.",
    "Bold and Confident": "Use strong verbs and affirmative language.",
    "Humble and Curious": "Express openness and willingness to learn."
}

# --- Gemini Call ---
if st.button("✨ Rewrite & Coach Me"):
    if not message_input.strip():
        st.warning("Please enter a message.")
    else:
        with st.spinner("Thinking deeply..."):
            prompt = build_prompt(st.session_state.history, message_input, tone, context, length)
            result = call_gemini_api(prompt)
            if result:
                parts = result.split("\n\n")
                rewritten = parts[0]
                feedback = "\n\n".join(parts[1:]) if len(parts) > 1 else "No feedback found."
                record = {
                    "input": message_input,
                    "rewritten": rewritten,
                    "feedback": feedback,
                    "context": context,
                    "tone": tone,
                    "length": length,
                }

                st.session_state.history.append(record)

                if st.session_state.user:
                    save_rewrite(st.session_state.user["localId"], **record)


                st.markdown("---")
                st.subheader("✅ Rewritten Message")
                st.markdown(f"<div style='color:#2C6E49; font-weight:600;'>{rewritten}</div>", unsafe_allow_html=True)

                st.subheader("🛠️ Why These Edits?")
                st.markdown(feedback)

                st.info(f"💡 Mini Tip: {mini_tips.get(tone, '')}")

                sentence_diff_table(message_input, rewritten)

# --- History ---
if st.session_state.history:
    st.markdown("---")
    st.subheader("🗂️ Your Past Rewrites")
    for i, entry in enumerate(reversed(st.session_state.history[-5:]), 1):
        with st.expander(f"Rewrite #{len(st.session_state.history) - i + 1} ({entry['tone']} / {entry['context']})"):
            st.markdown(f"**Original:**\n\n{entry['input']}")
            st.markdown(f"**Rewritten:**\n\n<div style='color:#34495e;'>{entry['rewritten']}</div>", unsafe_allow_html=True)
            st.markdown(f"**Feedback:**\n\n<div style='color:#27ae60;'>{entry['feedback']}</div>", unsafe_allow_html=True)

if st.session_state.user and "history" not in st.session_state:
    st.session_state.history = load_recent_rewrites(st.session_state.user["localId"])

# --- Footer Section ---
st.markdown("---")

# Quote with bigger font and energy
st.markdown(
    """
    <h3 style='text-align:center; font-weight:bold; font-size:26px;'>
    ⚡️ Clarity cuts deeper than noise ever could! Don’t just craft messages — craft MOMENTUM! ⚡️
    </h3>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown(
        """
        <div style="text-align: left; font-size: 0.85rem; line-height: 1.3;">
            <strong>Built with💡by Sabh & Powered by Google's Gemini & OpenAI's ChatGPT</strong><br>
            © 2025 CommLift — All rights reserved.
        </div>
        """,
        unsafe_allow_html=True,
    )

with right_col:
    st.markdown(
        """
        <div style="text-align: right; font-size: 0.85rem; line-height: 1.3;">
            <strong>Got a spark of thought, suggestion, or question? Just a message away — let’s connect!</strong><br>
            <a href="https://linkedin.com/in/sabdhayini" style="text-decoration:none;">🔗 LinkedIn</a>&nbsp;&nbsp; 
            <a href="mailto:sabdha.up@gmail.com" style="text-decoration:none;">✉️ Email</a>&nbsp;&nbsp; 
            <a href="https://yourwebsite.com" style="text-decoration:none;">🌐 Website</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
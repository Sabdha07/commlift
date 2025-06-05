import pyrebase
from datetime import datetime
import streamlit as st

firebase_config = {
    "apiKey": st.secrets["firebase"]["api_key"],
    "authDomain": st.secrets["firebase"]["auth_domain"],
    "projectId": st.secrets["firebase"]["project_id"],
    "storageBucket": st.secrets["firebase"]["storage_bucket"],
    "messagingSenderId": st.secrets["firebase"]["messaging_sender_id"],
    "appId": st.secrets["firebase"]["app_id"],
    "measurementId": st.secrets["firebase"]["measurement_id"],
    "databaseURL": st.secrets["firebase"]["database_url"],
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

def save_rewrite(user_id, input_text, rewritten, feedback, context, tone, length):
    key = datetime.utcnow().isoformat()
    db.child("users").child(user_id).child("sessions").child(key).set({
        "input": input_text,
        "rewritten": rewritten,
        "feedback": feedback,
        "context": context,
        "tone": tone,
        "length": length,
        "timestamp": key,
    })

def load_recent_rewrites(user_id, max_sessions=4):
    all_data = db.child("users").child(user_id).child("sessions").get()
    if not all_data.each():
        return []
    sorted_data = sorted(all_data.each(), key=lambda x: x.key(), reverse=True)
    return [item.val() for item in sorted_data[:max_sessions]]

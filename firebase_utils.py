import pyrebase
import os
from datetime import datetime

# Build firebase_config dict from environment variables
firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
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

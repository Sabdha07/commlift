import pyrebase
import json
from datetime import datetime

with open("firebase_config.json") as f:
    firebase_config = json.load(f)

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

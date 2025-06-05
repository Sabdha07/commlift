import pyrebase
import streamlit as st

# Build firebase_config dict from streamlit 
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
auth = firebase.auth()


def login_user(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user
    except Exception as e:
        return None

def signup_user(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        return user
    except Exception as e:
        return None

def get_user_email(user):
    return user['email'] if user else None

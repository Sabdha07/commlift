# 🌊 CommLift — Uplift Your Communication

**CommLift** is your friendly AI-powered communication coach.  
Paste your rough message, choose a tone and context — and get back a polished, confident version with instant tips.

Whether you're writing to a professor, applying for an opportunity, or just want to sound better — CommLift helps you express yourself clearly and powerfully.

---

## ✨ Features

- 🧠 Rewrites your message using Google Gemini API
- 🎯 Tone & length customization (Warm, Bold, Humble, etc.)
- 📝 Side-by-side sentence comparison to track edits
- 📌 Context-aware rewrites (thank-you, DM, cold email, etc.)
- 💡 Speaking and writing tips generated instantly
- 🗂️ Optional login to save up to 4 past sessions per user (via Firebase)

---

## 🚀 Try CommLift Live

Use the app instantly at:  
👉 [https://your-streamlit-link.streamlit.app](https://your-streamlit-link.streamlit.app)

---

## 🛠️ Run Locally (Optional)

If you want to run the app on your machine:

### 1. Clone the repository

```bash
git clone https://github.com/your-username/commlift.git
cd commlift
```
### 2. Install dependencies
We recommend using a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
### 3. Add API Keys
Create a .env file in the root directory with:
```ini
GEMINI_API_KEY=your_google_gemini_api_key
```
Also, place your Firebase credentials in ```firebase_config.json```.

### 4. Run the app
```bash
streamlit run app.py
```

---

## 🙌 Acknowledgements

- Built with [Streamlit](https://streamlit.io/)
- Developed with assistance from [ChatGPT by OpenAI](https://openai.com/chatgpt)
- AI-powered by [Google Gemini API](https://ai.google.dev/)  
- User authentication handled via [Firebase](https://firebase.google.com/)

---

## 
Developed by **Sabh**  
🔗 [LinkedIn](https://linkedin.com/in/sabdhayini) | ✉️ [Email](mailto:sabdha.up@gmail.com)

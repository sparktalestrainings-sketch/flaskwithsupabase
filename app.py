import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv

from db import SessionLocal, engine
from models import Base, Conversation

# load environment
load_dotenv()

app = Flask(__name__)

# init db tables
Base.metadata.create_all(bind=engine)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY missing")

client = Groq(api_key=GROQ_API_KEY)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # get LLM reply
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": user_message}]
    )
    bot_reply = completion.choices[0].message.content

    # save to db
    db = SessionLocal()
    conv = Conversation(user_message=user_message, bot_reply=bot_reply)
    db.add(conv)    
    db.commit()
    db.close()
    Base.metadata.create_all(bind=engine)
    
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

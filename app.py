import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from openai import OpenAI  # works for SambaNova's OpenAI-compatible SDK

load_dotenv()

app = Flask(__name__)

# Set your SambaNova API key and base URL
client = OpenAI(
    api_key= "-----", 
    base_url="-----",
)

SYSTEM_PROMPT = (
    "You are CalmMind, a supportive, empathetic virtual mental‑health companion. "
    "You listen without judgment, validate feelings, ask gentle open‑ended questions, "
    "and provide coping strategies such as breathing exercises, grounding techniques, "
    "and positive affirmations. You are not a licensed therapist and should encourage "
    "users to seek professional help or call emergency services if they are in crisis."
)

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/chat")
def chat():
    data = request.get_json(force=True)
    user_message = (data or {}).get("message", "")

    try:
        response = client.chat.completions.create(
            model="--------",  # from your working example- gpt-4.0, lama
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.5,
            top_p=0.9
        )
        assistant_reply = response.choices[0].message.content.strip()
    except Exception as e:
        app.logger.error(e)
        assistant_reply = "Sorry, something went wrong while connecting to SambaNova."

    return jsonify({"reply": assistant_reply})

if __name__ == "__main__":
    app.run(debug=True)

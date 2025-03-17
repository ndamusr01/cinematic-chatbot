from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows cross-origin requests

# Load OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Cinematic Prompting Chatbot is Live!"

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        user_description = data.get("description")

        # Corrected OpenAI API call
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # ✅ Changed to GPT-3.5-turbo
            messages=[{"role": "user", "content": f"I'm imagining this scene: {user_description}"}]
        )

        return jsonify({"prompt": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

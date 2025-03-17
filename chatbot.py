from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS  # Import CORS to allow cross-origin requests

app = Flask(__name__)
CORS(app)  # Enable CORS to fix cross-origin issues

# Get API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Cinematic Prompting Chatbot is Live!"

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        user_description = data.get("description", "")

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"I'm imagining this scene: {user_description}"}],
            api_key=OPENAI_API_KEY  # This line is incorrect in latest OpenAI API versions
        )

        return jsonify({"prompt": response["choices"][0]["message"]["content"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

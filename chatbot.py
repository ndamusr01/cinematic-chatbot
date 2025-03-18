from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import openai
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains (for testing)
# CORS(app, origins=["https://reikonomori.com"])  # Use this in production to allow only your domain

# Load API Key from Environment Variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Cinematic Prompting Chatbot is Live!"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    user_description = data.get("description", "")
    length = data.get("length", "default")  # Allow users to specify 'short', 'medium', 'long'

    # Define different prompt lengths
    max_tokens = {"short": 100, "medium": 250, "long": 400}.get(length, 300)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Generate a cinematic AI prompt for: {user_description}"}],
        max_tokens=max_tokens,
        api_key=OPENAI_API_KEY
    )

    output_prompt = response["choices"][0]["message"]["content"]
    return jsonify({"prompt": output_prompt})  # JSON response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

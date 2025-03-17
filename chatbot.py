from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS to allow cross-origin requests
import openai
import os

app = Flask(__name__)
CORS(app)  # Enable CORS

# Replace with your OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Cinematic Prompting Chatbot is Live!"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()  # Use request.get_json() instead of request.json
    if not data or "description" not in data:
        return jsonify({"error": "Missing 'description' field"}), 400  # Handle missing data

    user_description = data["description"]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"I'm imagining this scene: {user_description}"}],
            api_key=OPENAI_API_KEY
        )
        chatbot_response = response["choices"][0]["message"]["content"]
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Catch API errors

    return jsonify({"prompt": chatbot_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

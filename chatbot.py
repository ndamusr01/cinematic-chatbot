from flask import Flask, request, jsonify
from flask_cors import CORS  # Enable cross-origin requests
import openai
import os

app = Flask(__name__)
CORS(app)  # Allow CORS for all domains

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def determine_length(user_input):
    """Determines the length of the response based on user input."""
    if "shorter" in user_input.lower():
        return 200  # Shorter response (~200 characters)
    elif "longer" in user_input.lower():
        return 800  # Longer response (~800 characters)
    else:
        return 400  # Default response length (~400 characters)

@app.route("/", methods=["GET"])
def home():
    return "Cinematic Prompting Chatbot is Live!"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    user_description = data.get("description", "")
    length = determine_length(user_description)
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in generating hyper-detailed cinematic AI prompts for text-to-image generation."},
            {"role": "user", "content": f"Generate a highly detailed cinematic prompt based on this scene: {user_description}. Limit the response to approximately {length} characters."}
        ],
        api_key=OPENAI_API_KEY
    )
    
    return jsonify({"prompt": response["choices"][0]["message"]["content"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

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
    if length == "short":
        max_tokens = 100
    elif length == "medium":
        max_tokens = 250
    elif length == "long":
        max_tokens = 400
    else:
        max_tokens = 300  # Default length

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Generate a cinematic AI prompt for: {user_description}"}],
        max_tokens=max_tokens,
        api_key=OPENAI_API_KEY
    )

    output_prompt = response["choices"][0]["message"]["content"]
    
    return jsonify({"prompt": output_prompt})  # JSON response


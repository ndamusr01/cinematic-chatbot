from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from your frontend

# Load OpenAI API Key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Cinematic Prompting Chatbot is Live!"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    user_description = data.get("description", "").strip().lower()

    # Determine prompt length based on keywords
    if "shorter" in user_description:
        length_modifier = "Make it a concise but detailed description, around 250 characters."
        user_description = user_description.replace("shorter", "").strip()
    elif "longer" in user_description:
        length_modifier = "Expand it into an in-depth cinematic scene description, around 600 characters."
        user_description = user_description.replace("longer", "").strip()
    else:
        length_modifier = "Generate a standard-length detailed description."

    # OpenAI API Call
    try:
       response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a Cinematic Prompt Generator. Your task is to craft hyper-detailed, cinematic AI prompts for text-to-image generation, using highly specific descriptions, lighting details, composition, mood, and camera settings. Do not write a story. Format the response in structured prompt style."},
        {"role": "user", "content": f"Generate a detailed, cinematic AI image prompt for: {user_description}"}
    ],
    api_key=OPENAI_API_KEY
)

        output_prompt = response["choices"][0]["message"]["content"]

        return jsonify({"prompt": output_prompt})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

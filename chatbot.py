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
        {
            "role": "system",
            "content": (
                "You are a Cinematic AI Prompt Generator. Your job is to generate hyper-detailed prompts for AI image generation. "
                "Format the output strictly in a structured prompt style. Do NOT write a story. "
                "Include key details such as subject, lighting, camera settings, composition, depth of field, color grading, and mood. "
                "Ensure the response is concise, usable, and formatted as an AI prompt."
            ),
        },
        {
            "role": "user",
            "content": f"Generate a cinematic AI image prompt for: {user_description}",
        },
    ],
    api_key=OPENAI_API_KEY
)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_description}],
        api_key=OPENAI_API_KEY
    )  # Ensure this closes properly

    output_prompt = response["choices"][0]["message"]["content"]  # This should be aligned correctly

    return jsonify({"prompt": output_prompt})  # Make sure this aligns with the function block


    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

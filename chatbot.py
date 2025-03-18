from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows cross-origin requests

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Cinematic Prompting Chatbot is Live!"

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        user_input = data.get("description", "")

        if not user_input:
            return jsonify({"error": "No description provided."}), 400

        # Define the structured prompt template
        prompt_template = f"""
        Generate a highly detailed cinematic AI prompt for image generation. 
        The prompt should include:
        - **Subject:** {user_input}
        - **Lighting:** Describe realistic lighting conditions.
        - **Camera Settings:** Include specific lens, depth of field, and focus details.
        - **Composition:** Frame the scene artistically.
        - **Color Palette:** Mention dominant colors.
        - **Mood & Atmosphere:** Capture the emotional tone.
        - **Realism:** Enhance photorealistic details.

        The result should be formatted clearly and designed for **ultra-realistic AI-generated imagery**.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an AI assistant that generates structured cinematic prompts for AI image generation."},
                      {"role": "user", "content": prompt_template}],
            api_key=OPENAI_API_KEY
        )

        ai_response = response["choices"][0]["message"]["content"]

        return jsonify({"prompt": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

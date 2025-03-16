from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Replace with your OpenAI API Key
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



@app.route("/")
def home():
    return "Cinematic Prompting Chatbot is Live!"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    user_description = data.get("description")
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"I'm imagining this scene: {user_description}"}],
        api_key=OPENAI_API_KEY
    )
    
    return jsonify({"prompt": response["choices"][0]["message"]["content"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

# ✅ Replace this with your SambaNova-issued API key
SAMBA_API_KEY = os.getenv("SAMBA_API_KEY", "paste your api key here")

app = Flask(__name__)
CORS(app)

# Initialize OpenAI-compatible client using SambaNova's base URL
client = OpenAI(
    api_key=SAMBA_API_KEY,
    base_url="https://api.sambanova.ai/v1"
)

@app.route("/rewrite", methods=["POST"])
def rewrite():
    try:
        data = request.get_json()
        user_text = data.get("text", "").strip()
        tone = data.get("tone", "formal").strip().lower()

        if not user_text:
            return jsonify({"result": "⚠️ Please provide text to rewrite."}), 400

        # Construct the prompt
        prompt = f"Rewrite the following text in a {tone} tone:\n\n{user_text}"

        # Call DeepSeek-V3-0324 via SambaNova
        response = client.chat.completions.create(
            model="DeepSeek-V3-0324",
            messages=[
                {"role": "system", "content": "You are a helpful rewriting assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=300
        )

        rewritten = response.choices[0].message.content
        return jsonify({"result": rewritten})

    except Exception as e:
        return jsonify({"result": f"❌ Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

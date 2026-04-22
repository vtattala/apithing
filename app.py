from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "Backend is running"

@app.route("/advice", methods=["POST"])
def advice():
    data = request.json
    disease = data.get("disease", "unknown")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an agricultural expert helping farmers."},
                {"role": "user", "content": f"What should a farmer do for {disease}?"}
            ]
        )

        return jsonify({
            "advice": response.choices[0].message.content
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

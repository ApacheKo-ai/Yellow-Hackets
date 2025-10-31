from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import traceback

app = Flask(__name__)

# 🔑 Replace with your real Google API key
API_KEY = "AIzaSyDQU54zYrDtkyAS8axL_YUONGA-Nmf-hXY"

# Configure Gemini API for v0.8.5 (v1beta)
genai.configure(api_key=API_KEY)

# ✅ Use supported model for 0.8.5
model = genai.GenerativeModel("gemini-2.5-flash")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message")
        print("🟢 USER MESSAGE:", user_message)

        # Generate AI response using the v1beta-compatible model
        response = model.generate_content(user_message)
        print("🟢 RAW RESPONSE:", response)

        ai_text = response.text.strip()
        print("🟢 AI REPLY:", ai_text)

        return jsonify({"reply": ai_text})

    except Exception as e:
        print("⚠️ FULL ERROR TRACE:")
        traceback.print_exc()
        return jsonify({"reply": f"⚠️ Error connecting to AI server: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)

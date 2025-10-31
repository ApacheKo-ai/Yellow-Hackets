from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import traceback

app = Flask(__name__)

# 🔑 Replace with your actual Google API key
API_KEY = "AIzaSyDQU54zYrDtkyAS8axL_YUONGA-Nmf-hXY"

# ✅ Configure Gemini API (version 0.8.5)
genai.configure(api_key=API_KEY)

# ✅ Use a free supported Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

@app.route("/")
def index():
    return render_template("index.html")

# 💬 This is the API route your website JS calls
@app.route("/chat_api", methods=["POST"])
def chat_api():
    try:
        user_message = request.json.get("message")

        # 🧠 Context for WVSU Cybersecurity site
        context = """
        You are the WVSU Cybersecurity AI Assistant.
        You help visitors explore the WVSU Cybersecurity website.
        You can answer questions about:
        - Cybersecurity programs
        - Faculty and research
        - Student opportunities
        - Google Cybersecurity Clinic
        - Contact and department info
        - Navigation help (like where to find something on the site)
        Keep your answers short, helpful, and friendly.
        """

        # Combine user message with context
        full_prompt = f"{context}\n\nUser: {user_message}\nAssistant:"
        response = model.generate_content(full_prompt)
        ai_text = response.text.strip()

        print(f"🟢 USER: {user_message}")
        print(f"🤖 AI: {ai_text}")

        return jsonify({"reply": ai_text})

    except Exception as e:
        print("⚠️ FULL ERROR TRACE:")
        traceback.print_exc()
        return jsonify({"reply": f"⚠️ Error connecting to AI server: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)

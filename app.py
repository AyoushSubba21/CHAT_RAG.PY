
from flask import Flask, render_template, request, jsonify
from flask import session as flask_session
from flask_cors import CORS
from flask_session import Session
from Chat import Chat_response
import webbrowser
import os

app = Flask(__name__)
CORS(app)
# Secret key for session
app.secret_key = "your_secret_key_here"

# Configure session
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def home():
    # We only need one main template now
    return render_template('Index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({
                "status": "error",
                "reply": "No message received."
            }), 400

        user_message = data["message"]

        #history = flask_session.get("chat_history", [])

        reply = Chat_response(user_message)

        #history = flask_session.get("chat_history", [])
        #history.append({"role": "user", "content": user_message})
        #history.append({"role": "assistant", "content": reply})

        #flask_session["chat_history"] = history[-10:]

        return jsonify({
            "status": "success",
            "reply": reply
        })

    except Exception:
        return jsonify({
            "status": "error",
            "reply": "Service temporarily unavailable."
        }), 500

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)
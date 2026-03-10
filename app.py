from flask import Flask, render_template, request, jsonify
from Chat import Chat_response
import webbrowser
import os

app = Flask(__name__)

@app.route('/')
def home():
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
        reply = Chat_response(user_message)

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
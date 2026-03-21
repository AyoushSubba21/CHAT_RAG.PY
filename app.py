from flask import Flask, render_template, request, jsonify
from tempChat import Chat_response, initialize_models
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

    except Exception as e:
        print(e)
        return jsonify({
            "status": "error",
            "reply": "Service temporarily unavailable."
        }), 500

if __name__ == "__main__":
    print("Starting Flask server...")
    initialize_models()
    
    app.run(debug=True,use_reloader=False)

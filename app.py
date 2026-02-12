from flask import Flask, render_template, request ,jsonify
from Chat import Chat_response


app = Flask(__name__)
@app.route('/')
def home():
    return render_template('before.html')

@app.route('/chat',methods=['POST'])
def chat():
    user_message = request.form["message"]
    reply = Chat_response(user_message)
    return render_template("after.html",reply=reply,user_message=user_message)
    #return jsonify({"reply": reply})

import webbrowser
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
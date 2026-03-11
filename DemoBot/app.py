from flask import Flask, render_template, request, Response
import time

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.form["message"]

    # simple dummy chatbot response
    response_text = f"You said: {user_message}. This is a streamed chatbot response."

    def generate():

        for word in response_text.split():
            yield word + " "
            time.sleep(0.01)   # simulate streaming delay

    return Response(generate(), mimetype="text/plain")


if __name__ == "__main__":
    app.run(debug=True)
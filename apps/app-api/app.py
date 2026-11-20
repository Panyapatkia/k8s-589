
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return "API Service - Student ID 589"


@app.route("/api/<path:message>")
def display_message(message):
    return render_template(
        "index.html",
        message=message
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )

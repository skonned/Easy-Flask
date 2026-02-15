# flask quickstart for information on flask
from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    # home page
    return "Hello"


if __name__ == "__main__":
    app.run(debug=True)

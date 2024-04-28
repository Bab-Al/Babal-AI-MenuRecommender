from flask import Flask
from preprocessing import *

app = Flask(__name__)

data = preprocess_data()

@app.route('/')
def hello_world():
    return "hello world"

if __name__ == "__main__":
    app.run(debug=True)
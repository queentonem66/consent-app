from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Consent App is running successfully!"

if __name__ == "__main__":
    app.run(debug=True)

Fix app entry and requirements

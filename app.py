from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Alif Mahmud | Web Analytics Expert</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f9fafb;
                padding: 40px;
                color: #111;
            }
            .box {
                max-width: 700px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }
            h1 {
                margin-bottom: 5px;
            }
            .subtitle {
                color: #555;
                margin-bottom: 20px;
            }
            .price {
                font-size: 20px;
                font-weight: bold;
                margin: 15px 0;
            }
            a.button {
                display: inline-block;
                padding: 12px 20px;
                background: #1a73e8;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 15px;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>Alif Mahmud</h1>
            <div class="subtitle">
                Web Analytics Expert<br>
                Data-Driven Marketer & Web Developer
            </div>

            <p>
                I have built a custom <strong>Cookie Consent Banner</strong> with full tracking setup.
            </p>

            <p class="price">
                One-time setup: $70
            </p>

            <p>
                ✔ Banner + Consent Mode<br>
                ✔ Tracking Integration
            </p>

            <p>
                This server protects and serves JavaScript & CSS files
                for authorized domains only.
            </p>

            <a class="button" href="#" target="_blank">
                Buy Now on Fiverr
            </a>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run()

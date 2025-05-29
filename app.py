import os
import requests
from flask import Flask, request, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

API_URL = "https://api.exchangerate.host/convert"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        amount = float(request.form["amount"])
        from_currency = request.form["from_currency"]
        to_currency = request.form["to_currency"]
        params = {"from": from_currency, "to": to_currency, "amount": amount}
        response = requests.get(API_URL, params=params)
        data = response.json()
        result = data.get("result", "Error")
    return render_template("index.html", result=result)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

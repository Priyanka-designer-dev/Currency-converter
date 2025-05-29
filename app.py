import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("CURRENCY_API_KEY")

def convert_currency(amount, from_currency, to_currency):
    url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&from={from_currency}&amount={amount}"
    headers = {
        "apikey": API_KEY
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code != 200 or 'result' not in data:
        return None
    return round(data["result"], 2)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        amount = request.form["amount"]
        from_currency = request.form["from_currency"]
        to_currency = request.form["to_currency"]
        if amount and from_currency and to_currency:
            try:
                result = convert_currency(float(amount), from_currency, to_currency)
            except Exception as e:
                result = f"Error: {e}"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    from waitress import serve
    port = int(os.environ.get("PORT", 5000))
    serve(app, host="0.0.0.0", port=port)

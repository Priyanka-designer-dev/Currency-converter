from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("CURRENCY_API_KEY")
API_URL = "https://open.er-api.com/v6/latest/"

@app.route("/", methods=["GET", "POST"])
def index():
    converted_amount = None
    if request.method == "POST":
        amount = float(request.form["amount"])
        from_currency = request.form["from_currency"].upper()
        to_currency = request.form["to_currency"].upper()

        response = requests.get(f"{API_URL}{from_currency}")
        data = response.json()

        if data["result"] == "success":
            rate = data["rates"].get(to_currency)
            if rate:
                converted_amount = round(amount * rate, 2)
            else:
                converted_amount = "Error: Invalid target currency."
        else:
            converted_amount = "Error: Failed to retrieve exchange rates."

    return render_template("index.html", converted_amount=converted_amount)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
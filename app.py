from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://api.exchangerate-api.com/v4/latest/"

@app.route("/", methods=["GET", "POST"])
def index():
    converted_amount = None
    error = None
    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            from_currency = request.form["from_currency"].upper()
            to_currency = request.form["to_currency"].upper()

            response = requests.get(API_URL + from_currency)
            data = response.json()

            if "rates" not in data or to_currency not in data["rates"]:
                error = "Invalid currency code."
            else:
                rate = data["rates"][to_currency]
                converted_amount = round(amount * rate, 2)
        except Exception as e:
            error = "Error: " + str(e)
    return render_template("index.html", converted_amount=converted_amount, error=error)

if __name__ == "__main__":
    app.run(debug=True)

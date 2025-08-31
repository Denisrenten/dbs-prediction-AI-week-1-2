from flask import Flask, request, render_template
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

app = Flask(__name__)

# === STEP 1: Load Data and Train Model ===
data = pd.read_csv("combined_dbs_usdsgd.csv")

# Features (X) and Target (y)
X = data[['USD/SGD']]  # independent variable
y = data['DBS Stock Price']  # dependent variable

# Train Linear Regression Model
model = LinearRegression()
model.fit(X, y)

# Save the model for reuse (optional)
joblib.dump(model, "dbs_model.pkl")

# === STEP 2: Define Routes ===
@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            # Get the exchange rate from form input
            rate = float(request.form.get("rates"))
            
            # Predict using the model
            prediction = model.predict([[rate]])[0]
            
            return render_template("index.html", 
                                   result=f"Predicted DBS Price: {prediction:.2f} SGD")
        except ValueError:
            return render_template("index.html", result="Invalid input. Please enter a number.")
    else:
        return render_template("index.html", result="Waiting...")

if __name__ == "__main__":
    app.run(debug=True)

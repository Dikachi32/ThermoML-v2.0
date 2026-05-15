from flask import Flask, render_template, request, redirect
import joblib
import numpy as np

app = Flask(__name__)

# Load all four trained models
models = {
    "lr":       joblib.load("temperature_predictor_lr_model.pkl"),
    "gb":       joblib.load("temperature_predictor_gb_model.pkl"),
    "rf":       joblib.load("temperature_predictor_rf_model.pkl"),
    "ensemble": joblib.load("temperature_predictor_ensemble_model.pkl"),
}

MODEL_LABELS = {
    "lr":       "Linear Regression",
    "gb":       "Gradient Boosting",
    "rf":       "Random Forest",
    "ensemble": "Ensemble (Voting)",
}

@app.route("/", methods=["GET", "POST"])
def predict():
    prediction = None
    selected_model = "ensemble"   # default
    model_label    = MODEL_LABELS["ensemble"]

    if request.method == "POST":
        day        = request.form.get("day")
        humidity   = request.form.get("humidity")
        pressure   = request.form.get("pressure")
        wind_speed = request.form.get("wind_speed")
        rainfall   = request.form.get("rainfall")
        sunlight   = request.form.get("sunlight")
        selected_model = request.form.get("model", "ensemble")

        # Validate model key
        if selected_model not in models:
            selected_model = "ensemble"

        model_label = MODEL_LABELS[selected_model]

        # Guard against missing fields
        if not all([day, humidity, pressure, wind_speed, rainfall, sunlight]):
            return redirect("/")

        try:
            day        = float(day)
            humidity   = float(humidity)
            pressure   = float(pressure)
            wind_speed = float(wind_speed)
            rainfall   = float(rainfall)
            sunlight   = float(sunlight)
        except ValueError:
            return render_template(
                "temperature_predictor.html",
                prediction="Invalid input",
                selected_model=selected_model,
                model_label=model_label,
            )

        our_data   = [[day, humidity, pressure, wind_speed, rainfall, sunlight]]
        model      = models[selected_model]
        prediction = round(model.predict(our_data)[0], 2)

    return render_template(
        "temperature_predictor.html",
        prediction=prediction,
        selected_model=selected_model,
        model_label=model_label,
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")